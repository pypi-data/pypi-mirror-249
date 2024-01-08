from multiprocessing import Pool

from enums import ProcessingStage


class DataPreprocessor:
    def __init__(self, pool_size=1, create_datasets_online=False, transform_online=False,
                 extract_online=True, parallel: bool = False, reduce_mem=False,
                 offline_stage=ProcessingStage.CREATE_DATASETS):
        self.pool_size = pool_size
        self.create_datasets_online = create_datasets_online
        self.transform_online = transform_online
        self.extract_online = extract_online
        self.parallel = parallel
        self.reduce_mem = reduce_mem
        self.offline_stage = offline_stage

    def extract(self, data_gen):
        """Override this function to implement extra functionality around extraction."""
        data_gen.extract()

    def save_extracted(self, data_gen):
        """Override this function to implement extra functionality around extraced data saving."""
        data_gen.save_extracted()
        # TODO: clear_extracted()?

    def load_extracted(self, data_gen):
        """Override this function to implement extra functionality around extracted data loading."""
        data_gen.load_extracted()

    def create_datasets(self, data_gen):
        """Override this function to implement extra functionality around dataset creation."""
        data_gen.create_datasets()

    def save_datasets(self, data_gen):
        """Override this function to implement extra functionality around dataset saving."""
        data_gen.save_datasets()
        # TODO: clear_datasets()?

    def load_datasets(self, data_gen):
        """Override this function to implement extra functionality around dataset loading."""
        data_gen.load_datasets()

    def transform(self, data_gen):
        """Override this function to implement extra functionality around data transformation."""
        data_gen.transform()

    def execute_stage(self, func: callable, data_gen, online: bool, processing_stage: ProcessingStage):
        """Returns a boolean indicating if this is the last stage in offline mode."""
        if not online and self.offline_stage >= processing_stage or \
                online and self.offline_stage < processing_stage:
            func(self, data_gen, online)

            if not online and processing_stage == self.offline_stage:
                return True

        return False

    def preprocess(self, data_gen, online: bool = True):
        # TODO: make this a bit more modular, i.e., find a way to put the save_extracted logic into the
        #       extract function, so we can simply list functions to be executed here.
        # extract
        save_data = self.execute_stage(self.extract, data_gen, online, ProcessingStage.EXTRACT)
        if save_data:
            self.save_extracted(data_gen)

        # create datasets
        save_data = self.execute_stage(self.create_datasets, data_gen, online,
                                       ProcessingStage.CREATE_DATASETS)
        if save_data:
            self.save_datasets(data_gen)

        # transform
        self.execute_stage(self.transform, data_gen, online, ProcessingStage.TRANSFORM)
        if not online:
            self.save_datasets(data_gen)

    def preprocess_multi(self, data_gen_list: iter, online: bool = True):
        if self.parallel:
            with Pool(self.pool_size) as pool:
                pool.map(lambda data_gen: self.preprocess(data_gen, online=online), data_gen_list)
                # pool.map is a blocking call, it will wait until all processes are completed
        else:
            for data_gen in data_gen_list:
                self.preprocess(data_gen, online=online)
