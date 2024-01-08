from abc import ABCMeta, abstractmethod

import torch
from torch.utils.data import DataLoader, TensorDataset, Dataset

from torch_datasets import ContrastiveSelfSupTorchDataset
from mlsurf.data_descriptors import DataDescriptor
from mlsurf.data_generator import DataGenerator
from mlsurf.data_operators import TorchOperator


class NNDatasetHandler(metaclass=ABCMeta):
    def __init__(self, ds_wrapper_cls, dataset=None, dataset_name=None, dd: DataDescriptor = None, ds_prefixes=('X', 'y'),
                 batch_size=64, shuffle=True):
        """`data` can be either a dataset dict or a string as part the respective
        dataset's name in the dataset generator. When it is specified as a string,
        it is expected that the wrapping DataHandler will inject the respective
        dataset dict when required before use. The DataDescriptor may or may not be
        required depending on the subclass and if data needs converting. In most
        scenarios the data will probably already be in a compatible state to be
        converted to respective datasets."""
        self.dd = dd

        if dataset is None and dataset_name is None:
            raise "Both dataset and dataset_name cannot be None at the same time"
        self.dataset = dataset
        self.dataset_name = dataset_name

        self.ds_wrapper_cls = ds_wrapper_cls
        self.ds_prefixes = ds_prefixes
        self.ds_wrapper = None
        self.batch_size = batch_size
        self.shuffle = shuffle

        self.dataset_name = None

    def set_data_descriptor(self, dd):
        """The expected use case here is by a wrapping data handler so that the
        dev doesn't have to needlessly input the dd into every dataset."""
        self.dd = dd

    def load_dataset(self, dataset):
        self.dataset = dataset

    def clear_dataset(self):
        self.dataset = None

    def clear_ds_wrapper(self):
        self.ds_wrapper = None

    def init_dataset(self, gen: DataGenerator = None):
        if self.dataset_name is not None:
            if gen is not None:
                self.dataset = gen.get_dataset(self.dataset_name)
            elif self.dataset is None:
                raise "dataset is None and cannot be generated."
        self.init_ds_wrapper()

    @abstractmethod
    def init_ds_wrapper(self):
        raise NotImplementedError()

    @abstractmethod
    def get_batch_iter(self):
        raise NotImplementedError()


class TorchDatasetHandler(NNDatasetHandler):
    def __init__(self, *args, ds_wrapper_cls=TensorDataset, num_workers=0, drop_last_batch=False,
                 device='cuda', dtypes=None, **kwargs):
        """For PyTorch datasets, we need to convert data to torch tensors via torch.tensor.
        A lot of data types can be converted to torch tensors including, lists, tuples,
        numpy arrays, etc... But some data types will first need to be converted to a
        suitable format, such as pandas dataframes to numpy arrays. In such circumstances
        the `tensor_prep` function will be called. The default implementation here will
        call the respective prefix's `torch_tensor_prep` function, which requires said
        data operator to implement the TorchOperator interface. Override the `tensor_prep`
        functoin if different conversion logic is required."""
        super(TorchDatasetHandler, self).__init__(*args, ds_wrapper_cls=ds_wrapper_cls, **kwargs)

        self.num_workers = num_workers
        self.drop_last_batch = drop_last_batch
        self.device = device
        self.dtypes = dtypes

    def init_ds_wrapper(self, gen=None):
        # create the tensor based dataset
        tensors = []
        for prefix in self.ds_prefixes:
            tensors.append(self.create_tensor(prefix))
        self.ds_wrapper = self.create_ds_wrapper(*tensors)

    def create_ds_wrapper(self, *tensors) -> Dataset:
        return self.ds_wrapper_cls(*tensors)

    def create_tensor(self, prefix):
        data_obj = self.dataset['data'][prefix]
        dtype = self.get_dtype(prefix)
        try:
            tensor = torch.tensor(data_obj, dtype=dtype, device=self.device)
        except TypeError:
            tensor = torch.tensor(self.tensor_prep(prefix), dtype=dtype, device=self.device)
        return tensor

    def tensor_prep(self, prefix):
        """This function will attempt to automatically prepare the respective data
        object for `prefix`, which will require that the respective data operator
        implements the `TorchOperator` interface."""
        data_op = self.dd.get_data_operator(prefix)
        if not isinstance(data_op, TorchOperator):
            raise TypeError(f"Data object for prefix {prefix} is not compatible "
                            f"with torch.tensor, and the prefix's respective "
                            f"data operator is not a TorchOperator.")
        return data_op.torch_tensor_prep(self.dataset['data'][prefix])

    def get_dtype(self, prefix):
        """This function will return dtype as specified in `self.dtypes`, or it will
        automatically infer the dtype using the prefix's data operator for which it
        will need to implement the `TorchOperator` interface."""
        if self.dtypes is None or prefix not in self.dtypes:
            if 'torch_dtype' in self.dd.prefixes[prefix]:
                return self.dd.prefixes[prefix]['torch_dtype']
            data_op = self.dd.get_data_operator(prefix)
            if not isinstance(data_op, TorchOperator):
                raise TypeError(f"dtype hasn't been provided for prefix {prefix}, "
                                f"and the respective data operator is not a "
                                f"TorchOperator.")
            return data_op.get_torch_dtype(self.dataset['data'][prefix])
        return self.dtypes[prefix]

    def get_batch_iter(self):
        return DataLoader(self.ds_wrapper, batch_size=self.batch_size, shuffle=self.shuffle,
                          num_workers=self.num_workers, drop_last=self.drop_last_batch)


class ContrastiveSelfSupTorchDSHandler(TorchDatasetHandler):
    def __init__(self, *args, x_prefix='X', gid_prefix='gid',
                 retrieval_mode=ContrastiveSelfSupTorchDataset.CYCLE,
                 ds_wrapper_cls=ContrastiveSelfSupTorchDataset, **kwargs):
        ds_prefixes = (x_prefix, gid_prefix)
        super(ContrastiveSelfSupTorchDSHandler, self).__init__(*args, ds_wrapper_cls=ds_wrapper_cls,
                                                               ds_prefixes=ds_prefixes,
                                                               **kwargs)
        self.retrieval_mode = retrieval_mode

    def create_ds_wrapper(self, *tensors):
        return self.ds_wrapper_cls(*tensors, retrieval_mode=self.retrieval_mode)
