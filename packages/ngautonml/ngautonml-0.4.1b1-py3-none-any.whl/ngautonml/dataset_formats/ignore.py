'''Stub dataset config for tests.'''

from typing import Any, Optional

import pandas as pd

from ..wrangler.dataset import Dataset, DatasetKeys
from .impl.dataset_config import DatasetConfig
from .impl.dataset_format_catalog import DatasetFormat, DatasetFormatCatalog


class StubDatasetConfig(DatasetConfig):
    '''Stub dataset used in testing.'''

    def load_train(self) -> Dataset:
        '''Load a stub dataset'''
        return Dataset(metadata=self.metadata, **{DatasetKeys.DATAFRAME.value: pd.DataFrame()})

    def load_test(self) -> Optional[Dataset]:
        '''Load test data if it exists, otherwise None'''
        return None

    def dataset(self, data: Any, **kwargs) -> Dataset:
        return Dataset(metadata=self.metadata, **{DatasetKeys.DATAFRAME.value: pd.DataFrame()})


class StubFormat(DatasetFormat):
    '''Stub dataset format used in testing.'''
    _builder = StubDatasetConfig
    _name = 'ignore'


def register(catalog: DatasetFormatCatalog, *args, **kwargs):
    '''Register all the objects in this file.'''
    catalog.register(StubFormat(*args, **kwargs))
