'''Wrappers of metrics from sklearn, currently only contains roc_auc_score.'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from typing import Any, Callable, Dict, List, Optional

import numpy as np
import sklearn.metrics  # type: ignore[import]
from sklearn.metrics import mean_squared_error  # type: ignore[import]

from ..problem_def.task import TaskType
from ..wrangler.constants import ProblemDefKeys
from ..wrangler.dataset import Dataset, DatasetKeyError, RoleName
from .impl.metric import MetricInvalidDatasetError, SupervisedMetric
from .impl.metric_catalog import MetricCatalog


class SklearnMetric(SupervisedMetric):
    '''Wrapper for sklean.metrics'''
    _metric: Optional[Callable[..., float]] = None

    def __init__(self,
                 name: str,
                 metric: Optional[Callable[..., float]] = None,
                 tasks: Optional[List[TaskType]] = None,
                 high: bool = True,
                 uses_proba: bool = False,
                 needs_pos_label: bool = False):
        # TODO(Merritt): high, uses_proba, needs_pos_label should be put in tags
        if metric is None:
            metric = getattr(sklearn.metrics, name, None)
        self._metric = metric
        if tasks is None:
            tasks = []
        self._tags = {
            ProblemDefKeys.TASK_TYPE.value: [t.name.lower() for t in tasks],
        }
        self._needs_pos_label = needs_pos_label
        self._high = high
        self._uses_proba = uses_proba
        super().__init__(name=name)

    def calculate(self, pred: Dataset, ground_truth: Optional[Dataset] = None) -> float:
        # TODO(Merritt): should be able to accept hyperparams from problem def
        ground_truth = self.validate_input(pred, ground_truth)
        # validate_input is guaranteed to return ground truth Dataset rather than None.
        assert ground_truth.metadata.target is not None
        ground_truth_for_sklearn = list(
            ground_truth.ground_truth[ground_truth.metadata.target.name])
        assert pred.metadata.target is not None, (
            'BUG: calculate() called with no target info in metadata'
        )

        if self.uses_proba:
            try:
                pred_df = pred.probabilities
            except DatasetKeyError:
                # We are not using 'from' because this error will be displayed
                #   alongside metric scores as a explanation for why this score
                #   cannot be calculated, thus we want it to be succint.
                raise MetricInvalidDatasetError(   # pylint: disable=raise-missing-from
                    'No class probabilities output.')
        else:
            pred_df = pred.predictions

        predictions_for_sklearn = list(
            pred_df[pred.metadata.target.name])

        assert self._metric is not None

        if RoleName.TARGET in pred.metadata.pos_labels and self._needs_pos_label:
            return self._metric(
                ground_truth_for_sklearn,
                predictions_for_sklearn,
                pos_label=pred.metadata.pos_labels[RoleName.TARGET])

        return self._metric(ground_truth_for_sklearn, predictions_for_sklearn)


def root_mean_squared_error(*args, **kwargs):
    '''Root Mean Squared Error'''
    return np.sqrt(mean_squared_error(*args, **kwargs))


METRICS: List[Dict[str, Any]] = [
    {
        'name': 'roc_auc_score',
        'tasks': [TaskType.BINARY_CLASSIFICATION],
        'uses_proba': True,
    },
    {
        'name': 'accuracy_score',
        'tasks': [TaskType.BINARY_CLASSIFICATION, TaskType.MULTICLASS_CLASSIFICATION],
    },
    {
        'name': 'f1_score',
        'high': True,
        'tasks': [TaskType.BINARY_CLASSIFICATION],
        'needs_pos_label': True,
    },
    {
        'name': 'mean_squared_error',
        'tasks': [TaskType.FORECASTING, TaskType.REGRESSION],
        'high': False,
    },
    {
        'name': 'root_mean_squared_error',
        'metric': root_mean_squared_error,
        'tasks': [TaskType.FORECASTING, TaskType.REGRESSION],
        'high': False,
    },
    {
        'name': 'mean_absolute_error',
        'tasks': [TaskType.FORECASTING, TaskType.REGRESSION],
        'high': False,
    },
    {
        'name': 'r2_score',
        'high': True,
        'tasks': [TaskType.REGRESSION],
    },
]


def register(catalog: MetricCatalog):
    '''Register all the metrics in this file.'''
    for met in METRICS:
        catalog.register(SklearnMetric(**met))
