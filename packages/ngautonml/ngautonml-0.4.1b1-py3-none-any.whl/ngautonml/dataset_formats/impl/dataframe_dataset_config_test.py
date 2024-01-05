'''Test for dataframe_dataset_config.py'''

# pylint: disable=missing-function-docstring,missing-class-docstring

from typing import Optional

import pandas as pd

from ...wrangler.dataset import Dataset, RoleName
from .dataframe_dataset_config import DataframeDatasetConfig


class FakeConfig(DataframeDatasetConfig):

    def load_train(self) -> Dataset:
        return Dataset()

    def load_test(self) -> Optional[Dataset]:
        return None


def test_dataset_cols() -> None:
    dut = FakeConfig({})
    got = dut.dataset(
        pd.DataFrame({
            'a': [1, 2, 3],
            'b': [4, 5, 6]
        }),
        cols=['a']
    )

    want = pd.DataFrame({
        'a': [1, 2, 3]
    })

    pd.testing.assert_frame_equal(want, got.dataframe)


def test_dataset_roles() -> None:
    dut = FakeConfig({
        'column_roles': {
            'target': {'name': 'a'},
            'test_role': {'name': 'b'},
            'attribute': {'name': 'c'},
        }
    })
    df = pd.DataFrame({
        'a': [1, 2, 3],
        'b': [4, 5, 6],
        'c': [7, 8, 9]
    })
    got1 = dut.dataset(data=df, roles=[RoleName.TARGET])
    want1 = pd.DataFrame({
        'a': [1, 2, 3]})
    pd.testing.assert_frame_equal(got1.dataframe, want1)

    got2 = dut.dataset(data=df, roles=['attribute', RoleName.TEST_ROLE])
    want2 = pd.DataFrame({
        'b': [4, 5, 6],
        'c': [7, 8, 9],
    })
    pd.testing.assert_frame_equal(got2.dataframe, want2)


def test_dataset_roles_cols() -> None:
    dut = FakeConfig({
        'column_roles': {
            'target': {'name': 'a'},
            'attribute': {'name': 'c'},
            'test_role': {'name': 'd'},
        }
    })
    df = pd.DataFrame({
        'a': [1, 2, 3],
        'b': [4, 5, 6],
        'c': [7, 8, 9],
        'd': [10, 12, 13]  # ROFL
    })
    got = dut.dataset(data=df, roles=['target', 'attribute'], cols=['a', 'b'])
    want = pd.DataFrame({
        'a': [1, 2, 3],
        'b': [4, 5, 6],
        'c': [7, 8, 9]
    })
    pd.testing.assert_frame_equal(got.dataframe, want)
