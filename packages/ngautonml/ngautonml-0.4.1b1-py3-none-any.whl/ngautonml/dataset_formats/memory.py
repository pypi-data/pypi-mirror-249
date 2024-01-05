'''Holds information about an in-memory dataset'''
from typing import Dict, Any, Optional, List

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import pandas as pd

from .impl.dataframe_dataset_config import DataframeDatasetConfig
from .impl.dataset_config import DatasetConfigError
from .impl.dataset_format_catalog import DatasetFormat, DatasetFormatCatalog
from ..wrangler.dataset import Dataset
from ..problem_def.task import Task


class MemoryDatasetConfig(DataframeDatasetConfig):
    ''' Holds information about an in-memory dataset '''

    # pylint: disable=too-many-arguments
    def __init__(self,
                 clause: Dict[str, Any],
                 train_df: Optional[pd.DataFrame] = None,
                 test_df: Optional[pd.DataFrame] = None,
                 parents: Optional[List[str]] = None,
                 task: Optional[Task] = None):
        super().__init__(clause, parents, task)
        if train_df is None:
            raise DatasetConfigError(
                'Attempt to create a memory dataset config, but train dataframe is not provided.'
            )
        self.train_df = train_df
        self.test_df = test_df
        self._train_cols = train_df.head(0)
        self._read_roles()

    def load_train(self) -> Dataset:
        retval = Dataset(metadata=self.metadata)
        retval.dataframe = self.train_df

        return retval

    def load_test(self) -> Optional[Dataset]:
        if self.test_df is None:
            return None

        retval = Dataset(metadata=self.metadata)
        retval.dataframe = self.test_df

        return self._prune_target(retval)


class MemoryDatasetFormat(DatasetFormat):
    '''Used to load a local tabular dataset.'''
    _builder = MemoryDatasetConfig
    _name = 'memory'
    _tags = {}


def register(catalog: DatasetFormatCatalog, *args, **kwargs):
    '''Register all the objects in this file.'''
    catalog.register(MemoryDatasetFormat(*args, **kwargs))
