'''Contains ProblemDefinition'''
import json
import textwrap
from typing import Any, Dict, List, Optional, Union

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import pandas as pd
from pandas import DataFrame

from ..dataset_formats.impl.dataset_config import (DatasetConfig,
                                                   DatasetFileError,
                                                   DatasetConfigError)
from ..dataset_formats.impl.dataset_format_catalog import (DatasetFormatCatalog,
                                                           DatasetFormatCatalogAuto)
from ..executor.executor_kind import ExecutorKind
from ..wrangler.constants import ProblemDefKeys, ProblemDefKeySet, Defaults
from ..wrangler.dataset import Metadata, RoleName

from .aggregation_config import AggregationConfig, AggregationError
from .cross_validation_config import CrossValidationConfig
from .config_component import ConfigComponent, ConfigError, ParsingErrors
from .config_component import MissingKeyError
from .config_component import InvalidKeyError, ValidationErrors
from .config_component import InvalidValueError, ProblemDefTypeError
from .hyperparam_config import HyperparamConfig, HyperparamError
from .metric_config import MetricConfig, MetricConfigError
from .output_config import OutputConfig
from .task import TaskType, Task

# pylint: disable=too-many-branches,too-many-statements


class ProblemDefinition(ConfigComponent):
    '''Represents information needed to define an AutoML run'''
    _task: Optional[Task] = None

    _aggregation_config: Optional[AggregationConfig] = None
    _cross_validation_config: Optional[CrossValidationConfig] = None
    _dataset_config: Optional[DatasetConfig] = None
    _metric_configs: Optional[Dict[str, MetricConfig]] = None
    _hyperparam_config: Optional[HyperparamConfig] = None
    _output_config: Optional[OutputConfig] = None

    _data_formats_catalog: Optional[DatasetFormatCatalog] = None

    def __init__(self,
                 problem_def: Union[str, Dict[str, Any]],
                 train_df: Optional[DataFrame] = None,
                 test_df: Optional[DataFrame] = None,
                 data_formats_catalog: Optional[DatasetFormatCatalog] = None):

        if isinstance(problem_def, str):
            problem_def = self._parse_json(pdef=problem_def)
        super().__init__(clause=remove_comments(problem_def))
        self._data_formats_catalog = data_formats_catalog or DatasetFormatCatalogAuto()

        errors: List[ConfigError] = []

        try:
            self._task = Task(self._get(
                ProblemDefKeys.TASK))
        except KeyError as err:
            errors.append(InvalidKeyError(err))

        try:
            clause = self._get(ProblemDefKeys.DATASET)
            self._dataset_config = self._data_formats_catalog.build(
                clause=clause,
                task=self._task,
                train_df=train_df,
                test_df=test_df
            )
        except (KeyError,  # Missing field names, bad column name, bad role name
                FileNotFoundError,  # Missing csv
                TypeError,  # Malformed json.
                pd.errors.ParserError,  # Train file is not parsable.
                IndexError  # Column id out of range.
                ) as err:
            errors.append(DatasetConfigError(err))
        except DatasetConfigError as err:  # Train dataframe not provided for MemoryDatasetConfig
            errors.append(err)

        try:
            self._cross_validation_config = CrossValidationConfig(self._get_with_default(
                ProblemDefKeys.CROSS_VALIDATION, dflt={}))
        except KeyError as err:
            errors.append(InvalidKeyError(err))

        try:
            metrics_clause = self._get_with_default(ProblemDefKeys.METRICS, dflt={})
            self._metric_configs = {name: MetricConfig(clause={name: info})
                                    for name, info in metrics_clause.items()}
        except MetricConfigError as err:
            errors.append(err)

        try:
            hyperparam_clause = self._get_with_default(ProblemDefKeys.HYPERPARAMS, dflt=[])
            self._hyperparam_config = HyperparamConfig(
                clause={ProblemDefKeys.HYPERPARAMS.value: hyperparam_clause})
        except HyperparamError as err:
            errors.extend(err.errors)

        try:
            output_clause = self._get_with_default(ProblemDefKeys.OUTPUT, dflt={})
            self._output_config = OutputConfig(output_clause)
            # TODO(piggy): Confirm that OutputConfig calls its own validate()
            # and drop this call.
            self._output_config.validate()
        except ValidationErrors as err:
            errors.extend(err.errors)

        try:
            aggregation_clause = self._get_with_default(ProblemDefKeys.AGGREGATION, dflt={})
            self._aggregation_config = AggregationConfig(aggregation_clause)
        except AggregationError as err:
            errors.extend(err.errors)

        try:
            # This is where we do validation between sections.
            self.validate()
        except ValidationErrors as err:
            errors.extend(err.errors)

        if len(errors) > 0:
            raise ValidationErrors(errors)

    def _parse_json(self, pdef: str) -> Dict[str, Any]:
        '''Attempts to interpret pdef as a JSON string or path to JSON file.

        If neither succeeds, raises ParsingErrors.
        '''
        errors: List[ConfigError] = []

        try:
            retval = json.loads(pdef)
            return retval
        except json.decoder.JSONDecodeError as err:
            errors.append(ConfigError(err))

        try:
            with open(pdef, 'r', encoding='utf8') as f:
                retval = json.load(f)
            return retval
        except FileNotFoundError as err:
            errors.append(ConfigError(err))
        except json.decoder.JSONDecodeError as err:
            errors.append(ConfigError(err))

        errors.insert(0, ConfigError(
            'String provided could not be parsed as JSON or path to JSON file.'))
        raise ParsingErrors(errors=errors)

    def __str__(self):
        return textwrap.dedent(f'''
            problem_type={self.task}
            dataset_config={self.dataset_config}
        ''')

    def validate(self, **kwargs) -> None:
        errors: List[ConfigError] = []
        keys = set(self._clause.keys())
        if not ProblemDefKeySet.REQUIRED.issubset(keys):
            errors.append(MissingKeyError(
                'Required keys missing in problem definition: '
                f'{ProblemDefKeySet.REQUIRED.difference(keys)}'))
        if not keys.issubset(ProblemDefKeySet.ALLOWED):
            errors.append(InvalidKeyError(
                'Invalid key(s) in problem definition: '
                f'{keys.difference(ProblemDefKeySet.ALLOWED)}'))

        if self._task is not None:
            try:
                self.task.validate()
            except ValidationErrors as err:
                errors.extend(err.errors)

        if self._dataset_config is not None:
            try:
                self.dataset_config.validate()
            except ValidationErrors as err:
                errors.extend(err.errors)

        if self._task is not None and self._dataset_config is not None:
            try:
                self._validate_task_dataset()
            except ValidationErrors as err:
                errors.extend(err.errors)
            except ConfigError as err:
                errors.append(err)

        if self._metric_configs is not None:
            for metric_config in self._metric_configs.values():
                try:
                    metric_config.validate()
                except MetricConfigError as err:
                    errors.append(err)

        if self._cross_validation_config is not None \
                and self._dataset_config is not None \
                and self._task is not None:
            # we need information about the dataset in order to sanity check
            #   cross-validation settings (i.e., 0 < k <= total number of rows in dataframe)
            try:
                pass
                # train_df = self._dataset_config.load_train().dataframe
                # self._cross_validation_config.validate(df_row_count=train_df.shape[0])
            except ProblemDefTypeError as err:
                errors.append(err)
            except InvalidValueError as err:
                errors.append(err)

        if len(errors) > 0:
            raise ValidationErrors(errors)

    def _validate_task_dataset(self) -> None:
        errors: List[ConfigError] = []
        if self.task.task_type == TaskType.FORECASTING:
            if RoleName.TIME not in self.dataset_config.roles:
                errors.append(
                    DatasetFileError(
                        'Dataset for forecasting problem must have a time column.\n'
                        f'Found roles: {self.dataset_config.roles!r}'
                    )
                )

            if self.dataset_config.forecasting is None:
                errors.append(
                    MissingKeyError(
                        'Dataset config for forecasting problem must have a forecasting clause.'
                    )
                )

        if len(errors) > 0:
            raise ValidationErrors(errors=errors)

    @property
    def dataset_config(self) -> DatasetConfig:
        '''The dataset description.'''
        assert self._dataset_config is not None, (
            'BUG: attempt to access dataset_config but it is None.')
        return self._dataset_config

    @property
    def task(self) -> Task:
        '''Explains what kind of problem we're solving.

        This affects the selection of pipeline templates and models.
        '''
        assert self._task is not None, (
            'BUG: attempt to access problem_type but it is None.')
        return self._task

    @property
    def metric_configs(self) -> Dict[str, MetricConfig]:
        '''Names and other information, if applicable, about all the metrics for this problem.

        If there are no metrics specified, will return an empty list, in which case the wrangler is
        responsible for using a default metric based on the problem type.
        '''
        assert self._metric_configs is not None, (
            'BUG: attempt to access metric_config but it is None.')
        return self._metric_configs

    @property
    def cross_validation_config(self) -> CrossValidationConfig:
        '''
        Get configuration information for cross-validation.
        '''
        assert self._cross_validation_config is not None, (
            'BUG: attempt to access cross_validation_config but it is None.'
        )

        return self._cross_validation_config

    @property
    def instantiations(self) -> List[ExecutorKind]:
        '''The user requests these kinds of output pipeline instantiations.

        A missing instantions clause defaults to all available kinds.
        An empty instantions clause disables instantiation.
        '''
        inst = self._get_with_default(ProblemDefKeys.OUTPUT, ProblemDefKeys.INSTATIATIONS,
                                      dflt=Defaults.INSTANTIANTIONS)

        return [ExecutorKind(i.lower()) for i in inst]

    @property
    def output(self) -> OutputConfig:
        '''All the configuration about things to output.'''
        assert self._output_config is not None, (
            'BUG: empty output session should be handled in constructor.'
        )
        return self._output_config

    @property
    def metadata(self) -> Metadata:
        '''Package config metadata needed by some models.'''
        return self.dataset_config.metadata

    @property
    def hyperparams(self) -> HyperparamConfig:
        '''Configuration for all hyperparam overrides.'''
        assert self._hyperparam_config is not None, (
            'BUG: self._hyperparam_config is supposed to be set in __init__().')
        return self._hyperparam_config

    @property
    def aggregation(self) -> AggregationConfig:
        '''Configuration for rank aggregation.

        The only valid entry is "method" which gives
        the catalog name of a rank aggregation method.
        See the top level "aggregators" directory.
        '''
        assert self._aggregation_config is not None, (
            'BUG: self._aggregation_config is supposed to be set in __init__().')
        return self._aggregation_config


def remove_comments(entry: Any) -> Any:
    '''Remove '_comments' fields from every dict inside an anonymous object.'''
    if isinstance(entry, dict):
        retval = {
            k: remove_comments(v)
            for k, v in entry.items()
            if k != '_comments'
        }
        return retval
    if isinstance(entry, list):
        return [remove_comments(v) for v in entry]
    return entry
