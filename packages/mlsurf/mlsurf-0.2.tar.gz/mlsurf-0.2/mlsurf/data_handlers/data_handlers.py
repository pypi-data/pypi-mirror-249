from abc import ABCMeta
from typing import Union

from mlsurf.data_descriptors import DataDescriptor
from mlsurf.data_generator import DataGenerator, FoldWrapper
from mlsurf.preprocessing import DataPreprocessor


class NNDataHandler(metaclass=ABCMeta):
    def __init__(self, dd: DataDescriptor, data_gen: DataGenerator = None,
                 preprocessor: DataPreprocessor = None, train_ds=None, val_ds=None, test_ds=None):
        """If data_gen is provided, then train_handler, val_handler, and test_handler need to
        be strings representing the names of respective datasets from the data generator. If no data
        generator is provided, then the aforementioned 3 kwargs need to be dataset dictionaries.

        In the event that a data generator is passed, the data handler will take care of
        doing online preprocessing via the `self.online_preprocess` function should the user
        wish, otherwise it is presumed that online preprocessing was already complete before
        using this ..."""
        self.dd = dd
        self.data_gen = data_gen
        self.preprocessor = preprocessor

        self.train_ds = train_ds
        self.val_ds = val_ds
        self.test_ds = test_ds

        self.init_datasets()

    def init_datasets(self):
        """The idea of these dataset init functions is to convert the data into datasets
        (as in e.g., Pytorch/TF datasets), which can readibly be used by the respective
        concrete trainer classes."""

        # If there is no preprocessor, but a data generator exists, then we assume
        # data generation as already been complete.
        if self.preprocessor is not None:
            if self.data_gen is None:
                raise "A data generator needs to be specified with a preprocessor."
            self.preprocessor.preprocess(self.data_gen, online=True)

        # the default implementations of the init_*_dataset functions assume that
        # the dataset fields are all `DatasetHandler`s
        if self.train_ds is not None:
            self.init_train_dataset()
        if self.val_ds is not None:
            self.init_val_dataset()
        if self.test_ds is not None:
            self.init_test_dataset()

    def init_train_dataset(self):
        self.train_ds.init_dataset()

    def init_val_dataset(self):
        self.val_ds.init_dataset()

    def init_test_dataset(self):
        self.test_ds.init_dataset()

    def get_train_batch_iter(self):
        self.train_ds.get_batch_iter()

    def get_val_loader(self):
        self.val_ds.get_batch_iter()

    def get_test_loader(self):
        self.test_ds.get_batch_iter()


class FoldNNDataHandler(NNDataHandler):
    def __init__(self, *args, data_gen: Union[FoldWrapper, DataGenerator] = None, **kwargs):
        if data_gen is None:
            raise "data_gen kwarg must be present for FoldNNDataHandler."
        self.data_gen = data_gen
        super(FoldNNDataHandler, self).__init__(*args, **kwargs)

    def next_fold(self):
        return self.data_gen.next_fold()
