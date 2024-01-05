'''These are the kinds of executable pipelines for different executors.'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import abc
from typing import Dict, Optional

import pandas as pd

from ..executor.cucumber import JarOfCucumbers
from ..executor.executor_kind import ExecutorKind
from ..generator.bound_pipeline import BoundPipeline, BoundPipelineStub
from ..generator.designator import Designator
from ..splitters.impl.splitter import SplitDataset
from ..wrangler.constants import OutputColName
from ..wrangler.dataset import Dataset, DatasetKeys


class PipelineExecutionError(Exception):
    '''Base class for errors thrown by the executor'''


class FitError(PipelineExecutionError):
    '''A pipeline threw an error during fit.'''


class PredictError(PipelineExecutionError):
    '''A pipeline threw an error during predict'''


class ExecutablePipeline(metaclass=abc.ABCMeta):
    '''Base class for all executable pipelines.'''
    _kind: ExecutorKind
    _pipeline: BoundPipeline
    _trained: bool = False
    _fit_error: Optional[FitError] = None

    @property
    def kind(self):
        '''What kind of executor are we built for?

        e.g. json, python_script, jupyter_notebook, AirFlow Class, stub
        '''
        return self._kind

    @property
    def name(self) -> str:
        '''The name of the underlying pipeline'''
        return self._pipeline.name

    @property
    def designator(self) -> Designator:
        '''The designator for this instance of an executable pipeline

        Overriding classes should derive this from the bound pipeline.
        '''
        return Designator(self.name)  # TODO(piggy): This should be a .-separated path.

    @property
    def bound(self) -> BoundPipeline:
        '''The bound pipeline this was compiled from'''
        return self._pipeline

    @property
    def trained(self) -> bool:
        '''Is this pipeline trained?'''
        return self._trained

    def set_trained(self):
        '''Force the pipeline to trained.'''
        self._trained = True

    @abc.abstractmethod
    def fit(self, dataset: Dataset) -> JarOfCucumbers:
        '''Fit models to dataset.

        Args:
            dataset: The training dataset.

        Returns:
            A JarOfCucumbers
            (mapping from step designators to cucumbers for each step).
        '''

    @abc.abstractmethod
    def predict(self, dataset: Dataset) -> 'PipelineResult':
        '''Get predictions for this pipeline on this dataset.'''

    @abc.abstractmethod
    def cucumberize_all(self) -> JarOfCucumbers:
        '''Cucumberize all steps that hold algorithms, and return the result.

        This has the same output as fit() but requires the pipeline to be fit already.
        '''

    def __str__(self):
        return f'{{{self._pipeline.designator}, executor: {self.kind}}}'


class ExecutablePipelineStub(ExecutablePipeline):
    '''stub'''
    _cucumbers: JarOfCucumbers

    def __init__(self,
                 kind: Optional[ExecutorKind] = None,
                 pipeline: Optional[BoundPipeline] = None,
                 trained: bool = False,
                 cucumbers: Optional[JarOfCucumbers] = None):
        self._kind = kind or ExecutorKind('stub_executor_kind')
        self._pipeline = pipeline or BoundPipelineStub(name='stub_pipeline')
        self._trained = trained
        self._cucumbers = cucumbers or JarOfCucumbers({})

    def fit(self, dataset: Dataset) -> JarOfCucumbers:
        return JarOfCucumbers()

    def predict(self, dataset: Dataset) -> 'PipelineResult':
        return PipelineResult(prediction=dataset, executable_pipeline=self)

    def cucumberize_all(self) -> JarOfCucumbers:
        return self._cucumbers


class PipelineResultError(Exception):
    '''Base class for all errors associated with this file.'''


# TODO(Merritt): put this in own file
# (may need a separate InternalPipelineResult and ExternalPipelineResult)
class PipelineResult(metaclass=abc.ABCMeta):
    '''Base class for objects that represent the result of a pipeline run.

    At a minimum contains a pipeline that was run and a dataset resulting from that run.
    Subclasses may contain additional information.
    '''
    _prediction: Dataset
    _bound_pipeline: Optional[BoundPipeline] = None
    _executable_pipeline: Optional[ExecutablePipeline] = None
    _split_dataset: Optional[SplitDataset] = None

    def __init__(self,
                 prediction: Dataset,
                 bound_pipeline: Optional[BoundPipeline] = None,
                 executable_pipeline: Optional[ExecutablePipeline] = None,
                 split_dataset: Optional[SplitDataset] = None):

        if bound_pipeline is None:
            assert executable_pipeline is not None, (
                'BUG: both bound and executable pipelines are None'
                ' in PipelineResult instantiator.')

        self._prediction = prediction
        self._bound_pipeline = bound_pipeline
        self._executable_pipeline = executable_pipeline
        self._split_dataset = split_dataset
        if (self._split_dataset is not None
            and self._split_dataset.ground_truth is not None
                and DatasetKeys.PREDICTIONS.value in self._prediction):
            self._add_ground_truth()

    def _add_ground_truth(self) -> None:
        '''Display ground truth next to train predictions.'''
        assert self._split_dataset is not None
        assert self._split_dataset.ground_truth is not None
        assert isinstance(self.prediction[DatasetKeys.PREDICTIONS.value], pd.DataFrame), (
            'BUG: can only add ground truth to predictions if predictions is a dataframe. '
            f'instead found f{self.prediction[DatasetKeys.PREDICTIONS.value]}')

        if OutputColName.GROUND_TRUTH.value in self.prediction.predictions.columns:
            # Predictions dataframe already contains ground truth
            return
        gt_df = self._split_dataset.ground_truth[DatasetKeys.GROUND_TRUTH.value]
        assert isinstance(gt_df, pd.DataFrame), (
            'BUG: can only add ground truth to predictions if ground truth is a dataframe. '
            f'instead found {gt_df} of type {type(gt_df)}')
        target = self._split_dataset.ground_truth.metadata.target
        assert target is not None, (
            'BUG: attempt to add ground truth with no target.')
        new_df = self.prediction.predictions.copy(deep=True)
        # Align the ground truth with the prediction dataframe.
        new_df.reset_index(inplace=True, drop=True)
        gt_df.reset_index(inplace=True, drop=True)
        new_df[OutputColName.GROUND_TRUTH.value] = gt_df[target.name]
        self.prediction.predictions = new_df

    @property
    def prediction(self) -> Dataset:
        '''Dataset resulting from the pipeline run'''
        return self._prediction

    @property
    def bound_pipeline(self) -> BoundPipeline:
        '''Bound pipeline associated with this pipeline run.'''
        if self._executable_pipeline is not None:
            return self._executable_pipeline.bound
        assert self._bound_pipeline is not None, (
            'BUG: both bound and executable pipelines are None'
            ' in PipelineResult bound_pipeline property.')
        return self._bound_pipeline

    @property
    def executable_pipeline(self) -> Optional[ExecutablePipeline]:
        '''Trained executable pipeline associated with this pipeline run, if applicable.'''
        return self._executable_pipeline

    @property
    def split_dataset(self) -> Optional[SplitDataset]:
        '''Split dataset that was passed to the CrossValidator, if applicable'''
        return self._split_dataset

    def __str__(self) -> str:
        return f'pipeline: {self.bound_pipeline!s}\nprediction:\n{self.prediction!s}'

    def __repr__(self) -> str:
        return self.__str__()


class PipelineResults(Dict[Designator, PipelineResult]):
    '''Multiple PipelineResults identified by Designators.'''

    def _some_result(self) -> PipelineResult:
        '''Choose an arbitrary result and return it.'''
        return list(self.values())[0]

    def infer_ground_truth(self) -> Optional[Dataset]:
        '''Attempts to infer ground truth using an arbitrary PipelineResult.'''
        split_dataset = self._some_result().split_dataset
        if split_dataset is not None:
            return split_dataset.ground_truth
        return None

    @property
    def predictions(self) -> Dict[Designator, Dataset]:
        '''Datasets resulting from the pipeline runs'''
        return {k: v.prediction for k, v in self.items()}

    @property
    def bound_pipelines(self) -> Dict[Designator, BoundPipeline]:
        '''Bound Pipelines associated with the pipeline runs'''
        return {k: v.bound_pipeline for k, v in self.items()}

    @property
    def executable_pipelines(self) -> Dict[Designator, ExecutablePipeline]:
        '''Trained executable pipelines associated with the pipeline runs.

        Throws an error if not all runs have executable pipelines
        '''
        retval: Dict[Designator, ExecutablePipeline] = {}
        for des, pipe in self.items():
            pipeline = pipe.executable_pipeline
            if pipeline is None:
                raise PipelineResultError(
                    'Attempt to extract executable pipeline '
                    'from a PipelineResult that does not have one'
                    f' (designator: {pipe.bound_pipeline.designator}).')
            retval[des] = pipeline
        return retval

    def __str__(self) -> str:
        retval = 'Pipeline Results:\n'
        for pipe in self.values():
            retval = f'{retval}{pipe}\n'
        return retval
