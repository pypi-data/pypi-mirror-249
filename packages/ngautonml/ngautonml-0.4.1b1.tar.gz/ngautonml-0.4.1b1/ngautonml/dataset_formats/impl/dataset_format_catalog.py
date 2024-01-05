'''Catalog and autoloader for dataset input formats'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import abc
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

from .dataset_config import DatasetConfig
from ...catalog.catalog_element_mixin import CatalogElementMixin
from ...catalog.memory_catalog import MemoryCatalog
from ...catalog.plugin_catalog import PluginCatalog


class DatasetFormat(CatalogElementMixin, metaclass=abc.ABCMeta):
    '''Represents a way of reading data into the system.'''
    _builder: Type[DatasetConfig]

    def build(self, clause: Dict[str, Any],
              parents: Optional[List[str]] = None,
              **kwargs) -> DatasetConfig:
        '''Build a dataset config using this class's data format.'''
        return self._builder(clause=clause, parents=parents, **kwargs)


class DatasetFormatCatalog(MemoryCatalog[DatasetFormat], metaclass=abc.ABCMeta):
    '''Base class for dataset config catalogs'''

    def build(self, clause: Dict[str, Any], **kwargs) -> DatasetConfig:
        '''Resolve a dataset config clause to a DatasetConfig.

        This does a catalog lookup for the name in the clause. The lookup
        defaults to 'local'.
        '''
        config = clause.get('config', 'local')
        dataset_format: DatasetFormat = self.lookup_by_name(config)
        return dataset_format.build(clause=clause, **kwargs)


class DatasetFormatCatalogAuto(PluginCatalog[DatasetFormat], DatasetFormatCatalog):
    '''Dataset format catalog that automatically loads all dataset formats from a directory.

    Formats are located in ../dataset_formats.
    '''

    def __init__(self, **kwargs):
        super().__init__(
            catalog_name='dataset_formats',
            default_root=Path(__file__).parents[2], **kwargs)
