'''Tests for problem_def.py'''
from pathlib import Path

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import pandas as pd
import pytest

from ..dataset_formats.local import LocalDatasetConfig
from ..dataset_formats.memory import MemoryDatasetConfig
from ..wrangler.dataset import RoleName, Column
from .config_component import ParsingErrors
from .output_config import OutputConfigError
from .problem_def import ProblemDefinition, Task, ValidationErrors


# pylint: disable=missing-function-docstring,protected-access
# pylint: disable=redefined-outer-name


@pytest.fixture(scope="session")
def tmp_path(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp("data")


def module_path() -> Path:
    pathobj = Path(__file__).resolve()
    module_parent = pathobj.parents[2]
    return module_parent


TEST_PROBLEM_DEF = '''{
    "_comments" : [
        "A json file fully encapsulating the problem definition",
        "Specifically, an exmaple time series forecasting problem."
    ],
    "dataset": {
        "config": "ignore",
        "column_roles": {}
    },
    "problem_type": {
        "task": "regression"
    },
    "output": {}
}
'''


def test_get():
    dut = ProblemDefinition(TEST_PROBLEM_DEF)
    assert dut._get('problem_type', 'task') == 'regression'
    assert set(dut._get().keys()) == set(
        ['output', 'dataset', 'problem_type'])


def test_read_from_file(tmp_path: Path) -> None:
    tmp_file = tmp_path / 'pdef.json'
    with open(str(tmp_file), 'w', encoding='utf8') as f:
        f.write(TEST_PROBLEM_DEF)
    dut = ProblemDefinition(str(tmp_file))
    assert dut._get('problem_type', 'task') == 'regression'
    assert set(dut._get().keys()) == set(
        ['output', 'dataset', 'problem_type'])


def test_read_from_file_fail() -> None:
    '''We want to throw multiple errors for an invalid string.

    If a string is given that cannot be parsed as JSON or a filepath,
    we want to show the errors from both attempts to parse it.
    '''
    match_str = r'(JSONDecode.*FileNotFound)|(FileNotFound.*JSONDecode)'
    with pytest.raises(ParsingErrors,
                       match=match_str):
        ProblemDefinition('foo.foo')


def test_dataset_config() -> None:
    path = module_path() / 'examples' / 'classification' / 'credit.csv'
    pdef = {
        "dataset": {
            "config": "local",
            "train_path": path,
            "column_roles": {}
        },
        "problem_type": {
            "task": "regression"
        },
        "output": {}
    }
    dut = ProblemDefinition(pdef)
    assert isinstance(dut.dataset_config, LocalDatasetConfig)


MISSING_KEY = '''{
    "metrics" : {}
}
'''

# Missing "output" key


def test_missing_keys() -> None:
    with pytest.raises(ValidationErrors, match=r"[Mm]issing"):
        ProblemDefinition(MISSING_KEY)


INVALID_KEY = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {}
    },
    "problem_type": {
        "task": "regression"
    },
    "hamster": {}
}
'''


def test_invalid_keys() -> None:
    with pytest.raises(ValidationErrors, match=r"hamster"):
        ProblemDefinition(INVALID_KEY)


METRIC_MULTI = '''{
    "metrics" : {
        "metric1" : {
            "catalog_name": "real_metric_name",
            "k1" : "v1"
        },
        "metric2" : {
            "catalog_name": "real_metric_name",
            "k1" : "v2"
        },
        "another_metric": {}
    },
    "dataset": {
        "config": "ignore",
        "column_roles": {}
    },
    "problem_type": {
        "task": "regression"
    }
}
'''


def test_metric_sunny_day() -> None:
    dut = ProblemDefinition(METRIC_MULTI).metric_configs
    assert len(dut) == 3
    dutm1 = dut['metric1']
    assert dutm1.name == 'metric1'
    assert dutm1.hyperparams == {'k1': 'v1'}
    assert dutm1.catalog_name == 'real_metric_name'
    dutm2 = dut['metric2']
    assert dutm2.name == 'metric2'
    assert dutm2.hyperparams == {'k1': 'v2'}
    assert dutm2.catalog_name == 'real_metric_name'
    dutanother = dut['another_metric']
    assert dutanother.name == 'another_metric'
    assert dutanother.hyperparams == {}
    assert dutanother.catalog_name == 'another_metric'


def test_no_metrics() -> None:
    dut = ProblemDefinition(TEST_PROBLEM_DEF)
    assert dut.metric_configs == {}


OPTIONAL_FIELDS = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {}
    },
    "problem_type": {
        "task": "regression"
    },
    "template_disable_list": {},
    "template_enable_list": {},
    "model_disable_list": {},
    "model_enable_list": {},
    "instantiations": [],
    "hyperparam_search_space": {}
}
'''


def test_optional_fields() -> None:
    dut = ProblemDefinition(OPTIONAL_FIELDS)
    assert set(dut._get().keys()).issuperset(set(
        ["template_disable_list", "template_enable_list",
         "model_disable_list", "model_enable_list",
         "instantiations", "hyperparam_search_space"]))


SUNNY_TASK = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {}
    },
    "problem_type": {
        "data_type": "text",
        "task": "regression"
    }
}'''


def test_task_sunny_day() -> None:
    dut = ProblemDefinition(SUNNY_TASK)
    prob_type = dut.task
    print(f'Problem type: {prob_type}')
    assert prob_type == Task(clause={'data_type': 'text', 'task': 'regression'})


TASK_WITH_NO_TASK_TYPE = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {}
    },
    "problem_type": {
        "data_type": "TABULAR"
    }
}'''


def test_problem_type_missing_task() -> None:
    with pytest.raises(ValidationErrors, match=r'[Tt]ask'):
        ProblemDefinition(TASK_WITH_NO_TASK_TYPE)


TASK_WITH_NO_DATA_TYPE = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {}
    },
    "problem_type": {
        "task": "REGRESSION"
    }
}'''


def test_problem_type_missing_data_type() -> None:
    dut = ProblemDefinition(TASK_WITH_NO_DATA_TYPE)
    want = Task(clause={'data_type': "tabular", 'task': "regression"})
    got = dut.task
    assert want == got


NON_DICT_PROBLEM_TYPE = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {}
    },
    "problem_type": []
}'''


def test_problem_type_not_dict() -> None:
    with pytest.raises(ValidationErrors, match=r'dict((.|\n)*)problem_type.task'):
        ProblemDefinition(NON_DICT_PROBLEM_TYPE)


_DEFAULT_INSTANTIATIONS = sorted(['simple', 'stub_executor_kind'])


def test_instantiations_missing() -> None:
    dut = ProblemDefinition(TEST_PROBLEM_DEF)
    instantiations = dut.instantiations
    assert sorted(instantiations) == _DEFAULT_INSTANTIATIONS


EMPTY_INSTANTIATIONS = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {}
    },
    "problem_type": {
        "task": "regression"
    },
    "output": {
        "instantiations": []
    }
}'''


def test_instantiations_disable() -> None:
    dut = ProblemDefinition(EMPTY_INSTANTIATIONS)
    instantiations = dut.instantiations
    assert instantiations == []


SIMPLE_INSTANTIATIONS = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {}
    },
    "problem_type": {
        "task": "regression"
    },
    "output": {
        "instantiations": [
            "SIMPLE",
            "stub_executor_kind"
        ]
    }
}'''


def test_instantiations_sunny_day() -> None:
    dut = ProblemDefinition(SIMPLE_INSTANTIATIONS)
    instantiations = dut.instantiations
    assert set(instantiations) == set({'simple', 'stub_executor_kind'})


COMMENTS_PRESENT = '''{
    "metrics" : {},
    "dataset": {
        "config": "ignore",
        "column_roles": {}
    },
    "problem_type": {
        "_comments": ["Some comment."],
        "data_type": "TEXT",
        "task": "REGRESSION"
    }
}'''


def test_comments() -> None:
    dut = ProblemDefinition(COMMENTS_PRESENT)
    got = dut._get('problem_type')
    want = {
        'data_type': 'TEXT',
        'task': 'REGRESSION'
    }
    assert got == want


BINARY_CLASSIFICATION_NO_POS_LABEL = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {
            "target": "class"
        }
    },
    "problem_type": {
        "task": "binary_classification"
    },
    "metrics" : [
        {
          "MEAN_ABSOLUTE_ERROR": {}
        }
    ]
}
'''


@pytest.mark.xfail
def test_binary_classification_no_pos_label() -> None:
    with pytest.raises(ValidationErrors, match='binary_classification.*pos_label'):
        ProblemDefinition(BINARY_CLASSIFICATION_NO_POS_LABEL)


BINARY_CLASSIFICATION_WITH_POS_LABEL = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {
            "target": {
                "name": "class",
                "pos_label": "good"
            }
        }
    },
    "problem_type": {
        "task": "binary_classification"
    }
}
'''


def test_metadata_binary_classification_with_pos_label() -> None:
    dut = ProblemDefinition(BINARY_CLASSIFICATION_WITH_POS_LABEL)
    data = dut.dataset_config.load_train()
    assert data.roles[RoleName.TARGET] == [Column('class')]
    assert data.metadata.pos_labels[RoleName.TARGET] == 'good'


OUTPUT_DIR = '''{{
    "dataset": {{
        "config": "ignore",
        "column_roles": {{}}
    }},
    "problem_type": {{
        "task": "regression"
    }},
    "output": {{
        "path": "{output_path}"
    }}
}}
'''


def test_output_dir_exists(tmp_path: Path) -> None:
    tmp_dir = tmp_path / "sub"
    tmp_dir.mkdir()
    pdef_json = OUTPUT_DIR.format(output_path=str(tmp_dir))
    dut = ProblemDefinition(pdef_json)
    assert dut.output.path == tmp_dir


def test_output_dir_not_exist(tmp_path: Path) -> None:
    newsubdir = tmp_path / "newsubdir"
    pdef_json = OUTPUT_DIR.format(output_path=str(newsubdir))
    dut = ProblemDefinition(pdef_json)
    assert dut.output.path == newsubdir
    assert newsubdir.exists()


def test_output_dir_not_a_dir(tmp_path: Path) -> None:
    notadir = tmp_path / "notadir.txt"
    notadir.write_text('This is a text file, not a directory.\n')
    pdef_json = OUTPUT_DIR.format(output_path=str(notadir))
    with pytest.raises(OutputConfigError):
        _ = ProblemDefinition(pdef_json)


def test_output_dir_parent_not_exist(tmp_path: Path) -> None:
    nonexistent_parent = tmp_path / 'nonexistent' / 'also_nonexistent'
    pdef_json = OUTPUT_DIR.format(output_path=str(nonexistent_parent))
    with pytest.raises(OutputConfigError):
        _ = ProblemDefinition(pdef_json)


FORECASTING_NO_TIME = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {
            "target": {
                "name": "class"
            }
        },
        "forecasting": {
            "horizon": 5,
            "input_size": 15
        }
    },
    "problem_type": {
        "task": "forecasting"
    }
}
'''


def test_forecasting_no_time() -> None:
    with pytest.raises(ValidationErrors,
                       match='(forecasting.*time)|(time.*forecasting)'):
        ProblemDefinition(FORECASTING_NO_TIME)


FORECASTING_NO_HORIZON = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {
            "target": {
                "name": "class"
            },
            "time": {
                "name": "FOO"
            }
        },
        "forecasting": {
            "input_size": 15
        }
    },
    "problem_type": {
        "task": "forecasting"
    }
}
'''


def test_forecasting_no_horizon() -> None:
    with pytest.raises(ValidationErrors,
                       match='(forecasting.*horizon)|(horizon.*forecasting)'):
        ProblemDefinition(FORECASTING_NO_HORIZON)


FORECASTING_INVALID_FREQUENCY = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {
            "target": {
                "name": "class"
            },
            "time": {
                "name": "FOO"
            }
        },
        "forecasting": {
            "horizon": 5,
            "input_size": 15,
            "frequency": "INVALID_FREQ_FOR_TEST"
        }
    },
    "problem_type": {
        "task": "forecasting"
    }
}
'''


def test_forecasting_invalid_frequency() -> None:
    with pytest.raises(ValidationErrors,
                       match='(forecasting.*frequency)|(frequency.*forecasting)'):
        ProblemDefinition(FORECASTING_INVALID_FREQUENCY)


FORECASTING_WITH_FREQUENCY = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {
            "target": {
                "name": "class"
            },
            "time": {
                "name": "FOO"
            }
        },
        "forecasting": {
            "horizon": 5,
            "input_size": 15,
            "frequency": "D"
        }
    },
    "problem_type": {
        "task": "forecasting"
    }
}
'''


def test_forecasting_with_frequency() -> None:
    dut = ProblemDefinition(FORECASTING_WITH_FREQUENCY)
    got = dut._get('dataset', 'forecasting', 'frequency')
    want = 'D'

    assert got == want


FORECASTING_WITH_DEFAULT_FREQUENCY = '''{
    "dataset": {
        "config": "ignore",
        "column_roles": {
            "target": {
                "name": "class"
            },
            "time": {
                "name": "FOO"
            }
        },
        "forecasting": {
            "horizon": 5,
            "input_size": 15
        }
    },
    "problem_type": {
        "task": "forecasting"
    }
}
'''


def test_forecasting_with_default_frequency() -> None:
    dut = ProblemDefinition(FORECASTING_WITH_DEFAULT_FREQUENCY)
    assert dut.dataset_config.forecasting is not None
    got = dut.dataset_config.forecasting['frequency']
    want = 'M'

    assert got == want


MEMORY_PROBLEM_DEF = '''{
    "dataset": {
        "config": "memory",
        "column_roles": {
            "target": {
                "name": "c"
            }
        }
    },
    "problem_type": {
        "task": "binary_classification"
    }
}
'''


def test_memory_problem_def() -> None:
    dataframe = pd.DataFrame(
        {
            'a': range(1, 15001),
            'b': range(1, 15001),
            'c': range(1, 15001)
        }
    )
    dut = ProblemDefinition(MEMORY_PROBLEM_DEF, train_df=dataframe, test_df=dataframe)
    dataset = dut.dataset_config.load_test()

    assert isinstance(dut.dataset_config, MemoryDatasetConfig)
    pd.testing.assert_frame_equal(dataframe, dut.dataset_config.load_train().dataframe)

    assert dataset is not None
    # drop the target column in the original dataframe because we expect
    #   `load_test()` to drop the target column
    pd.testing.assert_frame_equal(dataframe.drop('c', axis=1), dataset.dataframe)


def test_missing_dataframe_memory_problem_def() -> None:
    # expect error message in the exception has one of the following two patterns:
    #   "memory ... dataframe"
    #   "dataframe ... memory"
    with pytest.raises(ValidationErrors, match=r'(memory.*dataframe)|(dataframe.*memory)/i'):
        ProblemDefinition(MEMORY_PROBLEM_DEF)


MEMORY_PROBLEM_DEF_WITH_K = '''{
    "dataset": {
        "config": "memory",
        "column_roles": {
            "target": {
                "name": "c"
            }
        }
    },
    "problem_type": {
        "task": "binary_classification"
    },
    "cross_validation": {
        "k": 10
    }
}
'''


def test_memory_problem_def_with_k() -> None:
    dataframe = pd.DataFrame(
        {
            'a': range(1, 15001),
            'b': range(1, 15001),
            'c': range(1, 15001)
        }
    )
    dut = ProblemDefinition(MEMORY_PROBLEM_DEF_WITH_K, train_df=dataframe, test_df=dataframe)

    assert dut.cross_validation_config.k == 10


# TODO(piggy): This test relies on validation that was removed to make image processing work.
# The fix is to add a new catalog for problem defs.
@pytest.mark.xfail
def test_memory_problem_def_with_invalid_k() -> None:
    dataframe = pd.DataFrame(
        {
            'a': range(1, 3),
            'b': range(1, 3),
            'c': range(1, 3)
        }
    )

    with pytest.raises(ValidationErrors, match=r'(k.*row)|(row.*k)/i'):
        ProblemDefinition(MEMORY_PROBLEM_DEF_WITH_K, train_df=dataframe, test_df=dataframe)
