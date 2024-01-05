''' Base class for dataset configs that use dataframes '''
import abc
from typing import Any, Optional, List, Union

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import pandas as pd

from ...problem_def.config_component import ConfigError, ValidationErrors
from .dataset_config import DatasetConfig, DatasetConfigError, ParsingErrors, DatasetFileError
from ...problem_def.task import TaskType
from ...wrangler.dataset import Dataset, Column, RoleName, DatasetKeys


class DataframeDatasetConfig(DatasetConfig, metaclass=abc.ABCMeta):
    '''Base class for dataset configs that use dataframes
    '''
    _train_cols: pd.DataFrame

    @abc.abstractmethod
    def load_train(self) -> Dataset:
        ...

    @abc.abstractmethod
    def load_test(self) -> Optional[Dataset]:
        ...

    def dataset(self,
                data: Any,
                key: Union[str, DatasetKeys] = DatasetKeys.DATAFRAME,
                cols: Optional[List[str]] = None,
                roles: Optional[List[Union[RoleName, str]]] = None,
                **kwargs) -> Dataset:
        '''Load a Dataset object, by placing data at the supplied key.

        As of 2023-12-04 we only know how to handle things we can turn into a pandas DataFrame.

        Args:
          data:
            Dataframe or object that can be turned into one.
          key:
            The key for the data in the dataset. Defaults to "dataframe".
          cols:
            If set, only selects supplied column(s).
            Will take union with roles if both are specified.
          roles:
            If set, only selects columns with supplied role(s).
            Will take union with cols if both are specified.
        '''

        retval = Dataset(metadata=self.metadata)

        data_df = pd.DataFrame(data)

        # Trim to selected columns if either cols or roles is set.
        cols_to_select = set()
        if cols is not None:
            cols_to_select.update(cols)
        if roles is not None:
            for role in roles:
                cols_to_select.update(
                    c.name for c in self.cols_with_role(role))
        if cols_to_select:
            data_df = data_df[sorted(cols_to_select)]

        if isinstance(key, str):
            key = DatasetKeys[key.upper()]

        retval[key.value] = data_df
        return retval

    def validate(self, **kwargs) -> None:
        '''Look for errors by comparing the problem definition JSON to the
            dataframe that was read.'''
        super().validate(**kwargs)
        errors: List[ConfigError] = []
        # TODO(Merritt): add test case for this validation error
        for rolename, cols in self._roles.items():
            for col in cols:
                if col.name not in self._train_cols.columns:
                    errors.append(DatasetFileError(
                        f'Column {col.name} specified under role {rolename}'
                        ' not found among columns in dataset. '
                        f'Found: {self._train_cols.columns}'))
        if len(errors) != 0:
            raise ValidationErrors(errors)

    def _read_roles(self) -> None:
        '''Flesh out roles based on the actual dataset.

        Give all unassigned columns the Attribute role.
        '''
        assigned_colnames: List[str] = []
        errors: List[DatasetConfigError] = []
        for cols in self.roles.values():
            for col in cols:
                assert col.name is not None
                assigned_colnames.append(str(col.name))

        unassigned_colnames = list(set(self._train_cols.columns) - set(assigned_colnames))
        unassigned_cols = []
        for colname in unassigned_colnames:
            unassigned_cols.append(Column(colname))

        # TODO(Merritt): Deal with situation where the user manually specifies a col as attribute
        self._roles[RoleName.ATTRIBUTE] = unassigned_cols

        if len(errors) != 0:
            raise ParsingErrors(errors)

    def _prune_target(self, retval: Dataset) -> Dataset:
        '''
        remove target col if it is in data; test data shouldn't have target
        keep target for forecasting problems
        '''

        if self._task is None or self._task.task_type != TaskType.FORECASTING:
            if self.target is not None and self.target.name in retval.dataframe.columns:
                new_data = retval.dataframe.drop([self.target.name], axis=1)
                retval.dataframe = new_data

        return retval
