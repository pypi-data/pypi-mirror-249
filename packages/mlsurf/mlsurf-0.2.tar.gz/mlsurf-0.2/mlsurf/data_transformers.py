from abc import ABCMeta, abstractmethod
from collections import defaultdict


class DataTransformer(metaclass=ABCMeta):
    @abstractmethod
    def transform(self, dataset: dict, dd):
        """The data descriptor should be injected into this function
        during transformation.
        TODO: figure out a way to do strong typing of the dd param w/out
        circular import."""
        pass


class TabularDataTransformer(DataTransformer):
    def transform(self, dataset: dict, dd, params=None):
        if params is None:
            params = defaultdict(lambda: {})

        for prefix, data, data_op in dd.get_data_with_data_ops():
            if 'columns' in data:
                for col in data['columns']:
                    if col.conv is None:
                        continue

                    # get index in extracted data
                    idx = data['columns'].index(col)

                    # transformation function
                    conv = col.conv

                    if type(conv) in (list, tuple):
                        conv_funcs = conv
                    else:
                        conv_funcs = (conv,)

                    conv_params = []
                    for i, func in enumerate(conv_funcs):
                        if col.name in params:
                            func_params = params[col.name][i]
                        else:
                            func_params = None
                        dataset[prefix]['data'], func_params = func(data, idx, params=func_params)
                        conv_params.append(func_params)
                    
                    params[prefix][col.name] = conv_params
        
        return params

    def normalise_cols(self, dataset: dict):
        # TODO: move the `transform` logic here in v2.
        pass

    def derive_cols(self, dataset: dict):
        # TODO: see class diagram (with FeatureDeriver)
        pass
