'''Metric object class for configurable and user-made metrics.'''
import abc

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from typing import Optional

from ...catalog.catalog_element_mixin import CatalogElementMixin
from ...wrangler.dataset import Dataset
from ...wrangler.dataset import DatasetKeys


class MetricError(Exception):
    '''Base error class for metrics'''


class MetricNameError(MetricError):
    '''Metric lacks a proper indexing name.'''


class MetricAttributeError(MetricError):
    '''Metric is missing a required attribute.'''


class MetricInvalidDatasetError(MetricError):
    '''Metric was passed a dataset it cannot use.'''


class Metric(CatalogElementMixin, metaclass=abc.ABCMeta):
    '''Base class wrapper for accessing metric objects.'''
    _name: Optional[str] = None
    _high: bool = True  # True means a higher score is better.
    _uses_proba: bool = False
    # True means metric uses class probabilites instead of class predictions.

    def __str__(self):
        return self.name

    @property
    def high(self) -> bool:
        '''Returns true if higher scores are better.'''
        return self._high

    @property
    def uses_proba(self) -> bool:
        '''True means metric uses class probabilites instead of class predictions.

        Should only be True for classification metrics.
        '''
        return self._uses_proba

    @abc.abstractmethod
    def calculate(self, pred: Dataset, ground_truth: Optional[Dataset] = None) -> float:
        '''Calculates the metric results.'''


class SupervisedMetric(Metric):
    '''Subclass for supervised Metrics'''

    def validate_input(self, pred: Dataset, ground_truth: Optional[Dataset] = None) -> Dataset:
        '''Validates the Dataset and GroundTruth given. Useful for derived classes.'''
        if ground_truth is None:
            raise MetricInvalidDatasetError(
                'No Ground Truth Provided!')

        if DatasetKeys.PREDICTIONS.value not in pred:
            raise MetricInvalidDatasetError(
                f'Predictions has no "{DatasetKeys.PREDICTIONS.value}" key.')

        if DatasetKeys.GROUND_TRUTH.value not in ground_truth:
            raise MetricInvalidDatasetError(
                f'Ground truth has no "{DatasetKeys.GROUND_TRUTH.value}" key.')

        if ground_truth.metadata.target is None:
            raise MetricInvalidDatasetError(
                'Ground truth has no target column in metadata.')

        # We take a Optional[Dataset] and turn it into a Dataset. Type checkers are happy.
        return ground_truth

    @abc.abstractmethod
    def calculate(self, pred: Dataset, ground_truth: Optional[Dataset] = None) -> float:
        '''
        Calculates the metric results.

        Most Supervised Metrics will require a ground truth. The implementation
        of the calculate should check if the ground truth exists.
        '''


class MetricStub(Metric):
    '''This is a stub'''
    _name = 'stub_metric'
    _high = True

    def calculate(self, pred: Dataset, ground_truth: Optional[Dataset] = None) -> float:
        return 0.0
