import csv
import sys
from abc import ABCMeta, abstractmethod
import copy
from datetime import datetime
import itertools
import logging
import os
import time

from tqdm import tqdm

from mlsurf.enums import Metric, SaveMode, ValMode, Reporting, ClsMetric, OutputMode


class NNTrainer(metaclass=ABCMeta):
    """Neural Network trainer. This will perform training functions typically required by neural networks,
    such as a backward pass"""

    # Sets out the prime metrics, i.e., the main metric to determine "how good" the model is, and if
    # we should save the model's parameters based on an improvement in this metric.
    # The form of new entries in here is:
    # <metric name, e.g., 'val_acc'>: <function to determine if the metric has improved>
    # The best metric will be assumed to be named best_<metric name>.
    # New instantiations of this class var can be made in subclasses without having to redefine the keys
    # in the super classes, due to the super class traversal logic in the __init__ method.
    metric_comparison_funcs = {
        'loss': lambda metric, best_metric: metric < best_metric
    }
    def __init__(self, optimiser, data_handler, model=None, epochs=None, batch_report_rate=1, epoch_report_rate=1,
                 val_mode=ValMode.AUTO, epoch_val_rate=1, save_behaviour=SaveMode.DONT_SAVE,
                 perf_metric='train.loss', reporting=None, custom_loss_func=None,
                 run_dir=None, make_run_dir: bool = True, log_dir=None, log_file_name='log.log',
                 model_save_dir=None, model_name='model.pth', metrics_dir=None,
                 epoch_metrics_file_name='epoch_metrics.csv', batch_metrics_file_name='batch_metrics.csv',
                 test_metrics_file_name='test_metrics.csv', test_metrics_out_mode=OutputMode.OFF,
                 epoch_metrics_out_mode=OutputMode.DEFAULT, batch_metrics_out_mode=OutputMode.STDOUT,
                 log_output_mode=OutputMode.DEFAULT, log_level=logging.INFO, logger_name='trainer',
                 default_output_mode=OutputMode.STDOUT):
        self.model = model
        self.best_model = None
        self.best_metrics = None

        self.optimiser = optimiser
        self.data_handler = data_handler
        self.epochs = epochs

        self.save_behaviour = save_behaviour

        # set up output paths
        self.run_dir = run_dir
        if make_run_dir:
            self.create_run_dir()
        self.log_dir = self.run_dir if log_dir is None else log_dir
        self.model_save_dir = self.run_dir if model_save_dir is None else model_save_dir
        self.log_file_name = log_file_name
        self.model_name = model_name
        self.best_model_name = f"best_{self.model_name}"
        self.best_model_save_path = os.path.join(self.model_save_dir, self.best_model_name)

        # set up logging
        self.log = None
        if log_output_mode is OutputMode.DEFAULT:
            log_output_mode = default_output_mode
        self.log_output_mode = log_output_mode
        self.log_level = log_level
        self.logger_name = logger_name
        self.setup_logger()

        # infer validation mode if user hasn't specified
        val_mode = int(val_mode)  # cast to int in case bool is used
        if val_mode == ValMode.AUTO:
            if self.validate is NNTrainer.validate:
                val_mode = ValMode.OFF
            else:
                val_mode = ValMode.ON
        elif val_mode == ValMode.ON and self.validate is NNTrainer.validate:
            raise "ValMode is ON but you haven't got any validation logic."
        elif val_mode == ValMode.OFF:
            # TODO: check that user hasn't specified other val-oriented metrics for reporting/save-metrics/etc
            if perf_metric == Metric.BEST_VAL_ACC:
                raise "ValMode is OFF, but BEST_VAL_ACC is being used as save metric"
        else:
            raise "Invalid val_mode."

        # set up metrics writing
        for out_mode in ('batch', 'epoch', 'test'):
            if getattr(self, f"{out_mode}_metrics_write_mode") == OutputMode.DEFAULT:
                setattr(self, f"{out_mode}_metrics_write_mode", default_output_mode)
        self.metrics_dir = self.run_dir if metrics_dir is None else metrics_dir
        self.epoch_metrics_file = os.path.join(metrics_dir, epoch_metrics_file_name)
        self.batch_metrics_file = os.path.join(metrics_dir, batch_metrics_file_name)
        self.test_metrics_file = os.path.join(metrics_dir, test_metrics_file_name)
        self.batch_metrics_out_mode = batch_metrics_out_mode
        self.epoch_metrics_out_mode = epoch_metrics_out_mode
        self.test_metrics_out_mode = test_metrics_out_mode
        self.setup_epoch_metrics_output()
        self.setup_batch_metrics_output()
        self.setup_test_metrics_output()

        # instantiate prime metric related attributes
        for cls in self.__class__.__mro__:
            if "metric_comparison_funcs" in cls.__dict__:
                if perf_metric in cls.metric_comparison_funcs:
                    self.is_new_best = cls.metric_comparison_funcs[perf_metric]
                    break
        else:
            raise "invalid prime metric"
        self.perf_dtype = perf_metric.split('.')[0]  # refers to data type, e.g., 'train', 'val' etc...
        self.perf_metric = perf_metric.split('.')[1]  # refers to metric type, e.g., 'acc', 'loss', etc...
        self.best_perf_metric = f"best_{self.perf_metric}"

        default_reporting = {
            Reporting.BATCH: (f'batch.loss', f'train.loss', perf_metric),
            Reporting.EPOCH: (f'train.loss', perf_metric),
            Reporting.TEST: (f'train.best_loss', self.perf_metric,
                             f"{self.perf_dtype}.{self.best_perf_metric}")
        }
        if reporting is not None:
            for key in reporting:
                default_reporting[key] = reporting[key]
        self._process_reporting(default_reporting)
        self.reporting = default_reporting

        self.val_mode = val_mode
        self.epoch_val_rate = epoch_val_rate

        self.batch_report_rate = batch_report_rate
        self.epoch_report_rate = epoch_report_rate

        self.metrics = {}

    def setup_logger(self):
        # TODO: set up logger, similar to how its done in old framework code
        logger = logging.getLogger(self.logger_name)
        if self.log_output_mode is OutputMode.WRITE_TO_FILE:
            file_handler = logging.FileHandler(os.path.join(self.log_dir, self.log_file_name))
            # add formatter if required
            logger.addHandler(file_handler)
            logger.setLevel(self.log_level)
        elif self.log_output_mode == OutputMode.STDOUT:
            stdout_handler = logging.StreamHandler(sys.stdout)
            # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            # stdout_handler.setFormatter(formatter)
            logger.addHandler(stdout_handler)
            logger.setLevel(self.log_level)
        elif self.log_output_mode == OutputMode.OFF:
            logger.disabled = True
        else:
            raise "invalid log mode"
        self.log = logger
        self.log.info("lol")

    def setup_metrics_file(self, metrics_file, report_group):
        with open(metrics_file, mode='a', newline='') as metrics_file:
            writer = csv.writer(metrics_file)
            writer.writerow([f"{dtype, metric}" for dtype, metric in self.reporting[report_group]])

    def setup_epoch_metrics_output(self):
        if self.epoch_metrics_out_mode == OutputMode.WRITE_TO_FILE:
            self.setup_metrics_file(self.epoch_metrics_file, 'epoch')

    def setup_batch_metrics_output(self):
        if self.batch_metrics_out_mode == OutputMode.WRITE_TO_FILE:
            self.setup_metrics_file(self.batch_metrics_file, 'batch')

    def setup_test_metrics_output(self):
        if self.test_metrics_out_mode == OutputMode.WRITE_TO_FILE:
            self.setup_metrics_file(self.test_metrics_file, 'test')

    def write_metrics_to_file(self, metrics_file, report_group):
        with open(metrics_file, mode='a', newline='') as metrics_file:
            writer = csv.writer(metrics_file)
            writer.writerow([self.metrics[dtype][metric]
                             if dtype in self.metrics and metric in self.metrics[dtype] else None
                             for dtype, metric in self.reporting[report_group]])

    def write_metrics_to_stdout(self, report_group):
        metric_strings = [f"{dtype}.{metric}: {self.metrics[dtype][metric]}"
                          for dtype, metric in self.reporting[report_group]
                          if dtype in self.metrics and metric in self.metrics[dtype]]
        epoch_metrics = ', '.join(metric_strings)
        print(f"\nMetrics for {report_group}:")
        print(f"{epoch_metrics}\n")

    def write_metrics(self, out_mode, report_group, metrics_file):
        if out_mode == OutputMode.OFF:
            return
        elif out_mode == OutputMode.WRITE_TO_FILE:
            self.write_metrics_to_file(report_group, metrics_file)
        elif out_mode == OutputMode.STDOUT:
            self.write_metrics_to_stdout(report_group)
        else:
            raise "invalid output mode"

    def write_batch_metrics(self):
        if self.batch_metrics_out_mode == OutputMode.OFF:
            return
        elif self.batch_metrics_out_mode == OutputMode.WRITE_TO_FILE:
            self.write_metrics_to_file('batch', self.batch_metrics_file)
        elif self.batch_metrics_out_mode == OutputMode.STDOUT:
            raise "standard out should be handled with tqdm"
        else:
            raise "invalid output mode"

    def write_epoch_metrics(self):
        self.write_metrics(self.epoch_metrics_out_mode, 'epoch', self.epoch_metrics_file)

    def write_test_metrics(self):
        self.write_metrics(self.test_metrics_out_mode, 'test', self.test_metrics_file)

    def create_run_dir(self, sep='|'):
        """Default automatic run directory creation creates a new run directory based
        on the current date. If self.run_dir was provided during initialisation, then
        this is used as the parent directory for the run dir."""
        if self.run_dir is not None:
            parent_dir = self.run_dir
        else:
            parent_dir = '..'

        today_date = datetime.today()
        mm = today_date.month
        dd = today_date.day
        v = 1

        # Format the directory name
        run_dir = f"{parent_dir}/{mm:02d}-{dd:02d}{sep}{v}"

        # Check if the directory exists, and increment the version number if it does
        while os.path.exists(run_dir):
            v += 1
            run_dir = f"{parent_dir}/{mm:02d}-{dd:02d}{sep}{v}"

        self.run_dir = run_dir

    def _process_reporting(self, reporting: dict):
        for k, v in reporting.items():
            reporting[k] = (tuple(self._get_dtype_metric(x)) for x in reporting[k])

    @staticmethod
    def _get_dtype_metric(key) -> list:
        return key.split('.')

    def _init_epoch_metrics(self):
        pass

    def _get_metrics_for_report_group(self, group):
        for dtype, metric in self.reporting[group]:
            pass

    def reset(self, reset_model: bool = False, new_model=None):
        """Reset the trainer so that it can start afresh. Optionally reset the model
        with the `new_model` parameter."""
        self.metrics = {}
        if reset_model:
            self.model = new_model
        # TODO: reset any save memory caches, etc...

    @abstractmethod
    def convert_loss(self, loss) -> float:
        pass

    @abstractmethod
    def lr_scheduler_step(self, metric):
        """LR scheduler step"""
        pass

    @abstractmethod
    def backward_pass(self, loss):
        pass

    def create_fold_model(self, fold):
        """Default behaviour is to assume the model is given as self.model initially, and we create
        copies of it for each fold.
        Override this if you want to do things more elegantly, e.g., create a new instance
        each fold, or potentially even a different model per fold."""
        if hasattr(self, '_master_model'):
            return self.copy_model(self._master_model)
        elif self.model is None:
            raise "Either pass in a model to __init__, " \
                  "or override create_fold_model to create one."
        else:
            self._master_model = self.copy_model(self.model)

    @staticmethod
    def append_suffix_to_path(orig_path, fold=None, fold_prefix="_fold", has_extension=False):
        suffix = f"{fold_prefix}{fold}" if fold is not None else ""
        if has_extension:
            base_name, extension = os.path.splitext(orig_path)
            new_path = base_name + suffix + extension
        else:
            new_path = f"{orig_path}{suffix}"
        return new_path

    def change_output_paths_with_fold(self, output_path_vars, fold: int = None, fold_prefix="",
                                      has_extension=False):
        for var in output_path_vars:
            orig_path = getattr(self, f"_{var}")
            setattr(self, var, self.append_suffix_to_path(orig_path, fold, fold_prefix=fold_prefix,
                                                          has_extension=has_extension))

    def save_original_model_output_paths(self, output_path_vars):
        for var in output_path_vars:
            setattr(self, f"_{var}", getattr(self, var))

    @staticmethod
    def get_all_model_output_dir_vars():
        # TODO: A better way for these two functions would be to "register" variables as
        # output dir vars / output file vars, and allow the user to easily do so as required.
        # It would have to be explained clearly that these variables are per-model things only.
        # Another benefit of doing this, is we have the option to tie more output vars to be
        # model-specific, such as having a log file for each model, or one master log file.
        # It would also be desirable to have better control of these variables being per
        return "model_save_path", "metrics_path",

    @staticmethod
    def get_all_model_output_file_vars():
        return "model_name", "metrics_file"

    def train_with_folds(self, separate_run_dirs: bool = False):
        """It is assumed that self.data_handler is of type FoldDataHandler. This would typically
        mean training with Cross-Validation, however, it's up to the data handler how the
        data changes between folds, so it's a little more abstract than that."""
        # TODO: decide if we'll make this CV logic a Mixin class instead
        # TODO: have more fine-grained configuration for output dir/file separation logic between
        #       fold models. E.g., let run_dir stay the same, but the others get nested.

        # save original output vars
        if separate_run_dirs:
            output_path_vars = self.get_all_model_output_dir_vars()
            fold_prefix = "/fold"
            has_extension = False
        else:
            output_path_vars = self.get_all_model_output_file_vars()
            fold_prefix = "_fold"
            has_extension = True
        self.save_original_model_output_paths(output_path_vars)

        fold = 1
        while self.data_handler.next_fold():
            new_model = self.create_fold_model(fold)
            self.reset(reset_model=True, new_model=new_model)
            self.change_output_paths_with_fold(output_path_vars, fold_prefix=fold_prefix,
                                               has_extension=has_extension)
            self.train()
            fold += 1

        # reset the paths
        self.change_output_paths_with_fold(output_path_vars, fold=None)

    def train(self):
        self.metrics['train']['loss'] = float('inf')

        data_loader = self.data_handler.get_train_loader()

        if self.epochs is None:
            epoch_gen = itertools.count()
            tqdm_filler = ""
        else:
            epoch_gen = range(self.epochs)
            tqdm_filler = f"/{self.epochs}"

        for epoch in epoch_gen:
            batch_loss_accum = 0
            self.metrics['train']['loss'] = 0  # for epoch

            epoch_start_time = time.time()

            use_tqdm = self.batch_metrics_out_mode == OutputMode.STDOUT

            if use_tqdm:
                batch_iter = tqdm(data_loader, desc=f"Epoch {epoch + 1}{tqdm_filler}", position=0, leave=True)
            else:
                batch_iter = data_loader

            batch_idx = 0
            for batch in batch_iter:
                if self.loss_function is not None:
                    outputs, loss_args = self.train_step(batch)
                    loss = self.loss_function(outputs, *loss_args)
                else:
                    loss = self.train_step(batch)
                self.backward_pass(loss)
                self.hook_train_batch_end()

                self.metrics['batch']['loss'] = self.convert_loss(loss)
                batch_loss_accum += self.metrics['batch']['loss']

                if (batch_idx + 1) % self.batch_report_rate == 0:
                    if use_tqdm:
                        batch_iter.set_postfix({f'{d}.{m}': self.metrics[d][m]
                                                for d, m in self.reporting['batch'].values()
                                                if d in self.metrics and m in self.metrics[d]})
                    else:
                        self.write_batch_metrics()

                batch_idx += 1

            self.metrics['train']['loss'] = batch_loss_accum / (batch_idx + 1)
            self.metrics['epoch']['train_time'] = time.time() - epoch_start_time

            if self.val_mode == ValMode.ON:
                self.validate()

            if self.is_new_best(self.metrics[self.perf_dtype][self.perf_metric],
                                self.metrics[self.perf_dtype][self.best_perf_metric]):
                self.save_new_best_model()
                self.metrics[self.perf_dtype][self.best_perf_metric] = \
                    self.metrics[self.perf_dtype][self.perf_metric]

            # WARNING: it's assumed that we always want to minimise the loss metric
            if self.metrics['train']['loss'] < self.metrics['train']['best_loss']:
                self.metrics['train']['best_loss'] = self.metrics['train']['loss']

            self.metrics['epoch']['time'] = time.time() - epoch_start_time

            if (epoch + 1) % self.epoch_report_rate == 0:
                self.write_epoch_metrics()

            self.hook_train_epoch_end()

        self.flush_best_model()

        self.hook_train_end()

        # TODO: reporting, logging, hooks, tensorboard, early stopping, etc...

    def train_step(self, batch):
        """The default is to assume the model will return the loss. If this step is to instead return
        x predictions, it is assumed the loss will be computed by the loss_function configured during
        __init__. If this is the case, then a tuple should be returned instead, representing the
        arguments to be input into the loss function which will be invoked immediately after this function.
        E.g., (model_outputs, y_data) where y_data might be taken from the batch, e.g., batch[1]."""
        return self.model(batch)

    @abstractmethod
    def validate(self, model=None):
        """This function is intended to be called during training. If you want to test with the
        validation set at the end of training, then use the test function, but with validation
        data."""
        pass

    @abstractmethod
    def test(self, model=None):
        pass

    def save_new_best_model(self):
        if self.save_behaviour != SaveMode.DONT_SAVE:
            # TODO: save aside best metrics too (give kwarg l8r on for this functionality)
            if self.save_behaviour == SaveMode.SAVE_TO_MEM_PERSIST_AT_END or \
                    self.save_behaviour == SaveMode.SAVE_TO_MEM:
                self.best_model = self.copy_model(self.model)
                # TODO: again, we should allow the option for metrics saving, and we should have some
                # flexibility on which metrics to pick. Bear in mind that these best metrics may not
                # contain the optimal required metrics because e.g., averaging metrics over all epochs
                # won't be fully materialised until the end. (so be careful how you use these
                # "best metrics").
                self.best_metrics = copy.deepcopy(self.metrics)
            elif self.save_behaviour == SaveMode.PERSIST_IMMEDIATELY_NO_MEM:
                self.save_model_to_disk(self.model, self.best_model_save_path)
            else:
                raise f"save mode: {self.save_behaviour} is currently not supported"

    def flush_best_model(self):
        if self.save_behaviour == SaveMode.SAVE_TO_MEM_PERSIST_AT_END and self.best_model is not None:
            self.save_model_to_disk(self.best_model, self.best_model_save_path)

    @staticmethod
    def copy_model(model):
        """Override this if underlying lib's model objects don't support copy.deepcopy."""
        return copy.deepcopy(model)

    @staticmethod
    @abstractmethod
    def save_model_to_disk(model=None, model_save_path="./model.pth"):
        pass

    def get_best_model(self):
        # TODO: add extra logic that if best_model is None, then load it from best save path if exists
        return self.best_model

    def get_best_metrics(self):
        return self.best_metrics

    def hook_train_batch_end(self):
        pass

    def hook_test_batch_end(self):
        pass

    def hook_train_epoch_end(self):
        pass

    def hook_train_end(self):
        pass

    def freeze(self):
        """Freeze all model params."""
        pass

    def unfreeze(self):
        pass

    def report(self):
        """Manual reporting, instigated by the user. This should use the thingy reporting."""
        pass

    def change_model_name(self, new_model_name):
        self.model_name = new_model_name
        self.best_model_name = f"best_{new_model_name}"
        self.best_model_save_path = os.path.join(self.model_save_dir, self.best_model_name)


class FineTuningNNTrainer(NNTrainer, metaclass=ABCMeta):
    def __init__(self, ft_trainer: NNTrainer, *args, resolve_name_conflicts=True, **kwargs):
        super(FineTuningNNTrainer, self).__init__(*args, **kwargs)

        if resolve_name_conflicts:
            if ft_trainer.model_name == self.model_name:
                ft_trainer.change_model_name(f"ft_{self.model_name}")
            if os.path.join(self.log_dir, self.log_file_name) == \
                    os.path.join(ft_trainer.log_dir, ft_trainer.log_file_name) \
                    and ft_trainer.logger_name == self.logger_name:
                ft_trainer.logger_name = f"ft_{self.logger_name}"
                ft_trainer.setup_logger()
        elif ft_trainer.model_name == self.model_name:
            self.log.warn(f"WARNING: ft_trainer.model_name and trainer.model_name are the same: {self.model_name}")

        # This should be an instantiated object.
        self.ft_trainer = ft_trainer

        self.ft_model = None

    @abstractmethod
    def build_ft_model(self):
        """Build a model. E.g., deep copy self.model (and put a prediction on on it?), etc..."""
        pass

    def process_ft_metrics(self, ft_metrics):
        """Default behaviour is to take all metrics groups, and prefix ft_ to them, then add them
        to self.metrics."""
        for k, v in ft_metrics.items():
            self.metrics[f'ft_{k}'] = v

    def extract_ft_model(self):
        """Default behaviour is to use the reference to the model trained by the ft_trainer. Override
        this is you want extra behaviour, such as resetting ft_trainer and nulling it's model."""
        self.ft_model = self.ft_trainer.get_best_model()
        ft_metrics = self.ft_trainer.get_best_metrics()
        self.process_ft_metrics(ft_metrics)

    def fine_tune(self):
        ft_model = self.build_ft_model()
        self.ft_trainer.reset(reset_model=True, new_model=ft_model)
        self.ft_trainer.train()


class ValidateWithFineTuningNNTrainer(metaclass=ABCMeta, FineTuningNNTrainer):
    """Rules for using this:
    - ft_model's best model's metrics' groups will be added to self.metrics with "ft_" prefixed
      to them, so e.g,. if you want to make the perf_metric='ft_best_val_acc', then this trainer
      will save a fine tuned model at the end of an epoch if it's best validation accuracy is
      better than the previous best fine tuned model's accuracy."""

    def __init__(self, val_func=None, *args, **kwargs):
        super(ValidateWithFineTuningNNTrainer, self).__init__(*args, **kwargs)
        self.val_func = val_func

    def validate(self, model=None):
        # NOTE: remember, validate function is intended to be done during training loop, so
        # it doesn't matter overriding that in AutoEvalMixin. Then we get to keep all the useful
        # stuff too.

        self.fine_tune()
        self.extract_ft_model()

        if self.val_func is not None:
            # we don't make assumptions as to how/if the fine tuning trainer validates the model,
            # so we give the caller the option to validate the fine tuned model if required
            # TODO: There should be a better way to do this, i.e., a flag that signals to pick
            # the next MRO validate function. An even better way would be to do some sort of
            # clabback registering, then we don't even need to worry about therse complciatoins.
            # With regards to knowing if to do validatoin or not, perhas check how pytorch lightinng
            # does it, i.e., loading the validation loader? With callback registering, we could
            # call this func something else, e.g., fine_tune_val, and register it, and then the
            # normal validate stuff can be registered if ValMod is ON or something. But it would b
            # rly nice to not have to resort to complex hooking logic
            self.val_func(self, model=self.ft_model)

    def infer(self, x):
        """Override default inference step to get from the ft_model instead"""
        self.ft_model(x)


class AutoEvalMixin(metaclass=ABCMeta):
    """This class assumes the inferrence logic is the same for the validation step and testing."""

    @abstractmethod
    def compute_eval_metrics(self, stats, mode='test') -> dict:
        pass

    @abstractmethod
    def accum_stats(self, stats, outputs, y):
        pass

    def evaluate(self, data_loader, metrics='test'):
        stats = None
        for batch in data_loader:
            outputs = self.infer(batch)
            self.accum_stats(stats, outputs, batch)
            self.hook_batch_eval_end()

        metrics = self.compute_eval_metrics(stats)

        return metrics

    def validate(self):
        data_loader = self.data_handler.get_val_loader()
        self.evaluate(data_loader, metrics='val')
        # add best metrics (or do it in self.evaluate)

    def test(self, data_loader=None):
        if data_loader is None:
            data_loader = self.data_handler.get_test_loader()
        self.evaluate(data_loader, metrics='test')
        # add test metrics (or do it in self.evaluate)

    def infer(self, x):
        return self.model(x)

    def hook_batch_eval_end(self):
        pass


class ClassificationAutoEvalMixin(AutoEvalMixin, metaclass=ABCMeta):
    def compute_eval_metrics(self, stats, metrics_group='test') -> dict:
        metrics = self.metrics[metrics_group]
        # TODO: decide best way to do this; perhaps we also need to check if these things are
        # required for reporting or prime metric too, otherwise we'll just skip them
        if ClsMetric.ACCURACY in metrics:
            self.metrics[ClsMetric.ACCURACY] = None
        if ClsMetric.RECALL in metrics:
            self.metrics[ClsMetric.RECALL] = None
        # etc...

    def accum_stats(self, stats, outputs, y):
        # convert the outputs to some kind of dict that compute_eval_metrics understands
        pass
