'''Tests for DatasetConfig and DataseConfigFactory'''
# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from pathlib import Path
from typing import Any, Optional

import pytest

from ...catalog.catalog import CatalogLookupError
from ...problem_def.config_component import ValidationErrors
from ...wrangler.dataset import Dataset, RoleName
from ..local import LocalDatasetConfig
from .dataset_format_catalog import DatasetFormatCatalogAuto
from .dataset_config import DatasetConfig, DatasetFileError

# pylint: disable=missing-function-docstring,duplicate-code,missing-class-docstring


class FakeDatasetConfig(DatasetConfig):

    def load_train(self) -> Dataset:
        return Dataset(metadata=self.metadata)

    def load_test(self) -> Optional[Dataset]:
        return Dataset(metadata=self.metadata)

    def dataset(self, data: Any, **kwargs) -> Dataset:
        return Dataset(metadata=self.metadata)


def valid_csv(filename: Optional[str] = None) -> str:
    '''Returns a path (in the form of a string) to a valid csv file.'''
    module_path = Path(__file__).parents[3]
    path = module_path / 'examples' / 'classification' / (filename or 'credit.csv')
    return str(path)


SUNNY_DATASET_CONFIG = {
    'config': 'local',
}


def test_dataset_format_catalog_sunny_day():
    clause = SUNNY_DATASET_CONFIG.copy()
    clause['train_path'] = valid_csv()

    config = DatasetFormatCatalogAuto().build(clause=clause)
    assert isinstance(config, LocalDatasetConfig)


NOT_FOUND_DATASET_CONFIG = {
    'config': 'non-existent',
}


def test_config_factory_not_found():
    with pytest.raises(CatalogLookupError, match=r'non-existent'):
        _ = DatasetFormatCatalogAuto().build(clause=NOT_FOUND_DATASET_CONFIG)


def test_config_factory_default():
    clause = {}
    clause['train_path'] = valid_csv()
    config = DatasetFormatCatalogAuto().build(clause=clause)
    assert isinstance(config, LocalDatasetConfig)


SUNNY_DATASET = {
    'config': 'local',
    'column_roles': {
        'target': {
            'name': 'class'
        }
    }
}


def test_dataset_sunny_day():
    clause = SUNNY_DATASET.copy()
    clause['train_path'] = valid_csv()

    config = DatasetFormatCatalogAuto().build(clause=clause)
    assert len(config.roles[RoleName.ATTRIBUTE]) == 20


TRAIN_PATH_MISSING = {
    'config': 'local'
}


def test_train_path_missing():
    with pytest.raises(KeyError, match=r'[Tt]rain'):
        _ = DatasetFormatCatalogAuto().build(clause=TRAIN_PATH_MISSING)


TRAIN_FILE_MISSING = {
    'config': 'local',
    'train_path': '/tmp/path/to/nonexistent_file.csv'
}


def test_train_file_missing():
    with pytest.raises(DatasetFileError, match=r'nonexistent'):
        _ = DatasetFormatCatalogAuto().build(clause=TRAIN_FILE_MISSING)


ROLE_WITH_NO_COL = {
    'config': 'local',
    'column_roles': {
        'target': {}
    }
}


def test_role_with_no_col():
    clause = ROLE_WITH_NO_COL.copy()
    clause['train_path'] = valid_csv()

    with pytest.raises(ValidationErrors, match=r'[Nn]ame'):
        DatasetFormatCatalogAuto().build(clause=clause).validate()


INVALID_KEY = {
    'config': 'local',
    'hamster': {
        'gerbil': 'gerbil',
    },
    'column_roles': {
        'target': {
            'name': 'class'
        },
        'index': {
            'id': 0
        }
    }
}


def test_dataset_invalid_key() -> None:
    clause = INVALID_KEY.copy()
    clause['train_path'] = valid_csv()

    dut = DatasetFormatCatalogAuto().build(clause=clause)

    with pytest.raises(ValidationErrors, match='hamster'):
        dut.validate()


POS_LABEL_DATASET = {
    'column_roles': {
        'target': {
            'name': 'a',
            'pos_label': 'good'
        }
    }
}


def test_pos_label_sunny_day() -> None:
    dut = FakeDatasetConfig(POS_LABEL_DATASET)
    assert 'good' == dut.load_train().metadata.pos_labels[RoleName.TARGET]


def test_pos_label_missing() -> None:
    clause = {
        'column_roles': {
            'target': {
                'name': 'class'
            }
        }
    }

    dut = FakeDatasetConfig(clause=clause)
    assert dut.pos_label(RoleName.TARGET) is None
