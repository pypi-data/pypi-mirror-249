'''Tests for sklearn_metrics.py'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from typing import Tuple

import pandas as pd
import pytest

from .impl.metric_catalog import MetricCatalog
from ..metrics.impl.metric import MetricInvalidDatasetError
from ..wrangler.dataset import Dataset, Metadata, RoleName, Column

from .sklearn_metrics import register
# pylint: disable=missing-function-docstring,redefined-outer-name


def make_catalog() -> MetricCatalog:
    retval = MetricCatalog()
    register(retval)
    return retval


@pytest.fixture(scope='session')
def classification_results() -> Tuple[Dataset, Dataset]:
    metadata = Metadata(
        roles={RoleName.TARGET: [Column('target')]},
        pos_labels={RoleName.TARGET: 'a'})
    pred = Dataset(metadata=metadata)
    pred.predictions = pd.DataFrame({'target': ['a', 'b', 'b', 'a']})
    pred.probabilities = pd.DataFrame({'target': [.3, .4, .5, .5]})

    ground_truth = Dataset(metadata=metadata)
    ground_truth.ground_truth = pd.DataFrame({'target': ['a', 'a', 'b', 'a']})
    return (pred, ground_truth)


@pytest.fixture(scope='session')
def regression_results() -> Tuple[Dataset, Dataset]:
    pred = Dataset(
        metadata=Metadata(
            roles={RoleName.TARGET: [Column('target')]}
        )
    )
    pred.predictions = pd.DataFrame({'target': [1.3, 2.8, 7.5, 2.1]})

    ground_truth = Dataset(
        metadata=Metadata(
            roles={RoleName.TARGET: [Column('target')]}
        )
    )
    ground_truth.ground_truth = pd.DataFrame({'target': [0.4, 3.5, 7.6, 2.0]})
    return (pred, ground_truth)


@pytest.mark.parametrize("name,value,precision", [
    ('roc_auc_score', 0.8333333333, 1e-6),
    ('accuracy_score', 0.75, 1e-6),
    ('f1_score', 0.8, 1e-6),
])
def test_classif_metrics(name: str, value: float, precision: float,
                         classification_results: Tuple[Dataset, Dataset]) -> None:
    pred, ground_truth = classification_results
    catalog = make_catalog()
    dut = catalog.lookup_by_name(name=name)

    assert dut.calculate(pred=pred, ground_truth=ground_truth) == pytest.approx(value, precision)


@pytest.mark.parametrize("name,value,precision", [
    ('mean_absolute_error', 0.45, 1e-6),
    ('mean_squared_error', 0.33, 1e-6),
    ('root_mean_squared_error', 0.57445626, 1e-6),
    ('r2_score', 0.95385825, 1e-6)
])
def test_regression_metrics(name: str, value: float, precision: float,
                            regression_results: Tuple[Dataset, Dataset]) -> None:
    pred, ground_truth = regression_results
    catalog = make_catalog()
    dut = catalog.lookup_by_name(name=name)

    assert dut.calculate(pred=pred, ground_truth=ground_truth) == pytest.approx(value, precision)


def test_roc_auc_no_gt(classification_results: Tuple[Dataset, Dataset]) -> None:
    pred, _ = classification_results
    pred.probabilities = pd.DataFrame({'target': [.3, .4, .5, .5]})
    catalog = make_catalog()
    dut = catalog.lookup_by_name('roc_auc_score')

    with pytest.raises(MetricInvalidDatasetError, match=r'(?i)ground.*truth'):
        dut.calculate(pred=pred)


def test_roc_auc_no_proba(classification_results: Tuple[Dataset, Dataset]) -> None:
    pred, ground_truth = classification_results
    catalog = make_catalog()
    dut = catalog.lookup_by_name('roc_auc_score')
    del pred['probabilities']

    with pytest.raises(MetricInvalidDatasetError, match=r'(?i)probabilit'):
        dut.calculate(pred=pred, ground_truth=ground_truth)


def test_accuracy_no_gt(classification_results: Tuple[Dataset, Dataset]) -> None:
    pred, _ = classification_results
    catalog = make_catalog()
    dut = catalog.lookup_by_name('accuracy_score')

    with pytest.raises(MetricInvalidDatasetError, match=r'(?i)ground.*truth'):
        dut.calculate(pred=pred)
