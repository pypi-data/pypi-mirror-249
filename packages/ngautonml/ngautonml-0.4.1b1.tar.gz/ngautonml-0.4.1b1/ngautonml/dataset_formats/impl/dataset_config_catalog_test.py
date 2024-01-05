'''Tests for dataset_config_catalog.py'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from .dataset_format_catalog import DatasetFormatCatalogAuto
from ..memory import MemoryDatasetFormat
from ..local import LocalDatasetFormat

# pylint: disable=missing-function-docstring


def test_sunny_day() -> None:
    dut = DatasetFormatCatalogAuto()
    assert isinstance(dut.lookup_by_name('memory'), MemoryDatasetFormat)
    assert isinstance(dut.lookup_by_name('local'), LocalDatasetFormat)
