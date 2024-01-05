'''Tests for the Dataset class'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import pandas as pd
import pytest

from .dataset import Dataset, Metadata, RoleName, Column
from .dataset import DatasetKeys, DatasetKeyError, DatasetValueError

# pylint: disable=missing-function-docstring,pointless-statement


def test_output():
    roles = {RoleName.TIME: Column('bug')}
    dut = Dataset(metadata=Metadata(roles=roles))
    dut['some_key'] = 'some_val'
    got = dut.output().roles
    assert Column('bug') == got[RoleName.TIME]
    with pytest.raises(KeyError):
        got['some_key']


def test_output_overrides():
    roles = {RoleName.TIME: Column('bug')}
    roles2 = {RoleName.TIME: Column('bugs')}
    dut = Dataset(metadata=Metadata(roles=roles))
    dut['some_key'] = 'some_val'
    got = dut.output(override_metadata=Metadata(roles=roles2))
    assert Column('bugs') == got.roles[RoleName.TIME]
    with pytest.raises(KeyError):
        got['some_key']


def test_output_overrides_role():
    roles = {RoleName.TIME: Column('bug')}
    roles2 = {RoleName.TIME: Column('bugs')}
    dut = Dataset(metadata=Metadata(roles=roles, forecasting={'horizon': 10}))
    dut['some_key'] = 'some_val'
    got = dut.output(override_metadata=dut.metadata.override_roles(roles=roles2))
    assert Column('bugs') == got.roles[RoleName.TIME]
    assert got.metadata.horizon == 10


def test_get_dataframe():
    dut = Dataset()
    dataframe = pd.DataFrame({'bug': [1, 2], 'bug2': ['a', 'b']})
    dut.dataframe = dataframe

    assert 'bug' == dut.get_dataframe().columns[0]


def test_df_setters_and_getters() -> None:
    dut = Dataset()
    df1 = pd.DataFrame({'a': [1]})
    df2 = pd.DataFrame({'b': [2]})
    df3 = pd.DataFrame({'c': [3]})
    dut.dataframe = df1
    dut.ground_truth = df2
    dut.predictions = df3
    pd.testing.assert_frame_equal(df1, dut.dataframe)
    pd.testing.assert_frame_equal(df2, dut.ground_truth)
    pd.testing.assert_frame_equal(df3, dut.predictions)


def test_df_getters_proper_errors() -> None:
    dut = Dataset()
    with pytest.raises(DatasetKeyError):
        _ = dut.dataframe

    dut[DatasetKeys.DATAFRAME.value] = 'hamster'
    with pytest.raises(DatasetValueError, match='hamster'):
        _ = dut.dataframe

    dut[DatasetKeys.GROUND_TRUTH.value] = 'gerbil'
    with pytest.raises(DatasetValueError, match='gerbil'):
        _ = dut.ground_truth

    dut[DatasetKeys.PREDICTIONS.value] = 'skink'
    with pytest.raises(DatasetValueError, match='skink'):
        _ = dut.predictions
