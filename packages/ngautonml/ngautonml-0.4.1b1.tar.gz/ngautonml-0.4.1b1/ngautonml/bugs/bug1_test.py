'''Test for issue #1 on gitlab (https://gitlab.com/autonlab/ngautonml/-/issues/1)'''
import pandas as pd
import pytest

from ..problem_def.problem_def import ProblemDefinition
from ..wrangler.wrangler import Wrangler

# pylint: disable=missing-function-docstring,redefined-outer-name,duplicate-code


@pytest.fixture(scope='session')
def bug1_problem_def() -> ProblemDefinition:
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
            "data_type": "tabular",
            "task": "binary_classification"
        },
        "metrics" : {
            "roc_auc_score": {},
            "accuracy_score": {}
        },
        "hyperparams": [
            "disable_grid_search"
        ]
    }
    '''
    train_data = pd.DataFrame(
        {
            'a': range(1, 101),
            'b': range(101, 201),
            'c': [0, 1] * 50
        }
    )
    test_data = pd.DataFrame(
        {
            'a': range(101, 151),
            'b': range(201, 251),
            'c': [0, 1] * 25
        }
    )

    return ProblemDefinition(
        problem_def=config,
        train_df=train_data,
        test_df=test_data)


def test_bug1(bug1_problem_def: ProblemDefinition) -> None:
    dut = Wrangler(
        problem_definition=bug1_problem_def)

    got = dut.fit_predict_rank()
    assert got.test_results is not None
    pred1 = got.test_results.predictions

    new_data = dut.load_test_dataset()
    assert new_data is not None
    got2 = dut.predict(new_data=new_data)
    pred2 = got2.predictions

    for des in pred1.keys():
        df1 = pred1[des].predictions
        df2 = pred2[des].predictions
        print(des)
        print(pd.concat([df1, df2], axis=1))
        pd.testing.assert_frame_equal(df1, df2)
