from enum import Enum


class CachingEnum(Enum):
    # TODO: do this.
    @classmethod
    def has(cls, e):
        # if "cache" doesn't exist, make one, putting everything in a set
        # `return e in cls.cache`
        if e in (item.value for item in CachingEnum):
            pass


class ConvenientEnum(Enum):
    @classmethod
    def has(cls, e):
        return any(e == item.value for item in cls)


class SplitMode(ConvenientEnum):
    RANDOM = 'random'
    STRATIFIED = 'stratified'
    EVEN = 'even'


class DataType(Enum):
    NUMPY = 0
    PANDAS = 1


class SaveMode(ConvenientEnum):
    # Persist every time a new best metric is produced; don't bother saving ot memory.
    PERSIST_IMMEDIATELY_NO_MEM = 0

    # Save model params to memory every time a new best metric is produced, and persist to disk
    # only at the end of training.
    SAVE_TO_MEM_PERSIST_AT_END = 1

    # save to memory only, and let the user decide if/how to save it from there
    SAVE_TO_MEM = 2

    DONT_SAVE = 3

    # TODO: Save model params to memory every time a new best metric is produced, but have a mimimum
    # number of epochs between persisting a model to disk

    # TODO: have more types of persist/memory configurations


class ClsMetric(ConvenientEnum):
    ACCURACY = 'acc'
    RECALL = 'rc'
    PRECISION = 'pr'
    F1_SCORE = 'micro_f1'
    F2_SCORE = 'macro_f1'


class RegMetric(ConvenientEnum):
    LOSS = 'loss'


class Metric(ConvenientEnum):
    # batch regression metrics
    BATCH_LOSS = 'batch_loss'

    # train regression metrics
    TRAIN_LOSS = 'train_loss'
    BEST_TRAIN_LOSS = 'best_train_loss'

    # val classification metrics
    VAL_ACC = 'val_acc'
    BEST_VAL_ACC = 'best_val_acc'

    # validation regression metrics
    VAL_LOSS = 'val_loss'
    BEST_VAL_LOSS = 'best_val_loss'

    # timing
    EPOCH_TRAIN_TIME = 'epoch_train_time'
    EPOCH_TIME = 'epoch_time'


class Reporting(ConvenientEnum):
    BATCH = 'batch'
    EPOCH = 'epoch'
    TEST = 'test'


class ValMode(ConvenientEnum):
    OFF = 0
    ON = 1
    AUTO = 2


class OutputMode(ConvenientEnum):
    OFF = 0
    WRITE_TO_FILE = 1
    STDOUT = 2
    DEFAULT = 3


class ProcessingStage:
    """This says what is encompassed in offline data preprocessing for the DataPreprossor.preprocess
    function. Whichever option is picked, then all other options before it must also be completed
    in offline mode too, due to the staged nature of data preprocessing. So this can be interpreted
    as "in offline mode, preprocess up to ProcessingStage.X"."""
    OFF = 0
    EXTRACT = 1
    CREATE_DATASETS = 2
    TRANSFORM = 3
