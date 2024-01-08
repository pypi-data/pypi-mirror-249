from abc import ABCMeta, abstractmethod
from collections import defaultdict
import gc

import numpy as np


class DataFolder(metaclass=ABCMeta):
    def __init__(self):
        self.num_iters = None
        self.gen = None

    def init_fold_pool(self, gen, pool_ds):
        """This function will initialise the folding pool. The folding pool
        is the data from which the data folds are sourced from."""
        if 'num_iters' in pool_ds:
            self.num_iters = pool_ds['num_iters']
        # else let subclass decide

        self.gen = gen

    @abstractmethod
    def get_dataset(self, name):
        pass

    @abstractmethod
    def get_all_datasets(self):
        pass

    @abstractmethod
    def next_fold(self, fold_num):
        """Re-load fold datasets based on the fold number. It is expected for the subclass to
        Override this function, and can optionally call into this function before applying
        new logic."""
        if fold_num >= self.num_iters:
            raise IndexError("Fold number is more than the number "
                             "iterations specified for this data folder.")

    def get_folds_num(self):
        return self.num_iters

    def all_folds(self):
        """The current idea is is to iterate like `while gen.next_fold()`;
        The `next_fold` function doesn't return/yield anything, instead it
        raises a StopIteration when we're done. This may change in the future
        so we're not removing this so to preserve ideas / original intentions."""
        for fold_num in range(1, self.num_iters+1):
            yield self.next_fold(fold_num)


class KFoldTrainVal(DataFolder):
    """Standard K Fold cross validation folding scheme, with only train/val split.
    To use this, set `dataset['fold_mode'] = 'k_fold'`.
    The to specify the train and validation set details, do:
    dataset['train'] = ...
    dataset['val'] = ...
    where the values are standard dataset dictionaries. The datasets will be processed
    in the order that they are specified, i.e., if 'val' key is specified after 'train' key,
    then dataset['train']['share'] cannot be None. Only the last one can use None
    for the share."""
    def __init__(self):
        super().__init__()

        # will be initiated during `init_fold_pool`
        self.n = None
        self.fname_fold_prefix = None
        self.pool_ds = None
        self.train_ds = None
        self.val_ds = None
        self.fold_pool = None
        self.pool_data_len = None
        self.splitter = None

    def init_fold_pool(self, gen, pool_ds):
        super(KFoldTrainVal, self).init_fold_pool(gen, pool_ds)

        if 'num_iters' not in pool_ds:
            self.num_iters = pool_ds['N']

        self.n = pool_ds['N']

        self.fname_fold_prefix = pool_ds['fold_prefix']

        fold_datasets = pool_ds['datasets']
        if len(fold_datasets) != 2:
            raise "There must be 2 fold datasets with 'k_fold' fold mode; train and val."

        self.train_ds = fold_datasets['train']
        self.val_ds = fold_datasets['val']

        # track original names
        self.set_up_orig_names(self.train_ds, self.val_ds)

        self.pool_ds = pool_ds

        # This will contain the pool_ds split up into n folds. Each fold will
        # have the corresponding fold number keyed for it.
        self.fold_pool = defaultdict(lambda: {})

        self.pool_data_len = gen.get_data_len(pool_ds)

        # shuffle the fold pool if specified
        if pool_ds['shuffle'] is True:
            shuf_idxs = np.arange(self.pool_data_len)
            np.random.shuffle(shuf_idxs)
            for prefix, data_op, data_obj in gen.get_prefixes_with_data_ops(pool_ds['data']):
                pool_ds['data'][prefix] = data_op.rearrange(data_obj, shuf_idxs)

        # initialise the fold blocks
        self.splitter = pool_ds['splitter']  # should already be an instantiated object

        shares = [1.0/self.n for _ in range(self.n - 1)]
        shares.append(None)

        split_idxs = self.splitter.get_split_idxs(pool_ds['data'],
                                                  self.pool_data_len, shares)

        for prefix, data_obj, data_op in gen.get_data_with_data_ops(pool_ds['data']):
            for i in range(self.n):
                self.fold_pool[i][prefix] = data_op.filter(data_obj, split_idxs[i])

            # we don't need the extracted data in this prefix now, so free memory
            pool_ds['data'][prefix] = None
            gc.collect()

    def next_fold(self, fold_num):
        super().next_fold(fold_num)
        # validation dataset is retrieved by using the respective fold for the
        # fold num we're currently at
        self.val_ds['data'] = self.fold_pool[fold_num]

        # train dataset will concatenate the rest of the data in the fold pool
        other_folds = [data for i, data in self.fold_pool.items() if i != fold_num]
        for prefix, data_op in self.gen.get_prefixes_with_data_ops(self.pool_ds['data']):
            self.train_ds['data'] = data_op.concatenate(*other_folds)

        # change the names of the datasets to reflect fold number
        self.update_ds_names(self.train_ds, self.val_ds, fold_prefix=self.fname_fold_prefix,
                             fold_num=fold_num)

        # return [self.train_ds, self.val_ds]

    @staticmethod
    def set_up_orig_names(*fold_datasets):
        for fds in fold_datasets:
            fds['orig_name'] = fds['name']

    @staticmethod
    def update_ds_names(*fold_datasets, fold_prefix='', fold_num=0):
        """Assumes the original name is in the 'orig_name' key for each fold ds.
        The idea is that the `set_up_orig_names` func is called to set things up correctly."""
        for fds in fold_datasets:
            fds['name'] = f"{fds['orig_name']}_{fold_prefix}{fold_num}"

    def get_dataset(self, name, fold_ds=None, fold_num=None):
        """For now, we only return fold datasets if they're actually initialised,
        which is simlar to what the group wrapper does. This means an error is
        thrown if we try to get a fold dataset before `create_datasets` is called,
        even if the fold dataset name is correct."""
        # TODO: make this code more concise (should be able to do it with a single loop)
        if fold_num is None:
            name_key = 'name'
            match_string = f"{name}_{self.fname_fold_prefix}{fold_num}"
        else:
            name_key = 'orig_name'
            match_string = name

        if fold_ds is None:
            train_ds, val_ds = self.train_ds, self.val_ds
        else:
            train_ds, val_ds = fold_ds['train'], fold_ds['val']

        for ds in (train_ds, val_ds):
            if ds[name_key] == match_string:
                return ds

    def get_all_datasets(self, fold_ds=None):
        datasets = []
        if fold_ds is None:
            if self.train_ds is not None:
                datasets.append(self.train_ds)
            if self.val_ds is not None:
                datasets.append(self.val_ds)
        else:
            datasets.append(fold_ds['train'])
            datasets.append(fold_ds['val'])
        return datasets
