'''Tests for LocalDatasetConfig'''
from pathlib import Path
from typing import Any, Dict, Optional
import os

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import pandas as pd
import pytest

from ..problem_def.problem_def import ValidationErrors
from ..problem_def.task import Task, TaskType
from ..wrangler.dataset import DatasetKeys, RoleName
from .local import LocalDatasetConfig


# pylint: disable=missing-function-docstring


def valid_csv(filename: Optional[str] = None) -> str:
    '''Returns a path (in the form of a string) to a valid csv file.'''
    current_path = str(os.getenv('PYTEST_CURRENT_TEST')).split('::', maxsplit=1)[0]
    pathobj = Path(current_path).resolve()
    module_parent = pathobj.parents[2]
    if filename is None:
        filename = 'credit.csv'
    path = module_parent / 'examples' / 'classification' / filename
    return str(path)


def valid_arff(filename: Optional[str] = None) -> str:
    '''Returns a path (in the form of a string) to a valid arff file.'''
    current_path = str(os.getenv('PYTEST_CURRENT_TEST')).split('::', maxsplit=1)[0]
    pathobj = Path(current_path).resolve()
    module_parent = pathobj.parents[2]
    if filename is None:
        filename = 'dataset_31_credit-g.arff'
    path = module_parent / 'examples' / 'classification' / filename
    return str(path)


def make_dataset(train_path: str) -> Dict[str, Any]:
    retval = {
        'config': 'local',
        'train_path': train_path,
        'column_roles': {
            'target': {
                'name': 'class',
                'pos_label': 'good'
            }
        }
    }
    return retval


def test_load_simple_dataset():
    clause = make_dataset(valid_csv())
    dut = LocalDatasetConfig(clause=clause)
    result = dut.load_train()

    train_df = result.dataframe
    assert train_df.shape == (1000, 21)
    assert train_df.columns[0] == 'checking_status'
    assert train_df.columns[20] == 'class'


def test_cols_with_role():
    dut = LocalDatasetConfig(clause=make_dataset(valid_csv()))
    result = dut.cols_with_role(role=RoleName.TARGET)
    assert 1 == len(result)
    assert 'class' == result[0].name


def test_attribute_role_default():
    dut = LocalDatasetConfig(clause=make_dataset(valid_csv()))
    result = dut.cols_with_role(role=RoleName.ATTRIBUTE)
    assert 20 == len(result)


def test_no_target():
    clause = {
        'config': 'local',
        'train_path': valid_csv(),
        'column_roles': {
            'index': {
                'id': 0
            }
        }
    }
    dut = LocalDatasetConfig(clause=clause)
    assert dut.target is None


def test_arff():
    clause = {
        'config': 'local',
        'train_path': valid_arff(),
        'column_roles': {
            'target': {
                'name': 'class'
            }
        }
    }
    dut = LocalDatasetConfig(clause=clause)
    assert isinstance(dut, LocalDatasetConfig)
    assert 'class' == dut.target.name
    assert len(dut.index_cols) == 0


def test_load_arff():
    clause = {
        'config': 'local',
        'train_path': valid_arff(),
        'column_roles': {
            'target': {
                'name': 'class'
            }
        }
    }
    dut = LocalDatasetConfig(clause=clause)
    result = dut.load_train()

    assert DatasetKeys.DATAFRAME.value in result

    train_df = result.dataframe
    assert isinstance(train_df, pd.DataFrame)
    assert train_df.shape == (1000, 21)


def test_load_testdata() -> None:
    clause = {
        'config': 'simple',
        'train_path': valid_arff(filename='credit-train.csv'),
        'test_path': valid_arff(filename='credit-test.csv'),
        'column_roles': {
            'target': {
                'name': 'class'
            }
        }
    }
    dut = LocalDatasetConfig(clause=clause)
    result = dut.load_test()
    assert result is not None
    test_df = result.dataframe
    assert test_df.shape == (200, 20)
    assert 'class' not in test_df.columns
    assert 'own_telephone' in test_df.columns


def test_load_nonexistent_testdata() -> None:
    '''If there is no test data, load_test() returns None'''
    clause = make_dataset(valid_csv())
    dut = LocalDatasetConfig(clause=clause)
    dut.validate()
    result = dut.load_test()
    assert result is None


FORECASTING_CLAUSE: Dict[str, Any] = {
    'config': 'local',
    'column_roles': {
        'target': {
            'name': 'class'
        }
    },
    'forecasting': {
        'horizon': 5,
        'input_size': 15,
        'frequency': 'M'
    }
}


FORECASTING_TASK_CLAUSE = {
    'task': 'forecasting'
}


def test_load_testdata_forecasting() -> None:
    # check that we don't drop the target column for forecasting test data
    clause = FORECASTING_CLAUSE.copy()
    clause['train_path'] = valid_csv()
    clause['test_path'] = valid_csv()

    dut = LocalDatasetConfig(
        clause=clause,
        task=Task(clause=FORECASTING_TASK_CLAUSE))
    test_data = dut.load_test()
    assert test_data is not None
    assert 'class' in test_data.dataframe.columns


def test_forecasting_metadata() -> None:
    clause = FORECASTING_CLAUSE.copy()
    clause['train_path'] = valid_csv()

    dut = LocalDatasetConfig(
        clause=clause,
        task=Task(clause=FORECASTING_TASK_CLAUSE))
    dut.validate()
    assert dut.load_train().metadata.horizon == 5
    assert dut.load_train().metadata.input_size == 15
    assert dut.load_train().metadata.frequency == 'M'
    assert dut.load_train().metadata.step_size == 5


def test_forecasting_step_size() -> None:
    clause = FORECASTING_CLAUSE.copy()
    clause['train_path'] = valid_csv()
    forecasting_dict = clause['forecasting']
    new_dict = forecasting_dict.copy()
    new_dict['step_size'] = 3
    clause['forecasting'] = new_dict

    dut = LocalDatasetConfig(
        clause=clause,
        task=Task(clause=FORECASTING_TASK_CLAUSE))
    dut.validate()
    assert dut.load_train().metadata.horizon == 5
    assert dut.load_train().metadata.input_size == 15
    assert dut.load_train().metadata.frequency == 'M'
    assert dut.load_train().metadata.step_size == 3


def test_forecasting_invalid_step_size() -> None:
    clause = FORECASTING_CLAUSE.copy()
    clause['train_path'] = valid_csv()
    forecasting_dict = clause['forecasting']
    new_dict = forecasting_dict.copy()
    new_dict['step_size'] = 8
    clause['forecasting'] = new_dict

    dut = LocalDatasetConfig(
        clause=clause,
        task=Task(clause=FORECASTING_TASK_CLAUSE))

    with pytest.raises(ValidationErrors, match=r"step_size"):
        dut.validate()


def test_static_exog() -> None:
    clause = FORECASTING_CLAUSE.copy()
    clause['train_path'] = valid_csv()
    clause['test_path'] = valid_csv()
    clause['static_exogenous_path'] = valid_csv()
    dut = LocalDatasetConfig(
        clause=clause,
        task=Task(clause=FORECASTING_TASK_CLAUSE))
    dut.validate()
    got = dut.load_train()
    assert isinstance(got['static_exogenous'], pd.DataFrame)
    got_test = dut.load_test()
    assert got_test is not None
    assert isinstance(got_test['static_exogenous'], pd.DataFrame)
    pd.testing.assert_frame_equal(got['static_exogenous'], got_test['static_exogenous'])


def test_static_exog_missing() -> None:
    clause = FORECASTING_CLAUSE.copy()
    clause['train_path'] = valid_csv()
    clause['test_path'] = valid_csv()

    dut = LocalDatasetConfig(
        clause=clause,
        task=Task(clause=FORECASTING_TASK_CLAUSE))
    dut.validate()
    got = dut.load_train()
    assert got['static_exogenous'] is None

    got_test = dut.load_test()
    assert got_test is not None
    assert got_test['static_exogenous'] is None


CLASSIFICATION_TASK_CLAUSE = {
    'task': 'binary_classification'
}


def test_task_in_metadata_with_load_train() -> None:
    clause = make_dataset(valid_csv())
    task = Task(clause=CLASSIFICATION_TASK_CLAUSE)
    dut = LocalDatasetConfig(clause=clause, task=task)
    dut.validate()
    result = dut.load_train()

    assert result.metadata.task == TaskType.BINARY_CLASSIFICATION


def test_task_in_metadata_with_load_test() -> None:
    clause = {
        'config': 'simple',
        'train_path': valid_arff(filename='credit-train.csv'),
        'test_path': valid_arff(filename='credit-test.csv'),
        'column_roles': {
            'target': {
                'name': 'class'
            }
        }
    }
    task = Task(clause=CLASSIFICATION_TASK_CLAUSE)
    dut = LocalDatasetConfig(clause=clause, task=task)
    dut.validate()
    result = dut.load_test()

    assert result is not None
    assert result.metadata.task == TaskType.BINARY_CLASSIFICATION


def test_load_arbitrary_csv() -> None:
    dut = LocalDatasetConfig(make_dataset(valid_csv(filename='credit-train.csv')))
    got = dut.dataset(data=valid_csv(filename='credit-test.csv'),
                      cols=['class', 'own_telephone'])
    assert got.dataframe.shape == (200, 2)
    assert set(got.dataframe.columns) == {'class', 'own_telephone'}
    assert got.metadata.roles[RoleName.TARGET][0].name == 'class'
