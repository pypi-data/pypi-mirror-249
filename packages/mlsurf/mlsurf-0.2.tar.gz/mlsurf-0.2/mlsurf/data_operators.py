from abc import ABCMeta, abstractmethod

import numpy as np


class DataOperator(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def get_len(data_obj) -> int:
        pass

    @staticmethod
    @abstractmethod
    def get_slice(data_obj, lower=0, upper=None):
        """If upper is None, then it implies it's the size of length, similar to [x:]."""
        pass

    @staticmethod
    @abstractmethod
    def concatenate(data_objs: iter):
        """This function should create a new data object, concatenating copies of all the
        data objects specified in `data_objs`."""
        pass

    @staticmethod
    @abstractmethod
    def save(data_obj, directory, file_name, make_extension=True):
        pass

    @staticmethod
    @abstractmethod
    def load(directory, file_name, make_extension=True):
        """If the file doesn't exist, then a FileNotFoundError must be raised."""
        pass

    @staticmethod
    @abstractmethod
    def filter(data_obj, idxs: list):
        pass

    @staticmethod
    @abstractmethod
    def rearrange(data_obj, idxs):
        pass

    @staticmethod
    @abstractmethod
    def copy(data_obj):
        pass


class TorchOperator(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def torch_tensor_prep(data_obj):
        """Prepare data for input to torch.tensor."""
        pass

    @staticmethod
    @abstractmethod
    def get_torch_dtype(data_obj):
        pass


class NumpyOperator(DataOperator, TorchOperator):
    # create a subclass overriding this mapping if you'd prefer different defaults
    dtype_map = {
        # by default, we limit torch models to use torch.float32 as it's much
        # more computationally efficient
        np.dtype('float32'): torch.float32,
        np.dtype('float64'): torch.float32,
        np.dtype('float'): torch.float32,  # np.float is an alias for np.float64

        np.dtype('int32'): torch.int32,
        np.dtype('int64'): torch.int64,
        np.dtype('int'): torch.int64,  # np.int is an alias for np.int64
        np.dtype('int16'): torch.int16,
        np.dtype('int8'): torch.int8,
        np.dtype('uint8'): torch.uint8,

        np.dtype('bool'): torch.bool
    }

    @staticmethod
    def get_len(data_obj: np.ndarray) -> int:
        return len(data_obj)

    @staticmethod
    def get_slice(data_obj: np.ndarray, lower=0, upper=None):
        """If upper is None, then it implies it's the size of length, similar to [x:]."""
        if upper is None:
            return data_obj[lower:]
        else:
            return data_obj[lower:upper]

    @staticmethod
    def concatenate(*data_objs: iter):
        """This function should create a new data object, concatenating copies of all the
        data objects specified in `data_objs`."""
        return np.concatenate(*data_objs)

    @staticmethod
    def save(data_obj: np.ndarray, directory, file_name, make_extension=True):
        np.save(
            f"{os.path.join(directory, file_name, '.jpy' if make_extension else '')}",
                data_obj
        )

    @staticmethod
    def load(directory, file_name, make_extension=True):
        """If the file doesn't exist, then a FileNotFoundError must be raised."""
        return np.load(
            f"{os.path.join(directory, file_name, '.npy' if make_extension else '')}"
        )

    @staticmethod
    def filter(data_obj: np.ndarray, idxs: list):
        return data_obj[idxs]

    @staticmethod
    def rearrange(data_obj: np.ndarray, idxs):
        return data_obj

    @staticmethod
    def copy(data_obj: np.ndarray):
        return data_obj.copy()

    @staticmethod
    def torch_tensor_prep(data_obj: np.ndarray):
        """Prepare data for input to torch.tensor."""
        return data_obj

    @staticmethod
    def get_torch_dtype(data_obj: np.ndarray):
        return dtype_map.get(data_obj.dtype, None)
