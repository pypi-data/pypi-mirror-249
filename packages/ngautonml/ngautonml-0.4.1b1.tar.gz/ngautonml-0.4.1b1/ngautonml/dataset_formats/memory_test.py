""" Tests for MemoryDatasetConfig """
from typing import Dict, Any

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import pandas as pd

from .memory import MemoryDatasetConfig
from ..problem_def.task import Task, TaskType
from ..wrangler.dataset import RoleName

# pylint: disable=missing-function-docstring

CLAUSE = {
    'config': 'memory',
    'column_roles': {
        'target': {
            'name': 'a',
            'pos_label': 1
        }
    }
}
TRAIN_DF = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})


def test_sunny_day():
    dut = MemoryDatasetConfig(train_df=TRAIN_DF, clause=CLAUSE)
    dut.validate()
    result = dut.load_train()
    got_train_df = result.dataframe

    assert got_train_df.shape == (2, 2)
    assert RoleName.TARGET in result.metadata.roles.keys()
    assert len(result.metadata.roles[RoleName.TARGET]) == 1
    assert result.metadata.roles[RoleName.TARGET][0].name == 'a'


def test_attribute_role_default():
    dut = MemoryDatasetConfig(train_df=TRAIN_DF, clause=CLAUSE)
    dut.validate()
    result = dut.cols_with_role(role=RoleName.ATTRIBUTE)

    assert 1 == len(result)
    assert result[0].name == 'b'


def test_no_target():
    clause_without_target = {
        'config': 'memory',
        'column_roles': {}
    }
    dut = MemoryDatasetConfig(train_df=TRAIN_DF, clause=clause_without_target)
    dut.validate()

    assert dut.target is None


def test_load_testdata() -> None:
    test_df = pd.DataFrame({'a': [1, 2, 2], 'b': [30, 40, 500]})
    dut = MemoryDatasetConfig(train_df=TRAIN_DF, clause=CLAUSE, test_df=test_df)
    dut.validate()
    result = dut.load_test()

    assert result is not None   # needed to make pylint happy
    got_test_df = result.dataframe

    assert got_test_df.shape == (3, 1)
    assert 'a' not in got_test_df.columns
    assert 'b' in got_test_df.columns


def test_load_nonexistent_testdata() -> None:
    dut = MemoryDatasetConfig(train_df=TRAIN_DF, clause=CLAUSE)
    dut.validate()
    result = dut.load_test()

    assert result is None


FORECASTING_CLAUSE: Dict[str, Any] = {
    'config': 'memory',
    'column_roles': {
        'target': {
            'name': 'a'
        }
    },
    'forecasting': {
        'horizon': 1,
        'input_size': 1,
        'frequency': 'M'
    }
}


FORECASTING_TASK_CLAUSE = {
    'task': 'forecasting'
}


def test_load_testdata_forecasting() -> None:
    """check that we don't drop the target column for forecasting test data"""
    forecasting_clause = FORECASTING_CLAUSE.copy()
    test_df = pd.DataFrame({'a': [1], 'b': [30]})

    dut = MemoryDatasetConfig(
        train_df=TRAIN_DF,
        clause=forecasting_clause,
        test_df=test_df,
        task=Task(clause=FORECASTING_TASK_CLAUSE))
    dut.validate()
    test_data = dut.load_test()

    assert test_data is not None
    assert 'a' in test_data.dataframe.columns


def test_forecasting_metadata() -> None:
    forecasting_clause = {
        'config': 'memory',
        'column_roles': {
            'target': {
                'name': 'a'
            }
        },
        'forecasting': {
            'horizon': 1,
            'input_size': 3,
            'frequency': 'M'
        }
    }
    custom_train_df = pd.DataFrame({'a': [1, 2, 1, 2, 1], 'b': [3, 4, 5, 6, 7]})

    dut = MemoryDatasetConfig(
        train_df=custom_train_df,
        clause=forecasting_clause,
        task=Task(clause=FORECASTING_TASK_CLAUSE))
    dut.validate()
    train_data = dut.load_train()

    assert train_data.metadata.horizon == 1
    assert train_data.metadata.input_size == 3
    assert train_data.metadata.frequency == 'M'
    assert train_data.metadata.step_size == 1


CLASSIFICATION_TASK_CLAUSE = {
    'task': 'binary_classification'
}


def test_task_in_metadata_with_load_train() -> None:
    clause = CLAUSE.copy()
    task = Task(clause=CLASSIFICATION_TASK_CLAUSE)
    dut = MemoryDatasetConfig(train_df=TRAIN_DF, clause=clause, task=task)
    dut.validate()
    result = dut.load_train()

    assert result.metadata.task == TaskType.BINARY_CLASSIFICATION


def test_task_in_metadata_with_load_test() -> None:
    clause = CLAUSE.copy()
    test_df = pd.DataFrame({'a': [1], 'b': [30]})
    task = Task(clause=CLASSIFICATION_TASK_CLAUSE)
    dut = MemoryDatasetConfig(train_df=TRAIN_DF, test_df=test_df,
                              clause=clause, task=task)
    dut.validate()
    result = dut.load_test()

    assert result is not None
    assert result.metadata.task == TaskType.BINARY_CLASSIFICATION
