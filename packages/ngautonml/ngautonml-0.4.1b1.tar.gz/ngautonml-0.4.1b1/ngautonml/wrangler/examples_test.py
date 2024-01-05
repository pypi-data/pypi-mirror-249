'''Tests replicating example notebooks.'''
# pylint: disable=missing-function-docstring,missing-class-docstring

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import os
from pathlib import Path

from .wrangler import Wrangler
from ..problem_def.problem_def import ProblemDefinition
from ..algorithms.impl.algorithm_auto import FakeAlgorithmCatalogAuto


def module_path() -> Path:
    current_path = str(os.getenv('PYTEST_CURRENT_TEST')).split('::', maxsplit=1)[0]
    pathobj = Path(current_path).resolve()
    module_parent = pathobj.parents[2]
    return module_parent


def credit_problem_def():
    train_path = module_path() / 'examples' / 'classification' / 'credit-train.csv'
    pdef = {
        "dataset": {
            "config": "local",
            "train_path": train_path,
            "column_roles": {
                "target": {
                    "name": "class"
                }
            }
        },
        "problem_type": {
            "task": "binary_classification"
        },
        "cross_validation": {
            "k": 2
        },
        "metrics": {
            "accuracy_score": {},
            "roc_auc_score": {}
        }
    }
    return ProblemDefinition(pdef)


def test_wrangle_credit() -> None:
    problem_def = credit_problem_def()
    dut = Wrangler(
        problem_definition=problem_def,
        algorithm_catalog=FakeAlgorithmCatalogAuto)
    got = dut.fit_predict_rank()

    assert got.split_dataset.ground_truth is not None
    assert len(got.split_dataset.ground_truth.ground_truth) == 800

    assert list(got.train_results.values())[0].prediction.predictions.shape == (800, 2)

    # For accuracy, we can't guarantee which pipe will be better, but
    #   we can check that both are present.
    # We know accuracy will be the first Ranking because they are sorted
    #   alphabetically by metric name.
    assert 'accuracy_score' in got.rankings
    pipes_included = {
        str(score.result.bound_pipeline.designator)
        for score in got.rankings['accuracy_score'].scores}
    assert len(pipes_included) == 18
    assert {
        'tabular_classification@sklearn.linear_model.logisticregression:c=100.0,class_weight=none',
        'tabular_classification@sklearn.svm.svc:c=0.01,class_weight=none'
    }.issubset(pipes_included)

    # For roc_auc, we know logistic regression is scorable and svc is unscorable
    #   (because svc cannot produce probabilities output.)
    # As a result, svc will always be ranked last and its score will be
    #   a str stating that it cannot be scored.
    assert 'roc_auc_score' in got.rankings
    best_score = got.rankings['roc_auc_score'].scores[0]
    best_pipe = str(best_score.pipeline_des)
    assert best_pipe == (
        'tabular_classification@sklearn.linear_model.logisticregression:'
        'c=1.0,class_weight=balanced')
    assert isinstance(best_score.score, float)

    worst_score = got.rankings['roc_auc_score'].scores[-1]
    assert str(worst_score.pipeline_des) == (
        'tabular_classification@sklearn.svm.svc:c=100.0,class_weight=none')
    assert isinstance(worst_score.score, str)


def iris_problem_def():
    train_path = module_path() / 'examples' / 'iris' / 'iris.csv'
    pdef = {
        "dataset": {
            "config": "local",
            "train_path": train_path,
            "column_roles": {
                "target": {
                    "name": "flowers"
                }
            }
        },
        "problem_type": {
            "task": "multiclass_classification"
        },
        "cross_validation": {
            "k": 2
        }
    }
    return ProblemDefinition(pdef)


def test_wrangle_iris() -> None:
    problem_def = iris_problem_def()
    dut = Wrangler(
        problem_definition=problem_def,
        algorithm_catalog=FakeAlgorithmCatalogAuto)
    got = dut.fit_predict_rank()

    assert got.split_dataset.ground_truth is not None
    assert len(got.split_dataset.ground_truth.ground_truth) == 150

    assert list(got.train_results.values())[0].prediction.predictions.shape == (150, 2)

    # For accuracy, we can't guarantee which pipe will be better, but
    #   we can check that both are present.
    # We know accuracy will be the first Ranking because they are sorted
    #   alphabetically by metric name.
    pipes_included = {
        str(score.result.bound_pipeline.designator)
        for score in got.rankings['accuracy_score'].scores}
    assert len(pipes_included) == 18
    assert {
        'tabular_classification@sklearn.linear_model.logisticregression:c=100.0,class_weight=none',
        'tabular_classification@sklearn.svm.svc:c=0.01,class_weight=none'
    }.issubset(pipes_included)

    # TODO(Merritt): make roc_auc_score work for multiclass


def diabetes_config():
    train_path = module_path() / 'examples' / 'regression' / 'diabetes.csv'
    pdef = {
        "dataset": {
            "config": "local",
            "train_path": train_path,
            "column_roles": {
                "target": {
                    "name": "Prog"
                }
            }
        },
        "problem_type": {
            "data_type": "TABULAR",
            "task": "REGRESSION"
        },
        "metrics": {
            "root_mean_squared_error": {}
        },
        "cross_validation": {
            "k": 2
        }
    }
    return ProblemDefinition(pdef)


def test_wrangle_diabetes() -> None:
    problem_definition = diabetes_config()
    dut = Wrangler(
        problem_definition=problem_definition,
        algorithm_catalog=FakeAlgorithmCatalogAuto
    )
    got = dut.fit_predict_rank()

    # there are 442 rows in examples/regression/diabetes.csv
    # we expect train predictions that cover all of them.
    assert list(got.train_results.values())[0].prediction.predictions.shape == (442, 2)
