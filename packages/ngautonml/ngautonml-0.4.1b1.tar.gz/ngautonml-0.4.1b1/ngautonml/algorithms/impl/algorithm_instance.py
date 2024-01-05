'''Holds an instance of a model.'''
import abc
from typing import Any
from typing_extensions import Protocol

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from ...wrangler.dataset import Dataset

from .algorithm import Algorithm


class Error(Exception):
    '''Base error class for AlgorithmInstance.'''


class DatasetError(Error):
    '''Something is malformed about the dataset.'''


class AlgorithmInstance(metaclass=abc.ABCMeta):
    '''Holds an instance of an algorithm as made by the instantiator.'''
    _algorithm: Algorithm

    def __init__(self, parent: Algorithm):
        self._algorithm = parent

    @abc.abstractmethod
    def predict(self, dataset: Dataset) -> Dataset:
        '''Apply model to input dataset to create output.

        This may require that the model is fit (self.trained == True) before it is called.
        '''

    @property
    def catalog_name(self) -> str:
        '''The catalog name of our algorithm.'''
        return self._algorithm.name


class Constructor(Protocol):
    '''Match the signature of a generic model constructor.'''
    def __call__(self, **kwargs: Any) -> Any:
        ...


def not_implemented(**kwargs):
    '''A constructor must be specified in a subclass'''
    raise NotImplementedError('Implementation must specify a model _constructor')
