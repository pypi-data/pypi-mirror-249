from abc import ABCMeta, abstractmethod
from collections import defaultdict
import gc

from mlsurf.data_descriptors import DataDescriptor
from mlsurf.data_util import topological_sort


class DataGenerator(metaclass=ABCMeta):
    """Generic Data Generator. The preprocessor uses objects instantiated from concrete subclasses of
    this class to create datasets."""
    def __init__(self, dd: DataDescriptor):
        self.dd = dd

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def save_extracted(self):
        pass

    @abstractmethod
    def load_extracted(self):
        pass

    @abstractmethod
    def create_datasets(self):
        pass

    @abstractmethod
    def save_datasets(self):
        pass

    @abstractmethod
    def load_datasets(self):
        pass

    @abstractmethod
    def get_dataset(self, name):
        """Return None if it doesn't exist."""
        pass

    @abstractmethod
    def get_all_datasets(self):
        """Return an empty list if there are none."""
        pass

    def get_datasets(self, *names):
        """Return an empty list if there are none."""
        if len(names) == 0:
            return self.get_all_datasets()
        return [self.get_dataset(name) for name in names]

    def clear_datasets(self, *names):
        if len(names) == 0:
            for ds in self.get_all_datasets():
                ds['data'] = None
        else:
            for ds in [d for d in self.get_all_datasets() if d['name'] in names]:
                ds['data'] = None

    @abstractmethod
    def remove_dataset(self, name):
        raise NotImplementedError()

    def remove_datasets(self, *names):
        for name in names:
            self.remove_dataset(name)

    def transform(self, datasets=None):
        """Typical implementation is to directly use the transformer on each dataset, with no
        extra logic. Override this for more intricate logic, such as dealing with cross dependencies
        between datasets, or even datasets from different data generators."""
        if datasets is None:
            datasets = self.get_all_datasets()
        transformer = self.dd.get_transformer()
        for ds in datasets:
            transformer.transform(ds)

    def get_dependents(self, *datasets):
        return {}

    def get_data_len(self, data):
        p, d = next(iter(data.items()))
        data_op = self.dd.get_data_operator(p)
        data_len = data_op.get_len(d)

        # data length must be the same
        # TODO: separate this functionality - this check should be orchestrated outside
        #       this function
        assert all([data_op.get_len(data_obj) == data_len
                    for data_obj in [v for v in data.values()][1:]])

        return data_len


class DataGeneratorNode(DataGenerator):
    def __init__(self, dd: DataDescriptor, generators: list,
                 extract_parallel: bool = False, create_datasets_parallel: bool = False,
                 transform_parallel: bool = False):
        super().__init__(dd)

        self.generators = generators

        self.extract_parallel = extract_parallel
        self.create_datasets_parallel = create_datasets_parallel
        self.transform_parallel = transform_parallel

    def extract(self):
        for gen in self.generators:
            gen.extract()

    def save_extracted(self):
        for gen in self.generators:
            gen.save_extracted()

    def load_extracted(self):
        for gen in self.generators:
            gen.load_extracted()

    def create_datasets(self):
        for gen in self.generators:
            gen.create_datasets()

    def save_datasets(self):
        for gen in self.generators:
            gen.save_datasets()

    def load_datasets(self):
        for gen in self.generators:
            gen.load_datasets()

    def get_dataset(self, name):
        for gen in self.generators:
            ds = gen.get_dataset(name)
            if ds is not None:
                return ds

    def get_all_datasets(self):
        """Return an empty list if there are none."""
        return [ds for gen in self.generators for ds in gen.get_all_datasets()]

    def remove_dataset(self, name):
        for gen in self.generators:
            gen.remove_dataset(name)

    def remove_datasets(self, *names):
        for name in names:
            self.remove_dataset(name)

    def transform(self):
        transformer = self.dd.get_transformer()
        for ds in self.get_all_datasets():
            transformer.transform(ds)


class DatasetGroupingWrapper(DataGeneratorNode):
    def __init__(self, groups: list, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If no action is specified in the group dicts, then 'join' action is assumed.
        for grp in groups:
            if 'action' not in grp:
                grp['action'] = 'copy'

        # Group criteria.
        # This will look similar to the self.datasets in DataSource class, but no 'share' keys
        # for convenience we turn it into a dict where the dataset name is the key.
        self.groups = {grp['name']: grp for grp in groups}

        self.group_datasets = {}

    def filter_groups(self, action=None):
        filtered_groups = self.groups.copy()

        if action is not None:
            filtered_groups = {k: v for k, v in filtered_groups if v['action'] == action}

        return filtered_groups

    def create_datasets(self):
        super(DatasetGroupingWrapper, self).create_datasets()
        self.copy_datasets()

    def copy_datasets(self):
        """To use the copy action, `'action': 'copy'` must be specified in the group dictionary,
        and `'from': list(datasets)` & `'to': dataset` keys should be specified. If there's no 'to' key
        in the group dict then a new group dataset is created using the 'name' key.

        `'remove': True` will instruct the old datasets to be removed after copying them over to another
        dataset. This means that any kwargs required for subsequent preprocessing steps (e.g., transformation)
        will need to be written in the group dict (unlike if 'to' key is specified, in which case said kwargs
        should be written in the destination dataset's dictionary. The datasets specified in the from or to may
        be normal datasets as configured in thedata sources, or joined group datasets as configured for the
        'join' action."""

        copy_groups = self.filter_groups(action='copy')
        for grp_name, grp in copy_groups.items():
            # 1) get from and to datasets
            from_datasets = grp['from'] if isinstance(grp['from'], list) or isinstance(grp['from'], tuple) \
                else [grp['from']]
            if 'to' in grp:
                to_ds = self.get_dataset(grp['to'])
            else:
                self.group_datasets[grp_name] = {**grp, 'data': {}}
                to_ds = self.group_datasets[grp_name]

            # 2) copy data from `from_datasets` to `to_ds`
            for prefix, data_op in self.dd.get_prefixes_with_data_ops():
                # It's not a requirement for datasets in a group to have the same prefixes.
                # We concatenate only the intersecting prefixes.
                if all(prefix in ds for ds in from_datasets):
                    to_ds['data'][prefix] = data_op.concatenate(ds['data'][prefix] for ds in from_datasets)

            # 3) remove `from_datasets` if so specified
            if 'remove' in grp:
                self.remove_datasets(from_datasets)
                gc.collect()

    def get_dataset(self, name):
        if name in self.group_datasets:
            return self.group_datasets[name]
        return super(DatasetGroupingWrapper, self).get_dataset(name)

    def get_all_datasets(self):
        datasets = [ds for gen in self.generators for ds in gen.get_all_datasets()
                    if ds['name'] not in self.group_datasets]
        datasets.extend(self.group_datasets.values())
        return datasets

    def save_datasets(self):
        # save dataset groups
        for name, grp in self.group_datasets.items():
            for prefix, data_obj in grp['data'].items():
                data_operator = self.dd.get_data_operator(prefix)
                data_operator.save(data_obj, self.dd.data_dir, f"{prefix}_{name}",
                                   make_extension=True)

        # save datasets not grouped
        super(DatasetGroupingWrapper, self).save_datasets()


class DatasetDependencyMixin:
    """General dataset dependency management."""
    def build_dataset_dependency_map(self, dependency_key, datasets=None):
        if datasets is None:
            datasets = self.get_all_datasets()
        dep_map = defaultdict(lambda: list())
        for ds in datasets:
            dep_map[ds[dependency_key]].append(ds)
        return dep_map

    @staticmethod
    def verify_dataset_dependency_map(dep_map):
        """TODO: check for circular dependencies, possibly among other things..."""
        pass

    def get_dependent_datasets(self, ds, dependency_key=None, dependency_map=None):
        if dependency_map is None:
            if dependency_key is None:
                raise "both dependency_key and dependency_map cannot be None at the same time"
            dependency_map = self.build_dataset_dependency_map(dependency_key)
        dependents = []
        if ds['name'] in dependency_map:
            dependents = dependency_map[ds['name']]
            for dep in dependents:
                dependents.extend(self.get_dependent_datasets(dep, dependency_map))
        return list(set(dependents))


class TransformerDependencyMixin(DatasetDependencyMixin):
    def __init__(self):
        self.trans_params_map = {}

        # This dependency map will help us to save only the trans params that we need
        self.trans_dependency_map = self.build_dataset_dependency_map('params_from')

    def transform(self, datasets=None):
        """TODO: figure out what to do when dependencies aren't"""
        if datasets is None:
            datasets = self.get_all_datasets()

        # Create group dictionary, keyed with group name (taken from 'trans_grp' key), and
        # values with list of respective datasets in that group.
        # These groups are intended to be transformed together, then split apart again after the
        # transformation.
        trans_groups = self.build_dataset_dependency_map('trans_grp', datasets=datasets)

        trans_groups_list = [e for lst in trans_groups.values() for e in lst]

        independent_jobs = []
        for ds in datasets:
            if ds['name'] not in trans_groups_list:
                independent_jobs.append(ds)

        trans_jobs = []

        for grp_name, datasets in trans_groups.items():
            # check all datasets have the same prefixes
            prefixes = [key for key in datasets[0].keys()]
            assert all([set(ds) == set(prefixes) for ds in datasets[1:]])

            # We assume all prefixes are the same length, so the first prefix will act as the
            # model for split indexes.
            first_pref = prefixes[0]
            data_op = self.dd.get_data_operator(first_pref)
            split_indexes = [data_op.get_len(ds['data'][first_pref]) for ds in datasets]

            # create the transformation job dict for this group
            grp_dict = {'name': grp_name, 'group': True,
                        'split_indexes': split_indexes, 'data': {}}

            # combine the grouped datasets
            for prefix in prefixes:
                data_op = self.dd.get_data_operator(prefix)
                grp_dict['data'][prefix] = data_op.concatenate([ds[prefix] for ds in datasets])

                # free memory temporarily
                for ds in datasets:
                    ds['data'][prefix] = None
                gc.collect()

            trans_jobs.append(grp_dict)

        trans_jobs.extend(independent_jobs)

        trans_jobs = topological_sort(trans_jobs)

        transformer = self.dd.get_transformer()
        for job in trans_jobs:
            if 'params_from' in job:
                trans_params = self.trans_params_map[job['params_from']]
            else:
                trans_params = None
            trans_params = transformer.transform(job, params=trans_params)
            if job['name'] in self.trans_dependency_map and trans_params is not None:
                self.trans_params_map[job['name']] = trans_params

        # split out the grouped datasets and move back to their original individual dataset
        # dictionaries
        for job in trans_jobs:
            if 'group' in job and job['group'] is True:
                for prefix in job['data']:
                    data_op = self.dd.get_data_operator(prefix)
                    lower_idx = 0
                    for ds, upper_idx in zip(trans_groups[job['name']], job['split_indexes']):
                        ds['data'][prefix] = data_op.get_slice(job['data'][prefix],
                                                               lower_idx, upper_idx)
                        lower_idx = upper_idx

                    # free memory
                    job['data'][prefix] = None
                gc.collect()

    def get_trans_params(self, param):
        pass


class FoldWrapper(DatasetDependencyMixin):
    """When using this wrapper, there is a second phase to dataset creation.
    This second phase will check for datasets that are described as "data folders",
    and such datasets effectively act as folding pools, from which folds of data
    will be created (as in cross validation). The actual folding logic will be
    defined in these data folders which inherit from the DataFolder base class and
    implement the interface `init_fold_pool` and `next_pool`.

    This wrapper can be used either as the first superclass in a new class definition,
    as in `class NewClass(FoldWrapper, DataGeneratorSubClass)` or it can directly
    wrap a generator class instance as in
    `wrapper = FoldWrapper(dataGeneratorSubClassInstance)`.
    TODO: If this is to be used as a wrapper, we need to make it implement the DataGenerator
          interface. In this case, the non-wrapped functions will be as simple as the
          first 4 lines of code in `create_datasets`.

    For now this wrapper is only intended to work with one data folding pool among
    data generator tree with which it is connected. It is also assumed that there's no
    datasets are dependence on the fold datasets at the `create_datasets` level."""
    def __init__(self, gen: DataGenerator = None):
        self.gen: DataGenerator = gen
        self.fold_nums_dict = defaultdict(lambda: 0)
        self.fold_pools = defaultdict(lambda: {})
        self.orig_dep_data = defaultdict(lambda: {})
        self.non_dep_set: list = None

        # are we in trans online or trans offline mode?
        self.trans_online = True

    def create_datasets(self):
        # standard phase of dataset creation
        if self.gen is None:
            super().create_datasets()
            gen = self
        else:
            self.gen.create_datasets()
            gen = self.gen

        # initialise folding pools for any datasets that are declared as such
        if self.gen is None:
            datasets = super().get_all_datasets()
        else:
            datasets = self.gen.get_all_datasets()
        for ds in datasets:
            if 'data_folder' in ds:
                folder = ds['data_folder']
                folder.init_fold_pool(gen, ds)
                self.fold_pools[ds['name']] = ds
                self.fold_pools[ds['name']]['trans_dependents'] = \
                    self.get_dependent_datasets(ds, dependency_key='params_from')

                for dep_ds in self.fold_pools[ds['name']]['trans_dependents']:
                    for prefix, data_obj, data_op in gen.get_data_with_data_ops(dep_ds['data']):
                        self.orig_dep_data[dep_ds['name']][prefix] = data_op.copy(data_obj)

    def get_dataset(self, name, fold_num=None):
        """TODO: tidy up this function; what if self.fold_pools isn't initialised?"""
        for fold_ds in self.fold_pools.values():
            ds = fold_ds['data_folder'].get_dataset(name, fold_ds=fold_ds, fold_num=fold_num)
            if ds is not None:
                return ds

        if self.gen is None:
            return super().get_dataset(name)
        else:
            return self.gen.get_dataset(name)

    def get_all_datasets(self):
        if self.gen is None:
            datasets = super().get_all_datasets()
        else:
            datasets = self.gen.get_all_datasets()
        ds_list = []
        for ds in datasets:
            datasets.append(ds)
            if 'data_folder' in ds:
                ds_list.extend(ds['data_folder'].get_all_datasets(ds))
        ds_list.extend(datasets)
        return datasets

    def remove_dataset(self, name):
        pass

    def save_datasets(self):
        """It is assumed that `self.transform` has already been called."""
        if self.gen is None:
            gen = self
        else:
            gen = self.gen

        for non_dep_ds in self.non_dep_set:
            for prefix, data_obj, data_op in gen.get_data_with_data_ops(non_dep_ds['data']):
                data_op.save(data_obj, gen.dd.data_dir, f"{prefix}_{non_dep_ds['name']}")

        # for now this is only compatible with 1 folding pool
        _, fold_pool = next(iter(self.fold_pools.items()))
        while self.next_fold():
            data_folder = fold_pool['data_folder']
            datasets = [*fold_pool['trans_dependents'], *data_folder.get_all_datasets()]

            for ds in datasets:
                for prefix, data_obj, data_op in gen.get_data_with_data_ops(ds['data']):
                    data_op.save(data_obj, gen.dd.data_dir, f"{prefix}_{ds['name']}",
                                 make_extension=True)

    def load_datasets(self, datasets=None):
        """For now, this function is only compatible with being called when the saved
        datasets are all fully transformed, including all the fold datasets. However,
        we provide intended functionality anyway."""
        # get datasets to load
        datasets = self._get_all_datasets(datasets)

        # TODO: AT: just need to load non dep set first, and make sure we track the dep set so we can
        #       load them in `next` function iteratively
        for ds in datasets:
            if 'data_folder' in ds:
                folder = ds['data_folder']
                self.fold_pools[ds['name']] = ds
                self.fold_pools[ds['name']]['trans_dependents'] = \
                    self.get_dependent_datasets(ds, dependency_key='params_from')
                folder.set_up_orig_names(folder.get_all_datasets(ds), *self.fold_pools[ds['name']]['trans_dependents'])

        self._set_non_dep_set(datasets)

        self._load_datasets(self.non_dep_set)

        # if we're calling the load function it means the datasets are fully transformed
        # because for now that're the compatibility requirement.
        self.trans_online = False

    def _load_datasets(self, datasets=None):
        gen = self._get_gen()
        for ds in datasets:
            for prefix, data_obj, data_op in gen.get_data_with_data_ops(ds['data']):
                data_op.load(gen.dd.data_dir, f"{prefix}_{ds['name']}", make_extension=True)

    def next_fold(self, pool_name=None):
        """If no pool name given, it's assumed there's only 1 pool.
        Raises a StopIteration exception when we've exhausted the folds.
        This means we should use `while` to iterate with this, e.g.:
        ```
        while gen.next():
           datasets
        ```"""
        gen = self._get_gen()
        if pool_name is None:
            pool_name, fold_pool = next(iter(self.fold_pools.items()))
        else:
            fold_pool = self.fold_pools[pool_name]

        data_folder = fold_pool['data_folder']

        fold_num = self.fold_nums_dict[pool_name]

        if fold_num >= data_folder.num_iters:
            return False

        if self.trans_online:
            data_folder.next_fold(fold_num)

            # restore original data, and change dependent datasets' names to reflect fold num
            # FIXME: We shouldn't need to do this for the first iteration
            for dep_ds in fold_pool['trans_dependents']:
                for prefix, data_obj, data_op in gen.get_data_with_data_ops(
                        self.orig_dep_data[dep_ds['name']]):
                    dep_ds['data'][prefix] = data_op.copy(data_obj)
                    data_folder.update_ds_names(dep_ds, fold_prefix=fold_pool['fold_prefix'],
                                                fold_num=fold_num)

            # transform the dep set
            datasets_to_transform = [*fold_pool['trans_dependents'], *data_folder.get_all_datasets()]
            if self.gen is None:
                super().transform(datasets_to_transform)
            else:
                gen.transform(datasets_to_transform)
        else:
            datasets = [*data_folder.get_all_datasets(fold_pool=fold_pool), *fold_pool['trans_dependents']]
            self._load_datasets(datasets=datasets)

        self.fold_nums_dict[pool_name] += 1

        return True

    def _get_all_datasets(self, datasets=None):
        if datasets is None:
            if self.gen is None:
                datasets = super().get_all_datasets()
            else:
                datasets = self.gen.get_all_datasets()
        return datasets

    def _get_gen(self):
        if self.gen is None:
            gen = self
        else:
            gen = self.gen
        return gen

    def _set_non_dep_set(self, datasets=None):
        """This function assumes that the `trans_dependents` has been initialised
        in the folding pools."""
        datasets = self._get_all_datasets(datasets=datasets)

        # get all datasets that have transformer dependencies on the collective folding pools
        dep_set = []
        for fold_pool_name, fold_pool in self.fold_pools.items():
            dep_set.extend(fold_pool['trans_dependents'])
            dep_set.extend(fold_pool)

        # datasets that are neither directly nor indirectly dependent on the fold datasets
        # for transformation
        self.non_dep_set = [ds for ds in datasets if ds not in dep_set]

    def transform(self):
        # only transform the non-fold-ds-dependent datasets for now
        if self.gen is None:
            super().transform(self.non_dep_set)
        else:
            self.gen.transform(self.non_dep_set)
