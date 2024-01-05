'''Base class for sklearn models'''
# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

# pylint: disable=duplicate-code,too-many-arguments
from typing import Any, Dict, List, Optional
import importlib

import numpy as np
from numpy.random import RandomState
import pandas as pd

from ..impl.algorithm import Algorithm, AlgorithmCatalog
from ..impl.sklearn_like_algorithm_instance import SklearnLikeAlgorithmInstance
from ..impl.algorithm_instance import DatasetError
from ..impl.fittable_algorithm_instance import UntrainedError

from ...problem_def.task import DataType, TaskType
from ...wrangler.constants import ProblemDefKeys, Defaults
from ...wrangler.dataset import Dataset, DatasetKeys


def is_empty(frame) -> bool:
    '''Determine if an array-like object is empty.'''
    if frame is None:
        return True
    if isinstance(frame, np.ndarray) and frame.size == 0:
        # ndarray.size represents the number of elements in the array
        # ndarray.ndim represents the number of dimensions in the array
        #   arrays with more than 0 dimension can have 0 elements, and
        #   we consider those empty
        return True
    if isinstance(frame, pd.DataFrame) and frame.empty:
        return True
    return False


# TODO(Merritt): set random seed
class SklearnAlgorithm(Algorithm):
    '''Generic object for an sklearn algorithm.'''
    def __init__(self,
                 name: str,
                 algorithm: Optional[type] = None,
                 tasks: Optional[List[TaskType]] = None,
                 data_types: Optional[List[DataType]] = None,
                 tags: Optional[Dict[str, List[str]]] = None,
                 **hyperparams: Any):
        self._name = name
        if algorithm is None:
            algorithm = self._load_module(name)
        self._algorithm = algorithm
        if tasks is None:
            tasks = []
        if data_types is None:
            data_types = []
        if tags is not None:
            self._tags = tags.copy()
        else:
            self._tags = {}
        self._tags.update({
            ProblemDefKeys.TASK_TYPE.value: [t.name.lower() for t in tasks],
            ProblemDefKeys.DATA_TYPE.value: [d.name.lower() for d in data_types],
        })
        super().__init__(**hyperparams)

    def _load_module(self, name: str):
        # Split name into module part (e.g. sklearn.linear_model)
        # and constructor part (e.g. LinearRegression)
        parts = name.split('.')
        constructor_part = parts[-1]
        module = importlib.import_module('.'.join(parts[:-1]))
        # Load the constructor.
        return getattr(module, constructor_part)

    def instantiate(self, **hyperparams) -> 'SklearnAlgorithmInstance':
        # TODO(Merritt): test that we're actually passing hyperparams through
        return SklearnAlgorithmInstance(
            parent=self,
            constructor=self._algorithm,
            **self._default_param_ranges(**self.hyperparams(**hyperparams)))


class SklearnAlgorithmInstance(SklearnLikeAlgorithmInstance):
    '''Generic object for an sklearn algorithm.'''

    def __init__(self, parent: Algorithm, constructor: type, *args, **kwargs):
        self._constructor = constructor
        assert parent._tags is not None, (
            'BUG: Algorithm __init__ should have set _tags'
        )
        if parent._tags.get('supports_random_seed', ['false'])[0] == 'true':
            if 'random_seed' in kwargs:
                kwargs['random_state'] = RandomState(kwargs.pop('random_seed'))
            elif kwargs.get('random_state', None) is None:
                kwargs['random_state'] = RandomState(Defaults.SEED)
        super().__init__(parent, *args, **kwargs)

    def fit(self, dataset: Dataset):
        assert DatasetKeys.TARGET.value in dataset, (
            "BUG: dataset.metadata.target is unexpectedly None")
        target_data = dataset[DatasetKeys.TARGET.value]
        if isinstance(target_data, pd.DataFrame):
            assert dataset.metadata.target is not None
            target_for_sklearn = list(
                target_data[dataset.metadata.target.name])
        else:
            target_for_sklearn = list(target_data)

        covariates = dataset[DatasetKeys.COVARIATES.value]

        new_dataset = dataset.output()
        new_dataset[DatasetKeys.TARGET.value] = target_for_sklearn
        new_dataset[DatasetKeys.COVARIATES.value] = covariates
        super().fit(dataset=new_dataset)

    def predict(self, dataset: Dataset) -> Dataset:
        if not self._trained:
            raise UntrainedError(f'attempt to predict before fit for {self._algorithm.name}')

        # this is not typed because it is supposed to hold the return value from sklearn
        # we expect it to be np.ndarray, but there is no guarantee in sklearn
        predictions_result = np.empty(0)
        probabilities_result = np.empty((0, 0))

        try:
            if not is_empty(dataset[DatasetKeys.COVARIATES.value]):
                predictions_result = self._impl.predict(dataset[DatasetKeys.COVARIATES.value])

                # assume the algorithm has a predict_proba function unless otherwise marked
                has_predict_proba = 'false' not in self._algorithm.tags.get(
                    'has_predict_proba', ['true'])
                if dataset.metadata.task == TaskType.BINARY_CLASSIFICATION and has_predict_proba:
                    probabilities_result = self._impl.predict_proba(
                        dataset[DatasetKeys.COVARIATES.value])

        except KeyError as err:
            raise DatasetError(f'predict dataset malformed {dataset!r}') from err

        # sklearn does not use typed Python, and thus we do not trust
        #    its return value to be consistently typed
        if is_empty(predictions_result):
            predictions_result = np.empty(0)

        retval = dataset.output()
        assert dataset.metadata.target is not None, (
            'BUG: predict() called with no target info in metadata'
        )
        retval.predictions = pd.DataFrame({
            dataset.metadata.target.name: predictions_result
        })

        if not is_empty(probabilities_result):
            # we arbitrarily choose only one column of probabilities to be included in retval
            probabilities_result = np.delete(probabilities_result, 0, axis=1).flatten()
            retval.probabilities = pd.DataFrame({
                dataset.metadata.target.name: probabilities_result
            })

        return retval


def register(catalog: AlgorithmCatalog):  # pylint: disable=unused-argument
    '''Nothing to register.

    All subclasses of SklearnAlgorithm are registered in sklearn_algorithms.py
    '''
