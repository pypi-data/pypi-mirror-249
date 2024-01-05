'''Holds configuration information for aggregation.'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from typing import Any, Dict, List

from ..wrangler.constants import ProblemDefKeys

from .config_component import ConfigComponent, ConfigError


class AggregationError(ConfigError):
    '''Accummulating error for rank aggregation parsing.'''

    errors: List[ConfigError]

    def __init__(self, errors: List[ConfigError]):
        super().__init__(f'At least one validation error occured: {errors!r}')
        self.errors = errors


class AggregationConfig(ConfigComponent):
    '''Holds configuration for rank aggregation.

    If this clause is missing, we do not do rank aggregation.
    '''
    _method: List[str]

    def __init__(self, clause: Dict[str, Any]):
        super().__init__(clause=clause)
        method = self._get_with_default(ProblemDefKeys.METHOD, dflt=[])
        if method is not None:
            if not isinstance(method, list):
                assert isinstance(method, str)
                method = [method]
        self._method = method
        self.validate()

    @property
    def method(self) -> List[str]:
        '''Returns the aggregation method(s).'''
        return self._method

    def validate(self, **kwargs) -> None:
        pass
