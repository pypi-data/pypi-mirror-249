'''Holds cofirguration information about the dataset.'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

# pylint: disable=protected-access

import abc
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from ...problem_def.config_component import (ConfigComponent, ConfigError,
                                             InvalidKeyError, InvalidValueError,
                                             MissingKeyError, ValidationErrors)
from ...problem_def.task import Task
from ...wrangler.dataset import Dataset, Metadata, RoleName, Column
from ...wrangler.constants import Defaults, ProblemDefKeys, ProblemDefKeySet


class DatasetConfigError(ConfigError):
    '''Base class for errors in DatasetConfig.'''


class UnknownConfigClassError(DatasetConfigError):
    '''Problem definition specified a dataset config that is not recognized.'''


class DatasetFileError(DatasetConfigError):
    '''The dataset file does not match information given in the problem definition.'''


class DatasetConfigTypeError(DatasetConfigError, TypeError):
    '''An object in the dataset config was not the right type.'''


class ParsingErrors(DatasetConfigError):
    '''At least one parsing error occured.'''
    def __init__(self, errors: List[DatasetConfigError]):
        super().__init__(f'At least one parsing error occured: {errors!r}')
        self.errors = errors


class DatasetConfig(ConfigComponent, metaclass=abc.ABCMeta):
    '''Holds confirguration information about the dataset.'''
    _roles: Dict[RoleName, List[Column]]
    _pos_labels: Dict[RoleName, Any]
    _forecasting_metadata: Dict[str, Any]
    _task: Optional[Task]

    def __init__(self,
                 clause: Dict[str, Any],
                 parents: Optional[List[str]] = None,
                 task: Optional[Task] = None,
                 **unused_kwargs):
        parents = self._add_parent(parents, ProblemDefKeys.CONFIG.value)
        super().__init__(clause=clause, parents=parents)
        self._roles = self._build_roles()
        self._pos_labels = self._build_pos_labels()
        self._forecasting_metadata = self._build_forecasting_metadata()
        self._task = task

    def __str__(self):
        return f'{{Index: {self.index_cols}, Target: {self.target}}}'

    def _build_roles(self) -> Dict[RoleName, List[Column]]:
        '''Build dict of column roles'''
        retval: Dict[RoleName, List[Column]] = {}
        for role in self._get_with_default(ProblemDefKeys.COL_ROLES, dflt={}):
            # this will throw a parsing error if the key does not match any known role name
            rolename = RoleName[role.upper()]

            col_names = self._get_with_default(ProblemDefKeys.COL_ROLES,
                                               role,
                                               ProblemDefKeys.COL_NAME,
                                               dflt=None)
            if col_names is not None:
                retval[rolename] = [Column(name=col_names)]
            # TODO(Merritt): make this more sensible

        return retval

    def _build_pos_labels(self) -> Dict[RoleName, Any]:
        '''Build dict of pos labels for binary classification.

        In the vast majority of cases, the only key will be RoleName.TARGET'''
        retval: Dict[RoleName, Any] = {}
        for role in self._get_with_default(ProblemDefKeys.COL_ROLES, dflt={}):
            rolename = RoleName[role.upper()]
            retval[rolename] = self._get_with_default(
                ProblemDefKeys.COL_ROLES, role, ProblemDefKeys.POS_LABEL, dflt=None)
        return retval

    def _build_forecasting_metadata(self) -> Dict[str, Any]:
        '''Build dict of additional metadata for forecasting problems.

        This includes 'horizon', 'input_size', and 'frequency'.
        '''
        retval: Dict[str, Any] = {}
        clause = self._get_with_default(ProblemDefKeys.FORECASTING, dflt={})
        if not isinstance(clause, dict):
            return retval
        for key, val in clause.items():
            retval[key] = val
        if ProblemDefKeys.FREQUENCY.value not in retval:
            retval[ProblemDefKeys.FREQUENCY.value] = Defaults.FREQUENCY

        # If step_size is not defined, set as equal to horizon
        if (ProblemDefKeys.STEP_SIZE.value not in retval
                and ProblemDefKeys.HORIZON.value in retval):
            retval[ProblemDefKeys.STEP_SIZE.value] = retval[ProblemDefKeys.HORIZON.value]

        return retval

    def validate(self, **kwargs) -> None:
        '''Check the problem definition dataset clause for errors.'''
        errors: List[ConfigError] = []

        dataset_keys = set(self._clause.keys())
        if not ProblemDefKeySet.DATASET.REQUIRED.issubset(dataset_keys):
            errors.append(MissingKeyError(
                'Required keys missing in dataset clause: '
                f'{ProblemDefKeySet.DATASET.REQUIRED.difference(dataset_keys)}'))

        if not dataset_keys.issubset(ProblemDefKeySet.DATASET.ALLOWED):
            errors.append(InvalidKeyError(
                'Invalid key(s) in dataset clause: '
                f'{dataset_keys.difference(ProblemDefKeySet.DATASET.ALLOWED)}'
            ))

        try:
            self._validate_roles()
        except ValidationErrors as err:
            errors.extend(err.errors)

        if self._exists(ProblemDefKeys.FORECASTING.value):
            data_keys = set(self._get(ProblemDefKeys.FORECASTING.value).keys())
            if not ProblemDefKeySet.DATASET.FORECASTING.REQUIRED.issubset(data_keys):
                errors.append(MissingKeyError(
                    'Required keys missing in forecasting metadata: '
                    f'{ProblemDefKeySet.DATASET.FORECASTING.REQUIRED.difference(data_keys)}'))

            if not data_keys.issubset(ProblemDefKeySet.DATASET.FORECASTING.ALLOWED):
                errors.append(InvalidKeyError(
                    'Invalid key(s) in forecasting metadata: '
                    f'{data_keys.difference(ProblemDefKeySet.DATASET.FORECASTING.ALLOWED)}'))

            freq_val = self._get_with_default(
                ProblemDefKeys.FORECASTING.value,
                ProblemDefKeys.FREQUENCY.value,
                dflt=Defaults.FREQUENCY)
            offset_strs = [x for x in dir(pd.offsets) if DatasetConfig._is_valid_offset(x)]
            allowed_freq = [getattr(pd.offsets, x)().freqstr for x in offset_strs]

            if freq_val not in allowed_freq:
                errors.append(InvalidValueError(
                    'Invalid value in forecasting metadata: '
                    f'{freq_val} is not a valid value for frequency. '
                    f'Allowed frequency values are: {allowed_freq}'))

            if ProblemDefKeys.HORIZON.value in data_keys:
                step_size = self.metadata.step_size or 0
                horizon = self._get(ProblemDefKeys.FORECASTING.value,
                                    ProblemDefKeys.HORIZON.value)
                if (step_size < 1) or (step_size > horizon):
                    errors.append(InvalidValueError(
                        'Invalid value in forecasting metadata: '
                        f'{step_size} is not a valid value for step_size. '
                        f'Value for step_size must be between 1 and {horizon}'
                    ))

        if len(errors) > 0:
            raise ValidationErrors(errors=errors)

    def _validate_roles(self) -> None:
        if ProblemDefKeys.COL_ROLES.value not in set(self._clause.keys()):
            return

        errors: List[ConfigError] = []

        for role_name in self._get(ProblemDefKeys.COL_ROLES.value):
            role_keys = set(self._get(ProblemDefKeys.COL_ROLES.value,
                                      role_name).keys())
            if not ProblemDefKeySet.DATASET.ROLES.REQUIRED.issubset(role_keys):
                errors.append(MissingKeyError(
                    f'Required key(s) missing in role clause for role {role_name}: '
                    f'{ProblemDefKeySet.DATASET.ROLES.REQUIRED.difference(role_keys)}'))

            if not role_keys.issubset(ProblemDefKeySet.DATASET.ROLES.ALLOWED):
                errors.append(InvalidKeyError(
                    f'Invalid key(s) in role clause for role {role_name}: '
                    f'{role_keys.difference(ProblemDefKeySet.DATASET.ROLES.ALLOWED)}'
                ))

        if len(errors) > 0:
            raise ValidationErrors(errors=errors)

    @staticmethod
    def _is_valid_offset(offset: str) -> bool:
        invalid_offsets = set(['BaseOffset', 'Tick', 'DateOffset', 'Easter'])
        obj = getattr(pd.offsets, offset)

        return not offset.startswith('_') and callable(obj) and offset not in invalid_offsets

    def cols_with_role(self, role: Union[str, RoleName]) -> List[Column]:
        '''Return a list of Columns that have the given role'''
        if isinstance(role, str):
            role = RoleName[role.upper()]
        if role not in self._roles:
            return []
        return self._roles[role]

    @property
    def target(self) -> Optional[Column]:
        '''Column with role "target".'''
        cols = self.cols_with_role(role=RoleName.TARGET)
        if len(cols) == 0:
            return None
        if len(cols) == 1:
            return cols[0]
        raise DatasetConfigError(f'Must have at most 1 target column, instead found {cols}')

    @property
    def roles(self) -> Dict[RoleName, List[Column]]:
        '''Full mapping of roles to lists of columns.'''
        return self._roles

    @property
    def index_cols(self) -> List[Column]:
        '''Column(s) containing indices for rows.'''
        return self.cols_with_role(role=RoleName.INDEX)

    @property
    def train_fraction(self) -> float:
        '''Config for the fraction of data to use for train.'''
        return self._get_with_default(
            ProblemDefKeys.SPLIT, ProblemDefKeys.TRAIN_FRAC, dflt=Defaults.SPLIT_FRACTION)

    def pos_label(self, role: RoleName) -> Optional[Any]:
        '''If this is a binary classification problem, return the positive label; otherwise None.'''
        return self._pos_labels[role]

    @property
    def forecasting(self) -> Optional[Dict[str, Any]]:
        '''Forecasting metadata'''
        retval = self._forecasting_metadata
        if not retval:
            return None
        return retval

    @property
    def metadata(self) -> Metadata:
        '''The metadata needed by models.'''
        task = None

        if self._task is not None:
            task = self._task.task_type

        return Metadata(roles=self._roles, pos_labels=self._pos_labels, task=task,
                        forecasting=self._forecasting_metadata)

    @abc.abstractmethod
    def load_train(self) -> Dataset:
        '''Load a Dataset from the information in the problem description'''

    @abc.abstractmethod
    def load_test(self) -> Optional[Dataset]:
        '''Load test data if it exists, otherwise None'''

    @abc.abstractmethod
    def dataset(self, data: Any, **kwargs) -> Dataset:
        '''Load a Dataset object, by placing data at supplied key.'''


class D3MDatasetConfig(DatasetConfig):
    '''Holds information about a local D3M formatted dataset.'''

    def load_train(self) -> Dataset:
        raise NotImplementedError

    def load_test(self) -> Optional[Dataset]:
        '''Load test data if it exists, otherwise None'''
        raise NotImplementedError

    def dataset(self, data: Any, **kwargs) -> Dataset:
        raise NotImplementedError


class TensorFlowDatasetConfig(DatasetConfig):
    '''Holds information about a local TensorFlow dataset.'''

    def load_train(self) -> Dataset:
        raise NotImplementedError

    def load_test(self) -> Optional[Dataset]:
        '''Load test data if it exists, otherwise None'''
        raise NotImplementedError

    def dataset(self, data: Any, **kwargs) -> Dataset:
        raise NotImplementedError


class CloudDatasetConfig(DatasetConfig):
    '''Holds information about a tabular dataset stored in the cloud.'''

    def load_train(self) -> Dataset:
        raise NotImplementedError

    def load_test(self) -> Optional[Dataset]:
        '''Load test data if it exists, otherwise None'''
        raise NotImplementedError

    def dataset(self, data: Any, **kwargs) -> Dataset:
        raise NotImplementedError
