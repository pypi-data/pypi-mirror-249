'''Holds configuration information for cross-validation.'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from typing import Dict, Any, Optional, List

from ..wrangler.constants import ProblemDefKeys, Defaults

from .config_component import ConfigComponent, InvalidValueError


class CrossValidationConfig(ConfigComponent):
    '''
    Holds configuration information for cross-validation.
    '''

    def __init__(self, clause: Dict[str, Any], parents: Optional[List[str]] = None):
        parents = self._add_parent(parents, ProblemDefKeys.CROSS_VALIDATION.value)
        super().__init__(clause=clause, parents=parents)

    @property
    def k(self) -> Optional[int]:
        '''get k fold'''
        field = self._get_with_default(
            ProblemDefKeys.K.value,
            dflt=None
        )

        return field

    @property
    def seed(self) -> int:
        '''Get default random seed or one set by'''
        field = self._get_with_default(
            ProblemDefKeys.SEED.value,
            dflt=Defaults.SEED
        )
        return field

    @property
    def splitter_hyperparams(self) -> Dict[str, Any]:
        '''get splitter hyperparams'''
        retval = {}

        if self.k:
            retval['n_splits'] = self.k

        return retval

    def validate(self, **kwargs) -> None:
        if self.k is None:
            return

        # single fold cross-validation does not make sense
        #   because we need data outside the fold to train on
        if self.k < 2:
            raise InvalidValueError(
                f'k must be an integer greater than 1, but we got {self.k} instead.')

        df_row_count = 'df_row_count'

        if df_row_count not in kwargs:
            return

        count = kwargs[df_row_count]

        if self.k > count:
            raise InvalidValueError(
                f'k must not be greater than the total number of rows in the dataframe.'
                f'Instead we got: k = {self.k}, row count = {count}'
            )
