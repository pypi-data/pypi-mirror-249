'''Tests for the Ranker class implementations'''
import re
from typing import Optional

import pandas as pd
import pytest

from ..executor.executor import ExecutorKind
from ..generator.bound_pipeline import BoundPipelineStub
from ..generator.designator import Designator
from ..instantiator.executable_pipeline import (ExecutablePipelineStub,
                                                PipelineResult,
                                                PipelineResults)
from ..metrics.impl.metric import MetricInvalidDatasetError
from ..metrics.impl.metric_catalog import Metric
from ..wrangler.dataset import Dataset
from .ranker import RankerError, ScoredResult
from .ranker_impl import RankerImpl

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.


# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=redefined-outer-name


class FakeMetricLow(Metric):
    '''Fake metric where lower is better'''
    _name = 'fake_metric_low'
    _high = False

    def calculate(self,
                  pred: Dataset,
                  ground_truth: Optional[Dataset] = None) -> float:
        if 'column' not in pred:
            raise MetricInvalidDatasetError('hamster')
        return pred['column'][0]


class FakeMetricHigh(Metric):
    '''Fake metric where higher is better'''
    _name = 'fake_metric_high'
    _high = True

    def calculate(self,
                  pred: Dataset,
                  ground_truth: Optional[Dataset] = None) -> float:
        if 'column' not in pred:
            raise MetricInvalidDatasetError('hamster')
        return pred['column'][0]


class FakeMetricAdd(Metric):
    '''Fake metric which adds .5 to whatever FakeMetricHigh returns'''
    _name = 'fake_metric_add'
    _high = True

    def calculate(self,
                  pred: Dataset,
                  ground_truth: Optional[Dataset] = None) -> float:
        return FakeMetricHigh().calculate(pred, ground_truth) + 0.5


PIPELINE1 = ExecutablePipelineStub(
    kind=ExecutorKind('stub_executor_kind'),
    pipeline=BoundPipelineStub(name='pipeline1'))


PIPELINE2 = ExecutablePipelineStub(
    kind=ExecutorKind('stub_executor_kind'),
    pipeline=BoundPipelineStub(name='pipeline2'))


UNRANKABLE_PIPE = ExecutablePipelineStub(
    kind=ExecutorKind('stub_executor_kind'),
    pipeline=BoundPipelineStub(name='unrankable_pipe'))


ERROR_PIPE = ExecutablePipelineStub(
    kind=ExecutorKind('stub_executor_kind'),
    pipeline=BoundPipelineStub(name='error_pipe')
)


@pytest.fixture(scope='session')
def result1() -> PipelineResult:
    prediction1 = Dataset(column=[1.0])
    return PipelineResult(executable_pipeline=PIPELINE1,
                          prediction=prediction1)


@pytest.fixture(scope='session')
def results(result1: PipelineResult) -> PipelineResults:
    result2 = PipelineResult(executable_pipeline=PIPELINE2,
                             prediction=Dataset(column=[2.0]))
    unrankable_res = PipelineResult(executable_pipeline=UNRANKABLE_PIPE,
                                    prediction=Dataset())
    error_res = PipelineResult(executable_pipeline=ERROR_PIPE,
                               prediction=Dataset(
                                   {'error': 'gerbil'}))
    des1 = Designator('result1')
    des2 = Designator('result2')
    unrankable_des = Designator('unrankable_res')
    error_des = Designator('error')
    return PipelineResults({
        des1: result1,
        des2: result2,
        unrankable_des: unrankable_res,
        error_des: error_res})


def test_scored_result_lt_different_metrics(result1: PipelineResult) -> None:
    met1 = FakeMetricLow()
    met2 = FakeMetricHigh()
    res1 = ScoredResult(metric=met1,
                        result=result1)
    res2 = ScoredResult(metric=met2,
                        result=result1)
    with pytest.raises(RankerError,
                       match=r'(c_low.*c_high)|(c_high.*c_low)'):
        _ = res1 < res2


def test_unscorable_reason(result1: PipelineResult) -> None:
    res = ScoredResult(metric=FakeMetricHigh(),
                       result=result1,
                       unscorable_reason='foo')
    assert 'foo' in str(res)


def test_ranker_low(results: PipelineResults) -> None:
    dut = RankerImpl()
    got = dut.rank(results=results, metrics={'fake_metric_low': FakeMetricLow()})

    # low: expect [res1, res2, gerbil, hamster]
    assert re.search(
        pattern='pipeline1.*pipeline2.*error_pipe.*unrankable_pipe',
        string=str(got['fake_metric_low']),
        flags=re.MULTILINE | re.DOTALL)


def test_ranker_high(results: PipelineResults) -> None:
    dut = RankerImpl()
    got = dut.rank(results=results, metrics={'fake_metric_high': FakeMetricHigh()})

    # high: expect [res2, res1, gerbil, hamster]
    assert re.search(
        pattern='pipeline2.*pipeline1.*error_pipe.*unrankable_pipe',
        string=str(got),
        flags=re.MULTILINE | re.DOTALL)


def test_ranking_df(results: PipelineResults) -> None:
    dut = RankerImpl()
    got = dut.rank(results=results, metrics={'fake_metric_high': FakeMetricHigh()})
    want = pd.DataFrame({
        'pipeline': ['pipeline2', 'pipeline1', 'error_pipe', 'unrankable_pipe'],
        'fake_metric_high': [2.0, 1.0, 'gerbil', 'hamster']
    })
    pd.testing.assert_frame_equal(want, got['fake_metric_high'].as_dataframe())


def test_rankings_df(results: PipelineResults) -> None:
    dut = RankerImpl()
    got = dut.rank(results=results, metrics={
        'fake_metric_high': FakeMetricHigh(),
        'fake_metric_low': FakeMetricLow(),
        'fake_metric_add': FakeMetricAdd()
    })
    want = pd.DataFrame({
        'pipeline': ['pipeline2', 'pipeline1', 'error_pipe', 'unrankable_pipe'],
        'fake_metric_add': [2.5, 1.5, 'gerbil', 'hamster'],
        'fake_metric_high': [2.0, 1.0, 'gerbil', 'hamster'],
        'fake_metric_low': [2.0, 1.0, 'gerbil', 'hamster']
    })
    pd.testing.assert_frame_equal(want, got.as_dataframe())


def test_rankings_df_order(results: PipelineResults) -> None:
    dut = RankerImpl()
    got = dut.rank(results=results, metrics={
        'fake_metric_high': FakeMetricHigh(),
        'fake_metric_low': FakeMetricLow(),
        'fake_metric_add': FakeMetricAdd()
    })
    want = pd.DataFrame({
        'pipeline': ['pipeline1', 'pipeline2', 'error_pipe', 'unrankable_pipe'],
        'fake_metric_low': [1.0, 2.0, 'gerbil', 'hamster'],
        'fake_metric_add': [1.5, 2.5, 'gerbil', 'hamster'],
        'fake_metric_high': [1.0, 2.0, 'gerbil', 'hamster']
    })
    got_df = got.as_dataframe(order_metric='fake_metric_low')
    print(got_df)
    pd.testing.assert_frame_equal(want, got_df)
