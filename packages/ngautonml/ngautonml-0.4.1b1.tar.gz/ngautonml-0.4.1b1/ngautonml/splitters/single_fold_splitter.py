'''Splitter that does random sampling.'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from ..problem_def.cross_validation_config import CrossValidationConfig
from ..wrangler.dataset import Dataset
from ..wrangler.constants import Defaults

from .impl.splitter import Splitter, SplitterCatalog, SplitDataset, Fold


class SingleFoldSplitter(Splitter):
    '''Splitter that randomly splits data into one fold.

    It produces a single internal-train set and internal-validation set,
    according to the fraction "train_frac".
    '''
    _name = 'single_fold'
    _hyperparams = {
        'train_frac': Defaults.SPLIT_FRACTION
    }

    def split(self, dataset: Dataset, **overrides) -> SplitDataset:
        '''Split dataset into train and validation sets.

        We use pandas.DataFrame.sample to extract dataset_config.split_fraction
        as the 'train' dataset, and the rest as the 'validate' dataset.

        If there is a target role in the dataset, that column is removed from
        the 'validate' dataset and put in the 'ground_truth' dataset.
        '''
        train = dataset.output()
        validate = dataset.output()
        ground_truth = dataset.output()

        hyperparams = self.hyperparams(**overrides)
        train_frac = hyperparams['train_frac']

        data_df = dataset.get_dataframe()
        train_df = data_df.sample(frac=train_frac, random_state=self._cv_config.seed)
        validate_df = data_df.drop(train_df.index)

        if dataset.metadata.target is not None:
            assert dataset.metadata.target.name is not None
            ground_truth_df = validate_df[[str(dataset.metadata.target.name)]]
            ground_truth.ground_truth = ground_truth_df

            validate_df_no_target = validate_df.drop(dataset.metadata.target.name, axis=1)
        else:
            validate_df_no_target = validate_df

        train.dataframe = train_df
        validate.dataframe = validate_df_no_target

        return SplitDataset([Fold(train=train, validate=validate, ground_truth=ground_truth)])


def register(catalog: SplitterCatalog, *args, cv_config: CrossValidationConfig, **kwargs):
    '''Register all the objects in this file.'''
    catalog.register(SingleFoldSplitter(*args, cv_config=cv_config, **kwargs))
