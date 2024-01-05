"""The wrangler is the central control object for all of AutonML."""
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Type, Union

from ..aggregators.impl.aggregate_ranker import AggregateRanker
from ..aggregators.impl.aggregator_auto import AggregatorCatalogAuto
from ..aggregators.impl.aggregator_catalog import AggregatorCatalog
from ..algorithms.impl.algorithm import AlgorithmCatalog
from ..algorithms.impl.algorithm_auto import AlgorithmCatalogAuto
from ..catalog.catalog import Catalog
from ..cross_validators.impl.cross_validator import CrossValidatorCatalog
from ..cross_validators.impl.cross_validator_auto import \
    CrossValidatorCatalogAuto
from ..executor.executor import Executor
from ..executor.simple.simple_executor import SimpleExecutor
from ..generator.bound_pipeline import BoundPipeline
from ..generator.designator import Designator
from ..generator.generator import Generator, GeneratorImpl
from ..instantiator.executable_pipeline import (ExecutablePipeline,
                                                PipelineResult,
                                                PipelineResults)
from ..instantiator.instantiator_factory import InstantiatorFactory
from ..metrics.impl.metric import Metric
from ..metrics.impl.metric_catalog import MetricCatalog
from ..metrics.impl.metric_auto import MetricCatalogAuto
from ..problem_def.problem_def import ProblemDefinition
from ..ranker.ranker import Ranker, Rankings
from ..ranker.ranker_impl import RankerImpl
from ..searcher.searcher import Searcher, SearcherImpl
from ..splitters.impl.splitter import SplitDataset, SplitterCatalog
from ..splitters.impl.splitter_auto import SplitterCatalogAuto
from ..templates.impl.pipeline_template import PipelineTemplate
from ..templates.impl.template import TemplateCatalog
from ..templates.impl.template_auto import TemplateCatalogAuto
from .dataset import Dataset
from .saver import Saver

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

# pylint: disable=too-many-instance-attributes,too-many-arguments


class Error(Exception):
    '''Base error for Wrangler.'''


class WranglerFailure(Error):
    '''Wrangler can not procede.'''


class ReassignmentError(Error):
    '''An attempt was made to assign a value more than once.'''


class WranglerResult():
    '''The results of Wrangler.wrangle.'''
    _split_dataset: SplitDataset
    _train_results: PipelineResults
    _test_results: Optional[PipelineResults]
    _rankings: Rankings

    def __init__(self,
                 split_dataset: SplitDataset,
                 train_results: PipelineResults,
                 test_results: Optional[PipelineResults],
                 rankings: Rankings):
        self._split_dataset = split_dataset
        self._train_results = train_results
        self._test_results = test_results
        self._rankings = rankings

    @property
    def split_dataset(self) -> SplitDataset:
        '''The ground truth and folds used to rank the pipelines.'''
        return self._split_dataset

    @property
    def train_results(self) -> PipelineResults:
        '''Predictions on train data, acquired using cross-validation.'''
        return self._train_results

    @property
    def test_results(self) -> Optional[PipelineResults]:
        '''Predictions on test data, if supplied in the problem definition.'''
        return self._test_results

    @property
    def rankings(self) -> Rankings:
        '''The rankings of all bound pipelines.'''
        return self._rankings

    @property
    def executable_pipelines(self) -> Dict[Designator, ExecutablePipeline]:
        '''Get all the executable pipelines.'''
        return self._train_results.executable_pipelines


class Wrangler():
    '''The wrangler is the central control object for all of AutonML.'''
    _bound_pipelines: Optional[Dict[Designator, BoundPipeline]] = None
    # These are all pipelines identified during the first run.
    _all_pipelines: Optional[Dict[Designator, ExecutablePipeline]] = None
    # This is a subset of _all_pipelines which will be the default
    # for subsequent fit, predict, and rank methods.
    _current_pipelines: Optional[Dict[Designator, ExecutablePipeline]] = None

    def __init__(
        self,
        problem_definition: ProblemDefinition,
        template_catalog: Optional[Type[TemplateCatalog]] = None,
        metric_catalog: Optional[Type[MetricCatalog]] = None,
        algorithm_catalog: Optional[Type[AlgorithmCatalog]] = None,
        generator: Optional[Type[Generator]] = None,
        searcher: Optional[Type[Searcher]] = None,
        executor: Optional[Type[Executor]] = None,
        ranker: Optional[Type[Ranker]] = None,
        instantiator_factory: Optional[Type[InstantiatorFactory]] = None,
        splitter_catalog: Optional[Type[SplitterCatalog]] = None,
        validator_catalog: Optional[Type[CrossValidatorCatalog]] = None,
        saver: Optional[Type[Saver]] = None,
        aggregator_catalog: Optional[Type[AggregatorCatalog]] = None,
    ):
        # TODO(Merritt): initialize the logger
        # instantiate default components only if input is None
        self._pd = problem_definition
        self._metric_catalog = (metric_catalog or MetricCatalogAuto)()
        self._algorithm_catalog = (algorithm_catalog or AlgorithmCatalogAuto)()
        self._generator = (generator or GeneratorImpl)(
            algorithm_catalog=self._algorithm_catalog,
            problem_definition=self._pd)
        self._template_catalog = (template_catalog or TemplateCatalogAuto)(
            algorithm_catalog=self._algorithm_catalog,
            generator=self._generator
        )
        self._searcher = (searcher or SearcherImpl)(hyperparams=self._pd.hyperparams)
        self._executor = (executor or SimpleExecutor)()
        self._ranker = (ranker or RankerImpl)()
        self._splitter_catalog = (splitter_catalog or SplitterCatalogAuto)(
            cv_config=self._pd.cross_validation_config)
        self._validator_catalog = (validator_catalog or CrossValidatorCatalogAuto)()
        self._aggregator_catalog = (aggregator_catalog or AggregatorCatalogAuto)()
        self._saver = None
        # If there is no output path, we'll output no files.
        if self._pd.output.path is not None:
            self._saver = (saver or Saver)(self._pd.output)
        self._instantiator_factory = (
            instantiator_factory or InstantiatorFactory)(
                saver=self._saver)

    @property
    def aggregator_catalog(self) -> AggregatorCatalog:
        '''Query and register aggregators'''
        return self._aggregator_catalog

    @property
    def algorithm_catalog(self) -> AlgorithmCatalog:
        '''Query and register algorithms'''
        return self._algorithm_catalog

    @property
    def metric_catalog(self) -> Catalog[Metric]:
        '''Query and register metrics'''
        return self._metric_catalog

    @property
    def template_catalog(self) -> TemplateCatalog:
        '''Query and register templates'''
        return self._template_catalog

    @property
    def generator(self) -> Generator:
        '''Generates bound pipelines from templates.'''
        return self._generator

    @property
    def ranker(self) -> Ranker:
        '''Ranks the results of running pipelines.'''
        return self._ranker

    def load_train_dataset(self) -> Dataset:
        '''Load self._pd.dataset()'''
        return self._pd.dataset_config.load_train()

    def load_test_dataset(self) -> Optional[Dataset]:
        '''Load self._pd.dataset()'''
        return self._pd.dataset_config.load_test()

    def dataset(self, data: Any, **kwargs) -> Dataset:
        '''Load in-memory data into a Dataset object, stored at key 'key'.'''
        return self._pd.dataset_config.dataset(data, **kwargs)

    def lookup_templates(self) -> Dict[str, PipelineTemplate]:
        '''Look up the templates that match the problem definition.'''
        task = self._pd.task
        data_type = "None"
        if task.data_type is not None:
            data_type = task.data_type.name
        task_type = "None"
        if task.task_type is not None:
            task_type = task.task_type.name

        return self._template_catalog.lookup_by_both(
            data_type=[data_type], task=[task_type])

    def train_all_results(self,
                          results: PipelineResults,
                          dataset: Dataset) -> PipelineResults:
        '''Instantiate and train all pipelines in results.

        Note that we do NOT calculate new predictions.
        '''
        retval = PipelineResults()
        pipelines: Dict[Designator, ExecutablePipeline] = {}

        for des, result in results.items():
            pipelines[des] = self._instantiator_factory.instantiate(
                kind=self._executor.kind,
                pipeline=result.bound_pipeline)

        self._executor.fit(
            dataset=dataset,
            pipelines=pipelines)

        for des, pipe in pipelines.items():
            retval[des] = PipelineResult(
                prediction=results[des].prediction,
                split_dataset=results[des].split_dataset,
                executable_pipeline=pipe)

        return retval

    def _predict_test_data(self,
                           executable_pipelines: Dict[Designator, ExecutablePipeline]
                           ) -> Optional[PipelineResults]:
        '''Run the executor again on test data to get test predictions,
            if test data is supplied in the problem definition.

        (Currently runs all pipelines, may eventually run x best ones)'''
        assert self._bound_pipelines is not None, (
            'BUG: wrangle_test() called with no bound pipelines.')

        test_dataset = self.load_test_dataset()

        if test_dataset is None:
            return None

        test_predictions = self._executor.predict(
            dataset=test_dataset,
            pipelines=executable_pipelines)
        return PipelineResults(test_predictions)

    def fit_predict_rank(self) -> WranglerResult:
        '''Do all the autoML things.'''
        train_dataset = self.load_train_dataset()

        templates = self.lookup_templates()
        if len(templates) == 0:
            raise WranglerFailure(f'found no templates for {self._pd.task}')
        logging.info('Found %d templates', len(templates))
        print(f'Found {len(templates)} templates')

        gen_result = self._generator.generate_all(templates)
        self._bound_pipelines = self._searcher.bind_all(gen_result)
        logging.info('Generated %d bound pipelines', len(self._bound_pipelines))
        print(f'Generated {len(self._bound_pipelines)} bound pipelines')

        task = self._pd.task
        assert task.task_type is not None, (
            'BUG: missing task should have been caught in validation.')
        splitters = self._splitter_catalog.lookup_by_tag_and(**{
            'task': task.task_type.name,
            'data_type': task.data_type.name,
        })
        if not splitters:
            splitters = self._splitter_catalog.lookup_by_tag_and(**{
                'default': 'true'
            })
        assert len(splitters) == 1, f'BUG: More than one splitter returned for {task}: {splitters}'
        splitter = list(splitters.values())[0]
        split_data = splitter.split(
            dataset=train_dataset,
            train_frac=self._pd.dataset_config.train_fraction,
            **self._pd.cross_validation_config.splitter_hyperparams
        )
        logging.info('Split dataset into %d folds.', len(split_data.folds))
        print(f'Split dataset into {len(split_data.folds)} folds.')

        cross_validator = self._validator_catalog.lookup_by_name('k_fold_cross_validator')
        cross_validator_results = PipelineResults(cross_validator.validate_pipelines(
            split_dataset=split_data,
            bound_pipelines=self._bound_pipelines,
            instantiator=self._instantiator_factory,
            executor=self._executor))

        metrics = self._metric_catalog.lookup_metrics(self._pd)
        print(f'Got {len(metrics)} metrics.')
        rankings = self._ranker.rank(
            results=cross_validator_results,
            metrics=metrics,
            ground_truth=split_data.ground_truth)
        logging.info('Rankings: %s', [str(rank) for rank in rankings])

        methods = [self._aggregator_catalog.lookup_by_name(method)
                   for method in self._pd.aggregation.method]
        new_rankings = AggregateRanker(methods=methods,
                                       rankings=rankings,
                                       results=cross_validator_results)()
        rankings.update(new_rankings)
        print(f'Added {len(new_rankings)} aggregate rankings.')

        train_results = self.train_all_results(
            results=cross_validator_results,
            dataset=train_dataset)

        if self._all_pipelines is None:
            self._all_pipelines = train_results.executable_pipelines
            self._current_pipelines = self._all_pipelines

        if self._saver is not None:
            self.save(train_results)

        test_results = self._predict_test_data(train_results.executable_pipelines)

        return WranglerResult(
            split_dataset=split_data,
            train_results=train_results,
            test_results=test_results,
            rankings=rankings)

    def save(self, train_results: PipelineResults) -> Dict[Designator, Path]:
        '''Save all the models and all the pipelines.'''
        assert self._saver is not None, 'BUG: Only call save if there is a saver.'
        retval: Dict[Designator, Path] = {}
        model_paths = self._saver.save_models(train_results.executable_pipelines)
        for kind in self._pd.instantiations:
            instantiatior = self._instantiator_factory.build(kind)
            for des, result in train_results.items():
                retval[des] = instantiatior.save(result.bound_pipeline, model_paths)
        return retval

    def fit(self,
            dataset: Dataset,
            pipelines: Optional[Dict[Designator, ExecutablePipeline]] = None
            ) -> Dict[Designator, ExecutablePipeline]:
        '''Fit the given pipelines with a new dataset.

        If no pipelines are specified, use the current set.
        '''
        if pipelines is None:
            pipelines = self._current_pipelines

        # Reinstantiate all the pipelines with clean models.
        assert pipelines is not None, (
            'BUG: fit called with None current pipelines'
        )
        for des, pipeline in pipelines.items():
            pipelines[des] = self._instantiator_factory.instantiate(
                kind=self._executor.kind,
                pipeline=pipeline.bound)

        self._executor.fit(
            dataset=dataset,
            pipelines=pipelines)

        return pipelines

    def predict(self,
                new_data: Dataset,
                trained_pipelines: Optional[
                    Dict[Designator, ExecutablePipeline]] = None) -> PipelineResults:
        '''Predict on new test data that was not supplied in the problem definition.'''
        if trained_pipelines is None:
            trained_pipelines = self._current_pipelines
        assert trained_pipelines is not None, (
            'BUG: predict called with None current pipelines.'
        )
        pipeline_errors: List[str] = []
        for des, pipe in trained_pipelines.items():
            if pipe.kind != self._executor.kind:
                pipeline_errors.append(
                    f'Pipeline {des} has incorrect ExecutorKind {pipe.kind}; '
                    f'expected {self._executor.kind}. \n')
            elif not pipe.trained:
                pipeline_errors.append(
                    f'Pipeline {des} is untrained. \n')

        if len(pipeline_errors) > 0:
            raise WranglerFailure(
                'Bad pipeline(s) provided to predict(): \n'
                f'{"".join(pipeline_errors)}')

        results = self._executor.predict(dataset=new_data, pipelines=trained_pipelines)
        return PipelineResults(results)

    def set_current(self, *args: str) -> None:
        '''Set the current set of pipelines to work with by name.

        If no arguments are given, reset to the full set of pipelines
        identified in the last fit_predict_rank.
        '''
        if len(args) == 0:
            self._current_pipelines = self._all_pipelines
            return
        if self._all_pipelines is None:
            self._current_pipelines = None
            return
        self._current_pipelines: Dict[Designator, ExecutablePipeline] = {
            Designator(des): self._all_pipelines[Designator(des)]
            for des in args
        }

    def rank(self,
             results: PipelineResults,
             metrics: Optional[Iterable[Union[str, Metric]]] = None,
             ground_truth: Optional[Dataset] = None) -> Rankings:
        '''Rank a set of pipeline results.

        If no metrics are provided, uses the ones from the problem definition

        If no ground truth is provided, attempts to infer it using the SplitDataset
        associated with an arbitrary PipelineResult.
        '''
        metrics_for_ranker: Dict[str, Metric] = {}
        if metrics is None:
            metrics_for_ranker = self._metric_catalog.lookup_metrics(self._pd)
        else:
            for m in metrics:
                if isinstance(m, Metric):
                    metrics_for_ranker[m.name] = m
                    continue
                metrics_for_ranker[m] = self._metric_catalog.lookup_by_name(m)

        if ground_truth is None:
            ground_truth = results.infer_ground_truth()

        return self.ranker.rank(results=results,
                                metrics=metrics_for_ranker,
                                ground_truth=ground_truth)
