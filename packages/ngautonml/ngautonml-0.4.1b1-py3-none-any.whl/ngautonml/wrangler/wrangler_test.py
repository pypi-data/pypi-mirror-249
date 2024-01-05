'''Tests for wrangler.py'''
import glob
import json
import os
from pathlib import Path
from typing import Dict

from numpy.random import RandomState
import pandas as pd
import pytest

from ..aggregators.impl.aggregator import AggregatorStub
from ..algorithms.impl.algorithm import Algorithm
from ..algorithms.impl.algorithm_auto import FakeAlgorithmCatalogAuto
from ..algorithms.impl.algorithm_instance import AlgorithmInstance
from ..algorithms.impl.fake_algorithm import FakeInstance
from ..executor.cucumber import Cucumber
from ..executor.executor import ExecutorStub
from ..executor.simple.simple_executor import SimpleExecutor
from ..generator.designator import Designator
from ..instantiator.executable_pipeline import (ExecutablePipeline,
                                                ExecutablePipelineStub,
                                                PipelineResult)
from ..problem_def.problem_def import ProblemDefinition
from ..templates.impl.pipeline_step import PipelineStep
from ..templates.impl.pipeline_template import PipelineTemplate
from ..templates.impl.template import TemplateCatalog

from .constants import Defaults
from .dataset import Dataset, RoleName
from .wrangler import Wrangler, WranglerFailure

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

# pylint: disable=missing-function-docstring,duplicate-code,protected-access,too-many-ancestors
# pylint: disable=missing-class-docstring,redefined-outer-name


class FakeExecutor(ExecutorStub):

    def predict(self,
                dataset: Dataset,
                pipelines: Dict[Designator, ExecutablePipeline]
                ) -> Dict[Designator, PipelineResult]:
        '''Use a list of pipelines to predict from a dataset.'''
        predictions = dataset.output()
        # create a dataframe with the shape we expect predictions to be:
        # 1 column (the target) and a number of rows equal to the size of the input
        predictions.predictions = pd.DataFrame({
            dataset.metadata.roles[RoleName.TARGET][0].name:
                range(0, dataset.dataframe.shape[0])})
        return {d: PipelineResult(executable_pipeline=p, prediction=predictions)
                for d, p in pipelines.items()}


MEMORY_PROBLEM_DEF = '''
{
    "dataset": {
        "config": "memory",
        "column_roles": {
            "target": {
                "name": "c"
            }
        }
    },
    "problem_type": {
        "task": "regression"
    },
    "cross_validation": {
        "k": 10
    },
    "metrics" : {
        "root_mean_squared_error" : {}
    },
    "hyperparams": ["disable_grid_search"]
}
'''

AGGREGATION_PROBLEM_DEF = '''
{
    "dataset": {
        "config": "memory",
        "column_roles": {
            "target": {
                "name": "c"
            }
        }
    },
    "problem_type": {
        "task": "regression"
    },
    "cross_validation": {
        "k": 10
    },
    "metrics": {
        "root_mean_squared_error" : {},
        "mean_squared_error": {},
        "mean_absolute_error": {}
    },
    "aggregation": {
        "method": ["method1", "method2"]
    },
    "hyperparams": ["disable_grid_search"]
}
'''


def memory_problem_def(has_test_data: bool = False,
                       has_aggregation: bool = False) -> ProblemDefinition:
    data = pd.DataFrame(
        {
            'a': range(1, 21),
            'b': range(1, 21),
            'c': range(1, 21)
        }
    )
    test_data = None
    if has_test_data:
        test_data = data

    problem_def = MEMORY_PROBLEM_DEF
    if has_aggregation:
        problem_def = AGGREGATION_PROBLEM_DEF

    return ProblemDefinition(
        problem_def=problem_def,
        train_df=data,
        test_df=test_data)


def test_init_default() -> None:
    '''Test the components that wrangler defaults to.'''
    dut = Wrangler(problem_definition=memory_problem_def())
    assert dut._generator.__class__.__name__ == "GeneratorImpl"
    assert dut._template_catalog.__class__.__name__ == "TemplateCatalogAuto"


def test_init_custom() -> None:
    '''Test that overriding components when initializing the wrangler works.'''
    dut = Wrangler(
        problem_definition=memory_problem_def(),
        executor=FakeExecutor,
        template_catalog=FakeTemplateCatalog)
    assert dut._executor.__class__.__name__ == "FakeExecutor"
    assert dut._template_catalog.__class__.__name__ == "FakeTemplateCatalog"

    # Testing that non-set arguments are still default
    assert dut._generator.__class__.__name__ == "GeneratorImpl"


def test_wrangler_dataset() -> None:
    '''Test wrangler.dataset(), which takes a dataframe and returns a
    dataset containing the dataframe with metadata matching the problem definition.'''
    problem_def = memory_problem_def()
    metadata = problem_def.metadata
    data = {
        'a': range(1, 31),
        'b': range(1, 31),
        'c': range(1, 31),
    }

    dut = Wrangler(
        problem_definition=problem_def,
        executor=FakeExecutor)

    got = dut.dataset(data)

    # Confirm that the dataframe matches
    pd.testing.assert_frame_equal(
        got.dataframe,
        pd.DataFrame(data))

    # Confirm that at least part of the metadata matches.
    assert got.metadata.roles == metadata.roles


def test_wrangler_split() -> None:
    problem_def = memory_problem_def()
    dut = Wrangler(
        problem_definition=problem_def,
        algorithm_catalog=FakeAlgorithmCatalogAuto,
        executor=FakeExecutor)

    train_result = dut.fit_predict_rank()

    # we expect 10 folds because k=10 was set in the problem definition
    assert len(train_result.split_dataset.folds) == 10
    # we expect each fold's validate set to have 2 rows,
    #    because there are 10 folds and the dataset is 20 rows long,
    #    and 2 columns, because it contains the attributes but not the target.
    assert train_result.split_dataset.folds[0].validate.dataframe.shape == (2, 2)
    # we expect each fold's train set to have 18 rows,
    #    because it is composed of 9 folds of 2 rows each,
    #    and 3 columns, becase it contains the attributes and the target.
    assert train_result.split_dataset.folds[0].train.dataframe.shape == (18, 3)
    # we expect the ground truth to have 20 rows,
    #    because it covers the whole dataset,
    #    and 1 col, because it only has the target.
    assert train_result.split_dataset.ground_truth is not None
    assert train_result.split_dataset.ground_truth.ground_truth.shape == (20, 1)


def test_fit_predict_rank() -> None:
    problem_def = memory_problem_def(has_test_data=True)

    dut = Wrangler(
        problem_definition=problem_def,
        algorithm_catalog=FakeAlgorithmCatalogAuto)

    got = dut.fit_predict_rank()

    # we expect pipelines to be named according to thier template (tabular regression)
    #    and the model that was chosen from thier query step.
    #    in the case of random forest regressor, wrangler will do grid search,
    #    and thus hyperparam values will also be in the designator.
    random_forest_des = Designator('tabular_regression@sklearn.ensemble.randomforestregressor:'
                                   'max_depth=None,min_samples_split=2')
    linear_regression_des = Designator('tabular_regression@sklearn.linear_model.linearregression')
    assert {random_forest_des, linear_regression_des} == set(got.executable_pipelines.keys())

    assert len(got.train_results) == 2  # 2 pipelines
    assert got.train_results.predictions[random_forest_des].predictions.shape == (20, 2)

    assert len(got.rankings) == 1  # 1 metric
    assert 'root_mean_squared_error' in got.rankings

    assert got.test_results is not None
    assert len(got.test_results) == 2  # 2 pipelines

    # executable pipelines associated with the test results should be identical
    assert set(got.executable_pipelines.keys()) == set(got.test_results.executable_pipelines.keys())

    assert got.test_results.predictions[random_forest_des].predictions.shape == (20, 1)


def test_fit_predict_rank_with_aggregation() -> None:
    problem_def = memory_problem_def(has_test_data=True, has_aggregation=True)

    dut = Wrangler(
        problem_definition=problem_def,
        algorithm_catalog=FakeAlgorithmCatalogAuto)

    dut.aggregator_catalog.register(AggregatorStub(name="method1"))
    dut.aggregator_catalog.register(AggregatorStub(name="method2"))

    got = dut.fit_predict_rank()

    assert len(got.rankings) == 5  # 3 metrics, and 2 aggregate metrics
    want = {
        'root_mean_squared_error', 'mean_squared_error', 'mean_absolute_error',
        'method1', 'method2'
    }
    assert want == set(got.rankings.keys())


class FakeTemplateCatalog(TemplateCatalog):
    '''fake, no templates'''


def memory_test_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            'a': range(1, 11),
            'b': range(1, 11)
        }
    )


def memory_train_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            'a': range(1, 21),
            'b': range(1, 21),
            'c': range(1, 21)
        }
    )


def test_predict() -> None:
    problem_def = memory_problem_def()
    executor = SimpleExecutor
    alg_catalog = FakeAlgorithmCatalogAuto
    dut = Wrangler(
        problem_definition=problem_def,
        executor=executor,
        algorithm_catalog=alg_catalog)
    got = dut.fit_predict_rank()

    fake_des = Designator('fake_des')

    testset = dut.dataset(memory_test_df())
    result = list(got.train_results.values())[0]
    pipeline = result.executable_pipeline
    assert pipeline is not None
    test_got = dut.predict(
        new_data=testset,
        trained_pipelines={fake_des: pipeline})
    prediction_df = test_got[fake_des].prediction.predictions

    # we expect 10 rows (length of test dataframe) and 1 col (target)
    assert prediction_df.shape == (10, 1)
    # we expect to be able to predict perfectly since test data is identical to train data.
    assert prediction_df['c'][9] == 10.0


def test_predict_defaulted() -> None:
    problem_def = memory_problem_def()
    executor = SimpleExecutor
    alg_catalog = FakeAlgorithmCatalogAuto
    dut = Wrangler(
        problem_definition=problem_def,
        executor=executor,
        algorithm_catalog=alg_catalog)
    _ = dut.fit_predict_rank()

    testset = dut.dataset(memory_test_df())
    test_got = dut.predict(
        new_data=testset)
    assert {
        'tabular_regression@sklearn.linear_model.linearregression',
        'tabular_regression@sklearn.ensemble.randomforestregressor:'
        'max_depth=None,min_samples_split=2',
    } == set(test_got.keys())


def test_set_current_predict() -> None:
    problem_def = memory_problem_def()
    executor = SimpleExecutor
    alg_catalog = FakeAlgorithmCatalogAuto
    dut = Wrangler(
        problem_definition=problem_def,
        executor=executor,
        algorithm_catalog=alg_catalog)
    _ = dut.fit_predict_rank()

    testset = dut.dataset(memory_test_df())

    # Pick one pipeline.
    dut.set_current('tabular_regression@sklearn.ensemble.randomforestregressor:'
                    'max_depth=None,min_samples_split=2')
    test_got = dut.predict(new_data=testset)
    assert set(test_got.keys()) == {
        'tabular_regression@sklearn.ensemble.randomforestregressor:'
        'max_depth=None,min_samples_split=2',
    }

    # Reset to all known pipelines.
    dut.set_current()

    test_got = dut.predict(new_data=testset)
    assert {
        'tabular_regression@sklearn.linear_model.linearregression',
        'tabular_regression@sklearn.ensemble.randomforestregressor:'
        'max_depth=None,min_samples_split=2',
    } == set(test_got.keys())


def test_set_current_fit() -> None:
    problem_def = memory_problem_def()
    executor = SimpleExecutor
    alg_catalog = FakeAlgorithmCatalogAuto
    dut = Wrangler(
        problem_definition=problem_def,
        executor=executor,
        algorithm_catalog=alg_catalog)
    _ = dut.fit_predict_rank()

    testset = dut.dataset(memory_train_df())

    # Pick one pipeline.
    dut.set_current('tabular_regression@sklearn.ensemble.randomforestregressor:'
                    'max_depth=None,min_samples_split=2')

    test_got = dut.fit(dataset=testset)
    assert set(test_got.keys()) == {
        'tabular_regression@sklearn.ensemble.randomforestregressor:'
        'max_depth=None,min_samples_split=2',
    }

    # Reset to all known pipelines.
    dut.set_current()

    test_got = dut.fit(dataset=testset)
    assert {
        'tabular_regression@sklearn.linear_model.linearregression',
        'tabular_regression@sklearn.ensemble.randomforestregressor:'
        'max_depth=None,min_samples_split=2',
    } == set(test_got.keys())


def test_predict_bad_executor_kind() -> None:
    problem_def = memory_problem_def()
    executor = SimpleExecutor
    dut = Wrangler(
        problem_definition=problem_def,
        executor=executor)

    fake_des = Designator('fake_des')
    stub_pipeline = ExecutablePipelineStub(trained=True)

    with pytest.raises(WranglerFailure, match=r'(fake_des.*simple)|(simple.*fake_des)/i'):
        dut.predict(
            new_data=Dataset(),
            trained_pipelines={fake_des: stub_pipeline})


def test_predict_untrained_pipeline() -> None:
    problem_def = memory_problem_def()
    executor = FakeExecutor  # executor kind is 'stub_executor_kind', should match stub pipeline.
    dut = Wrangler(
        problem_definition=problem_def,
        executor=executor)

    fake_des = Designator('fake_des')
    stub_pipeline = ExecutablePipelineStub(trained=False)

    with pytest.raises(WranglerFailure, match=r'(fake_des.*trained)|(trained.*fake_des)/i'):
        dut.predict(
            new_data=Dataset(),
            trained_pipelines={fake_des: stub_pipeline})


@pytest.fixture(scope='session')
def saver_problem_def(tmp_path_factory: pytest.TempPathFactory) -> ProblemDefinition:
    tmp_path = tmp_path_factory.mktemp('data')
    tmp_dir = tmp_path / 'sub'
    tmp_dir.mkdir()
    config = {
        "dataset": {
            "config": "memory",
            "column_roles": {
                "target": {
                    "name": "c"
                }
            }
        },
        "problem_type": {
            "task": "regression"
        },
        "cross_validation": {
            "k": 10
        },
        "metrics": {
            "root_mean_squared_error": {}
        },
        "output": {
            "path": tmp_dir,
            "instantiations": [
                "json"
            ],
            "file_type": "csv"
        },
        "hyperparams": ["disable_grid_search"]
    }
    data = pd.DataFrame(
        {
            'a': range(1, 21),
            'b': range(1, 21),
            'c': range(1, 21)
        }
    )

    return ProblemDefinition(
        problem_def=config,
        train_df=data)


def test_save_filesystem(saver_problem_def: ProblemDefinition) -> None:
    PipelineStep.reset_serial_number()
    dut = Wrangler(
        problem_definition=saver_problem_def,
        algorithm_catalog=FakeAlgorithmCatalogAuto)
    _ = dut.fit_predict_rank()

    path = saver_problem_def.output.path
    assert path is not None
    filenames = glob.glob(str(path / 'models' / '*.linearregression' / '@connect_*@.pkl'))
    assert len(filenames) == 1
    with Path(filenames[0]).open(mode='rb') as filepointer:
        cucumber = Cucumber.deserialize(filepointer.read())
    assert cucumber.hyperparams == {
        'target': ['target', 'dataframe'],
        'covariates': ['attributes', 'dataframe']
    }

    pipelines = os.listdir(str(path / 'pipelines'))
    assert {'tabular_regression@sklearn.ensemble.randomforestregressor:'
            'max_depth=none,min_samples_split=2.json',
            'tabular_regression@sklearn.linear_model.linearregression.json',
            } == set(pipelines)

    with (path / 'pipelines' / 'tabular_regression@sklearn.linear_model.linearregression.json'
          ).open() as file_pointer:
        got = json.load(file_pointer)

    assert got['pipeline_designator'] == 'tabular_regression@sklearn.linear_model.linearregression'


@pytest.fixture(scope='session')
def search_problem_def() -> ProblemDefinition:
    config = '''
    {
        "dataset": {
            "config": "memory",
            "column_roles": {
                "target": {
                    "name": "c"
                }
            }
        },
        "problem_type": {
            "task": "regression"
        },
        "cross_validation": {
            "k": 2
        },
        "metrics" : {
            "root_mean_squared_error" : {}
        },
        "hyperparams": [
            {
                "select": {
                    "algorithm": "sklearn.ensemble.RandomForestRegressor"
                },
                "params": {
                    "n_estimators": {
                        "list": [100, 200]
                    }
                }
            }
        ]
    }
    '''
    data = pd.DataFrame(
        {
            'a': range(1, 21),
            'b': range(1, 21),
            'c': range(1, 21)
        }
    )

    return ProblemDefinition(
        problem_def=config,
        train_df=data)


def test_hyperparam_search(search_problem_def: ProblemDefinition) -> None:
    dut = Wrangler(
        problem_definition=search_problem_def,
        algorithm_catalog=FakeAlgorithmCatalogAuto)
    got = dut.fit_predict_rank()
    assert len(got.executable_pipelines) == 25
    assert {
        'tabular_regression@sklearn.linear_model.linearregression',
        'tabular_regression@sklearn.ensemble.randomforestregressor:'
        'max_depth=8,min_samples_split=10,n_estimators=100',
        'tabular_regression@sklearn.ensemble.randomforestregressor:'
        'max_depth=15,min_samples_split=10,n_estimators=200',
    }.issubset(got.executable_pipelines.keys())


@pytest.fixture(scope='session')
def order_problem_def() -> ProblemDefinition:
    config = '''
    {
        "dataset": {
            "config": "memory",
            "column_roles": {
                "target": {
                    "name": "c"
                }
            }
        },
        "problem_type": {
            "task": "test_task"
        },
        "cross_validation": {
            "k": 3
        },
        "metrics" : {
            "root_mean_squared_error" : {}
        },
        "hyperparams": ["disable_grid_search"]
    }
    '''
    data = pd.DataFrame(
        {
            'a': range(1, 22),
            'b': range(1, 22),
            'c': range(2, 23)
        }
    )

    return ProblemDefinition(
        problem_def=config,
        train_df=data)


class FakeInst(FakeInstance):
    '''The instance of a fake algorithm for order tests.'''
    def predict(self, dataset: Dataset) -> Dataset:
        retval = dataset.output()
        df = pd.DataFrame({'c': dataset.dataframe['a'] + 1})
        retval.predictions = df
        return retval


class FakeAlg(Algorithm):
    '''A fake algorithm used for order tests.'''
    _name = 'fake_algorithm'

    def instantiate(self, **hyperparams) -> 'FakeInstance':
        return FakeInst(parent=self, **hyperparams)


def test_order(order_problem_def) -> None:
    dut = Wrangler(
        problem_definition=order_problem_def)

    fake_template = PipelineTemplate(
        name='test_template',
        tags={
            'task': ['test_task'],
            'data_type': ['tabular']},
        generator=dut.generator
    )
    fake_template.step(model=FakeAlg())
    dut.template_catalog.register(fake_template)

    got = dut.fit_predict_rank()
    predict_df = got.train_results.predictions[Designator('test_template')].predictions
    assert got.split_dataset.ground_truth is not None
    ground_truth_df = got.split_dataset.ground_truth.ground_truth
    pd.testing.assert_frame_equal(predict_df[['c']], ground_truth_df)
    assert all(predict_df['c'] == predict_df['ground truth'])


def non_seeded_problem_def() -> ProblemDefinition:
    config = '''
    {
        "dataset": {
            "config": "memory",
            "column_roles": {
                "target": {
                    "name": "c"
                }
            }
        },
        "problem_type": {
            "task": "test_task"
        },
        "cross_validation": {
            "k": 2
        },
        "metrics" : {
            "root_mean_squared_error" : {}
        },
        "hyperparams": ["disable_grid_search"]
    }
    '''
    data = pd.DataFrame(
        {
            'a': range(1, 21),
            'b': range(1, 21),
            'c': range(2, 22)
        }
    )

    return ProblemDefinition(
        problem_def=config,
        train_df=data)


def seeded_problem_def(seed: int) -> ProblemDefinition:
    config = {
        "dataset": {
            "config": "memory",
            "column_roles": {
                "target": {
                    "name": "c"
                }
            }
        },
        "problem_type": {
            "task": "test_task"
        },
        "cross_validation": {
            "k": 2
        },
        "metrics": {
            "root_mean_squared_error": {}
        },
        "hyperparams": [
            "disable_grid_search",
            {
                "select": {
                    "tags": {
                        "supports_random_seed": "true"
                    }
                },
                "params": {
                    "random_seed": {
                        "fixed": seed
                    }
                }
            }
        ]
    }
    data = pd.DataFrame(
        {
            'a': range(1, 21),
            'b': range(1, 21),
            'c': range(2, 22)
        }
    )

    return ProblemDefinition(
        problem_def=config,
        train_df=data)


class RandomAlgorithmInstance(AlgorithmInstance):
    _rng: RandomState

    def __init__(self, parent: Algorithm, **hyperparams):
        super().__init__(parent)
        if 'random_seed' in hyperparams:
            self._rng = RandomState(hyperparams['random_seed'])

    def predict(self, dataset: Dataset) -> Dataset:
        retval = dataset.output()
        retval['predictions'] = pd.DataFrame({
            'c': list(self._rng.randint(0, 10, len(dataset.dataframe)))
        }).reset_index(drop=True)
        return retval


class RandomAlgorithm(Algorithm):
    _name = 'random_algorithm'
    _tags = {
        'task': ['test_task'],
        'data_type': ['tabular'],
        'supports_random_seed': ['true']
    }
    _default_hyperparams = {
        'random_seed': Defaults.SEED,
    }

    def instantiate(self, **hyperparams) -> RandomAlgorithmInstance:
        return RandomAlgorithmInstance(parent=self, **self.hyperparams(**hyperparams))


def test_set_seed() -> None:
    dut_def = Wrangler(problem_definition=non_seeded_problem_def())
    dut5678 = Wrangler(problem_definition=seeded_problem_def(5678))

    pipe_def = PipelineTemplate(
        name='test_template',
        tags={
            'task': ['test_task'],
            'data_type': ['tabular']},
        generator=dut_def.generator
    )
    pipe_def.step(model=RandomAlgorithm())
    dut_def.template_catalog.register(pipe_def)

    pipe5678 = PipelineTemplate(
        name='test_template',
        tags={
            'task': ['test_task'],
            'data_type': ['tabular']},
        generator=dut5678.generator
    )
    pipe5678.step(model=RandomAlgorithm())
    dut5678.template_catalog.register(pipe5678)

    got_def = dut_def.fit_predict_rank()
    got5678 = dut5678.fit_predict_rank()

    des_def = Designator('test_template')
    des5678 = Designator('test_template@random_algorithm:random_seed=5678')

    predictions_def = got_def.train_results[des_def].prediction.predictions[['c']]
    predictions5678 = got5678.train_results[des5678].prediction.predictions[['c']]

    # The k-fold-cross-validator instantiates the algorithm separately
    # for each fold, so in this special case, we expect to see the same
    # sequence twice.

    want_def = pd.DataFrame({'c': [3, 3, 6, 2, 1, 8, 5, 1, 7, 3, 3, 3, 6, 2, 1, 8, 5, 1, 7, 3]})
    want5678 = pd.DataFrame({'c': [5, 3, 6, 9, 3, 3, 9, 8, 3, 3, 5, 3, 6, 9, 3, 3, 9, 8, 3, 3]})
    pd.testing.assert_frame_equal(predictions_def, want_def)
    pd.testing.assert_frame_equal(predictions5678, want5678)


@pytest.fixture(scope='session')
def disable_grid_search_problem_def() -> ProblemDefinition:
    config = '''
    {
        "dataset": {
            "config": "memory",
            "column_roles": {
                "target": {
                    "name": "c"
                }
            }
        },
        "problem_type": {
            "task": "regression"
        },
        "cross_validation": {
            "k": 2
        },
        "metrics" : {
            "root_mean_squared_error" : {}
        },
        "hyperparams": [
            "disable_grid_search",
            {
                "select": {
                    "algorithm": "sklearn.ensemble.RandomForestRegressor"
                },
                "params": {
                    "n_estimators": {
                        "list": [100, 200],
                        "default": 100
                    }
                }
            }
        ],
        "output": {}
    }
    '''
    data = pd.DataFrame(
        {
            'a': range(1, 21),
            'b': range(1, 21),
            'c': range(1, 21)
        }
    )

    return ProblemDefinition(
        problem_def=config,
        train_df=data)


def test_disable_grid_search(disable_grid_search_problem_def: ProblemDefinition) -> None:
    dut = Wrangler(
        problem_definition=disable_grid_search_problem_def,
        algorithm_catalog=FakeAlgorithmCatalogAuto)
    got = dut.fit_predict_rank()
    assert {
        'tabular_regression@sklearn.linear_model.linearregression',
        'tabular_regression@sklearn.ensemble.randomforestregressor'
        ':max_depth=None,min_samples_split=2,n_estimators=100'
    } == set(got.executable_pipelines.keys())
