from abc import ABCMeta, abstractmethod

from mlsurf.data_operators import DataOperator, NumpyOperator
from mlsurf.data_transformers import DataTransformer
from mlsurf.enums import DataType


class DataDescriptor(metaclass=ABCMeta):
    data_dir: str = './data'

    prefixes = {
        'X': {
            'type': DataType.NUMPY
        }
    }

    transformer = None
    
    data_type_operator_map = {
        DataType.NUMPY: NumpyOperator
        # Add more as necessary
    }

    def get_data_operator(self, prefix: str) -> DataOperator:
        data_type = self.prefixes[prefix]['type']
        return self.prefixes[prefix]['type']

    def get_transformer(self) -> DataTransformer:
        self.transformer.dd = self
        return self.transformer

    def get_prefixes(self) -> list:
        return tuple(self.prefixes.keys())
    
    def get_prefix_items(self):
        return tuple(self.prefixes.items())
    
    def get_prefixes_with_data_ops(self, *data):
        """Yield every prefix with corresponding data operator. When datasets are
        specified, we only want the prefixes that intersect all of them."""
        if len(data) == 0:
            prefixes = self.get_prefixes()
        else:
            prefixes = [pref for pref in self.get_prefixes()
                        if all([pref in ds for ds in data])]
        for prefix in prefixes:
            data_op = self.dd.get_data_operator(prefix)
            yield prefix, data_op

    def get_data_with_data_ops(self, *data):
        if len(data) == 0:
            prefixes = self.get_prefixes()
        else:
            prefixes = [pref for pref in self.get_prefixes()
                        if all([pref in ds for ds in data])]
        for prefix in prefixes:
            data_op = self.dd.get_data_operator(prefix)
            for ds in data:
                yield prefix, ds[prefix], data_op


class TabularDD(DataDescriptor):
    pass
