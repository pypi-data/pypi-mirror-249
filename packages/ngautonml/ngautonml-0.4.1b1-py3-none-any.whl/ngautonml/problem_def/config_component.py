'''Base class for elements of the Problem Definition file'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import abc
import copy
from typing import Any, Dict, List, Optional, Union
from ..wrangler.constants import ProblemDefKeys


class ConfigError(BaseException):
    '''All errors thrown by problem definition modules'''


class ConfigDirectoryError(ConfigError, NotADirectoryError):
    '''A path given in the problem doc was not a directory, but should be.'''


class MissingKeyError(ConfigError, KeyError):
    '''We failed to find a given key in the problem doc.'''


class InvalidKeyError(ConfigError, KeyError):
    '''We found an invalid key in the problem doc.'''


class ProblemDefTypeError(ConfigError, TypeError):
    '''A value in the problem definition was the wrong type.'''


class InvalidValueError(ConfigError, ValueError):
    '''A value in the problem definition has the right type but is invalid.'''


class ParsingErrors(ConfigError):
    '''Error(s) thrown when problem definition JSON cannot be parsed'''

    def __init__(self, errors: List[ConfigError]):
        super().__init__(f'At least one parsing error occured: {errors!r}')
        self.errors = errors


class ValidationErrors(ConfigError):
    '''Problem definition JSON can be parsed, but is invalid in some other way.'''

    def __init__(self, errors: List[ConfigError]):
        super().__init__('At least one validation error occured:')
        self.errors = errors

    def __str__(self) -> str:
        retval_list1 = [str(arg) for arg in self.args]
        retval_list2 = [f'\t{repr(error)}' for error in self.errors]
        return '\n'.join(retval_list1 + retval_list2)


class ConfigComponent(metaclass=abc.ABCMeta):
    '''Base class for elements of the Problem Definition file

    This provides _get, _get_with_default, and _exists for
    use by config components.
    '''
    # pylint: disable=too-few-public-methods
    _parents: List[str]
    _clause: Dict[str, Any]

    def __init__(self, clause: Dict[str, Any], parents: Optional[List[str]] = None):
        if parents is None:
            parents = []
        self._parents = parents
        self._clause = clause

    def _add_parent(self,
                    parents: Optional[List[str]],
                    new_parent: str) -> List[str]:
        if parents is None:
            retval = []
        else:
            retval = parents.copy()
        retval.append(new_parent)
        return retval

    def _get(self, *args: Union[int, str, ProblemDefKeys]):
        '''for ex: call _get('metric', 'name') to get metric name'''
        here = self._clause
        so_far = []
        for k in args:
            if isinstance(k, ProblemDefKeys):
                k = k.value
            so_far.append(str(k))
            if isinstance(here, list):
                if not isinstance(k, int):
                    raise ProblemDefTypeError(
                        f'found a list at {".".join(self._parents + so_far[:-1])}, '
                        f'expected an integer at {".".join(self._parents + so_far)}')
                if not -len(here) < k < len(here):
                    raise MissingKeyError(f'Could not find the {k}th element of {here}')
            elif isinstance(here, dict):
                if k not in here:
                    raise MissingKeyError('Could not find '
                                          f'{".".join(so_far)}')
                assert isinstance(k, str), (
                    f'BUG: at _get {".".join(so_far)} we have a non-string key, {k!r} for {here!r}')
            here = here[k]

        return copy.deepcopy(here)

    def _get_with_default(self, *args: Union[int, str, ProblemDefKeys], dflt: Any) -> Any:
        if self._exists(*args):
            return self._get(*args)
        return dflt

    def _exists(self, *args: Union[int, str, ProblemDefKeys]) -> bool:
        '''for ex: call _exists('metric', 'name') to see if metric.name exists'''
        here = self._clause
        so_far = []
        for k in args:
            if isinstance(k, ProblemDefKeys):
                k = k.value
            so_far.append(str(k))
            if isinstance(here, list):
                if not isinstance(k, int):
                    raise ProblemDefTypeError(
                        f'found a list at {".".join(self._parents + so_far[:-1])}, '
                        f'expected an integer at {".".join(self._parents + so_far)}')
                if not -len(here) < k < len(here):
                    raise MissingKeyError(f'Could not find the {k}th element of {here}')
            elif isinstance(here, dict):
                if k not in here:
                    return False
                assert isinstance(k, str), (
                    f'BUG: at _exists {".".join(so_far)} we have a '
                    f'non-string key, {k!r} for {here!r}')
            here = here[k]
        return True

    @abc.abstractmethod
    def validate(self, **kwargs) -> None:
        '''Raise a ConfigError if something about the clause is invalid.'''
