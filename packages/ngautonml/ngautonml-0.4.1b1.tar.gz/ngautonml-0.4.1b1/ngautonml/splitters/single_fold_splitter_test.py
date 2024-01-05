'''Tests for single_fold_splitter.py'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import pandas as pd


from ..problem_def.cross_validation_config import CrossValidationConfig
from ..wrangler.dataset import Dataset, Metadata, RoleName, Column
from .single_fold_splitter import SingleFoldSplitter

# pylint: disable=missing-function-docstring, duplicate-code


def test_split_default_hyperparams() -> None:
    dataframe = pd.DataFrame({
        'a': range(1, 1001),
        'b': range(1001, 2001),
        'c': range(2001, 3001)})
    data = Dataset(metadata=Metadata(
        roles={
            RoleName.TARGET: [Column('c')]
        }
    ))
    data.dataframe = dataframe
    dut = SingleFoldSplitter(cv_config=CrossValidationConfig({}))

    got = dut.split(dataset=data)

    # default train_frac: 0.8
    got = dut.split(dataset=data)
    assert got.ground_truth is not None
    assert got.ground_truth.ground_truth.shape == (200, 1)
    assert len(got.folds) == 1
    assert got.folds[0].train.dataframe.shape == (800, 3)
    assert got.folds[0].validate.dataframe.shape == (200, 2)


def test_split_override_hyperparams() -> None:
    dataframe = pd.DataFrame({
        'a': range(1, 1001),
        'b': range(1001, 2001),
        'c': range(2001, 3001)})
    data = Dataset(metadata=Metadata(
        roles={
            RoleName.TARGET: [Column('c')]
        }
    ))
    data.dataframe = dataframe
    dut = SingleFoldSplitter(cv_config=CrossValidationConfig({}))

    got = dut.split(dataset=data, train_frac=0.6)
    assert got.ground_truth is not None
    assert got.ground_truth.ground_truth.shape == (400, 1)
    assert len(got.folds) == 1
    assert got.folds[0].train.dataframe.shape == (600, 3)
    assert got.folds[0].validate.dataframe.shape == (400, 2)
