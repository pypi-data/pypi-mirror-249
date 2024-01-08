from abc import ABCMeta, abstractmethod
import gc

from mlsurf.data_descriptors import DataDescriptor, TabularDD
from mlsurf.data_generator import DataGenerator
from mlsurf.data_splitting import SplitterInterface


class DatasetSource(DataGenerator, metaclass=ABCMeta):
    """TODO: maybe provide which prefixes we can expect to exist in these data sources, so verifications
             can be made as per user expectations when extracting, loading files, etc..."""
    def __init__(self, dd: DataDescriptor, name: str, input_path: str, datasets: list,
                 splitter: SplitterInterface):
        super(DatasetSource, self).__init__(dd)
        self.name = name
        self.input_path = input_path
        self.datasets = datasets
        self.splitter = splitter

        self._extracted_data = None

    @abstractmethod
    def extract(self):
        """Must extract data to self._extracted_data as a dict in the form:
        {'prefix': data_obj, ...}"""
        pass

    def save_extracted(self):
        for prefix, data_obj in self._extracted_data:
            data_op = self.dd.get_data_operator(prefix)
            data_op.save(data_obj, self.dd.data_dir, f"{prefix}_{self.name}",
                         make_extension=True)

    def load_extracted(self):
        # init data dict
        self._extracted_data = {}

        # load data
        for prefix, data_op in self.dd.get_prefixes_with_data_ops():
            try:
                self._extracted_data[prefix] = \
                    data_op.load(self.dd.data_dir, f"{prefix}_{self.name}", make_extension=True)
            except FileNotFoundError:
                continue

    def create_datasets(self):
        # split self.data based on the ratios
        # need that ratio splitting function
        shares = [ds['share'] for ds in self.datasets]
        data_len = self.get_data_len(self._extracted_data)
        split_idxs = self.splitter.get_split_idxs(self._extracted_data, data_len, shares)

        # init datasets' data
        for ds in self.datasets:
            ds['data'] = {}

        for prefix, data_obj, data_op in self.get_data_with_data_ops(self._extracted_data):
            for i, ds in enumerate(self.datasets):
                ds['data'][prefix] = data_op.filter(data_obj, split_idxs[i])

            # we don't need the extracted data in this prefix now, so free memory
            self._extracted_data[prefix] = None
            gc.collect()

    def get_dataset(self, name):
        return next(ds for ds in self.datasets if ds['name'] == name)

    def get_all_datasets(self):
        return self.datasets
    
    def remove_dataset(self, name):
        for ds in self.datasets:
            if ds['name'] == name:
                self.datasets.remove(ds)
                break

    def save_datasets(self):
        for ds in self.datasets:
            name = ds['name']
            for prefix, data_obj in ds['data']:
                data_operator = self.dd.get_data_operator(prefix)
                data_operator.save(data_obj, self.dd.data_dir, f"{prefix}_{name}",
                                   make_extension=True)

    def load_datasets(self):
        # init datasets' data
        for ds in self.get_all_datasets():
            ds['data'] = {}

        # load
        for prefix, data_op in self.get_prefixes_with_data_ops():
            for ds in self.datasets:
                name = ds['name']
                try:
                    data_op.load(self.dd.data_dir, f"{prefix}_{name}", make_extension=True)
                except FileNotFoundError:
                    continue


class Col:
    def __init__(self, pos: int, name: str = None, dtype=None, conv: callable = None):
        """
        Initialize a new column configuration.

        This class represents a column in a tabular data structure, allowing for 
        customization of data handling and processing.

        :param pos: The position of the column in the raw tabular data source.
        :type pos: int
        :param name: The name assigned to the column, optional. Useful for reference, 
                     especially during operations on derived columns.
        :type name: str, optional
        :param dtype: The expected data type for the column. Depends on the prefix's type.
        :param conv: A function for transforming or normalizing the column data, optional.
        :type conv: callable, optional
        """
        self.pos = pos
        self.name = name
        self.dtype = dtype
        self.conv = conv
