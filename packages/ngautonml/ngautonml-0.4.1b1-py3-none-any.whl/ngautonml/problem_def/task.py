'''Class representing problem type, which is a combination of data type and task.'''
from typing import List, Optional, Dict, Any
from enum import Enum, auto

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from .config_component import ConfigComponent, ConfigError
from .config_component import InvalidKeyError, ValidationErrors, MissingKeyError
from .config_component import InvalidValueError, ProblemDefTypeError
from ..wrangler.constants import ProblemDefKeys, ProblemDefKeySet, Defaults


class DataType(Enum):
    '''Possible input data types'''
    TABULAR = auto()
    IMAGE = auto()
    TIMESERIES = auto()
    TEXT = auto()

    @staticmethod
    def validate(name: str) -> List[str]:
        '''Return an error message if data type is not in the list'''
        errors: List[str] = []
        names = [member.name for member in DataType]
        if name.upper() not in names:
            errors.append(f'"{name}" not among valid data types: f{names}')
        return errors


class TaskType(Enum):
    '''Possible ML tasks'''
    BINARY_CLASSIFICATION = auto()
    MULTICLASS_CLASSIFICATION = auto()
    REGRESSION = auto()
    FORECASTING = auto()
    TEST_TASK = auto()  # Only used in testing

    @staticmethod
    def validate(name: str) -> List[str]:
        '''Return an error message if task type is not in the list'''
        errors: List[str] = []
        names = [member.name for member in TaskType]
        if name.upper() not in names:
            errors.append(f'"{name}" not among valid task types: f{names}')
        return errors


class Task(ConfigComponent):
    '''Parsed form of the problem_type.'''

    def __init__(self, clause: Dict[str, Any], parents: Optional[List[str]] = None):
        parents = self._add_parent(parents, ProblemDefKeys.TASK.value)
        super().__init__(clause=clause, parents=parents)

    @property
    def data_type(self) -> DataType:
        '''Data type'''
        return DataType[self._get_with_default(
            ProblemDefKeys.DATA_TYPE.value,
            dflt=Defaults.DATA_TYPE).upper()]

    @property
    def task_type(self) -> Optional[TaskType]:
        '''ML task'''
        field = self._get_with_default(
            ProblemDefKeys.TASK_TYPE.value,
            dflt=None
        )
        if field is None:
            return None
        try:
            return TaskType[field.upper()]
        except KeyError as err:
            raise InvalidValueError(
                f'task type {field} is not recognized.') from err

    def __str__(self) -> str:
        data_type_name = "None"
        if self.data_type is not None:
            data_type_name = self.data_type.name
        task_name = "None"
        if self.task_type is not None:
            task_name = self.task_type.name
        return (f'{{Data type: {data_type_name}'
                f', Task: {task_name} }}')

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Task):
            if __value.data_type == self.data_type and __value.task_type == self.task_type:
                return True
        return False

    def validate(self, **kwargs) -> None:
        # test that problem_type maps to a dictionary containing exactly data_type and task_type
        errors: List[ConfigError] = []

        if isinstance(self._clause, dict):
            task_keys = set(self._clause.keys())
            if not ProblemDefKeySet.TASK.REQUIRED.issubset(task_keys):
                errors.append(MissingKeyError(
                    'Required keys missing in problem type: '
                    f'{ProblemDefKeySet.TASK.REQUIRED.difference(task_keys)}'))

            if not task_keys.issubset(ProblemDefKeySet.TASK.ALLOWED):
                errors.append(InvalidKeyError(
                    'Invalid key(s) in problem type: '
                    f'{task_keys.difference(ProblemDefKeySet.TASK.ALLOWED)}'
                ))

            if ProblemDefKeys.DATA_TYPE.value in self._clause:
                errmessages = DataType.validate(self._clause[ProblemDefKeys.DATA_TYPE.value])
                errors = errors + [InvalidValueError(err) for err in errmessages]

            if ProblemDefKeys.TASK_TYPE.value in self._clause:
                errmessages = TaskType.validate(self._clause[ProblemDefKeys.TASK_TYPE.value])
                errors = errors + [InvalidValueError(err) for err in errmessages]
        else:
            errors.append(ProblemDefTypeError(
                f'{ProblemDefKeys.TASK.value} must be a dict, '
                f'instead found {type(self._clause)}'))

        if len(errors) > 0:
            raise ValidationErrors(errors=errors)
