'''Tests for sampled_splitter.py'''

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
import pytest

from ngautonml.dataset_formats.impl.dataset_format_catalog import DatasetFormatCatalogAuto
from ngautonml.problem_def.cross_validation_config import CrossValidationConfig
from ngautonml.wrangler.dataset import Dataset, DatasetKeys
from .forecasting_splitter import ForecastingSplitter

# pylint: disable=missing-function-docstring, duplicate-code

TEST_DATASET_CONFIG = {
    "config": "ignore",
    "forecasting": {
        "horizon": 30,
        "input_size": 90
    },
    "column_roles": {
        "target": {
            "name": "c",
        },
        "time": {
            "name": "a",
        },
    },
}


def test_split_sunny_day() -> None:
    dataset_config = DatasetFormatCatalogAuto().build(TEST_DATASET_CONFIG)
    metadata = dataset_config.metadata
    dataframe = pd.DataFrame({
        'a': range(1, 1001),
        'b': range(1001, 2001),
        'c': range(2001, 3001)})
    data = Dataset(metadata=metadata, **{
        'dataframe': dataframe,
        'static_exogenous': None})

    dut = ForecastingSplitter(cv_config=CrossValidationConfig({}))

    got = dut.split(dataset=data, dataset_config=dataset_config)
    assert len(got.folds) == 1

    assert got.folds[0].train.dataframe.shape == (970, 3)
    assert got.folds[0].validate.dataframe.shape == (90, 3)
    assert got.ground_truth is not None
    assert got.ground_truth.ground_truth.shape == (30, 3)

    # Confirm that order is preserved.
    assert got.folds[0].train[DatasetKeys.DATAFRAME.value].index[599] == 599


TEST_DATASET_CONFIG_NO_TIME = {
    "config": "ignore",
    "forecasting": {
        "horizon": 30,
        "input_size": 90
    },
    "column_roles": {
        "target": {
            "name": "class",
        },
    },
}


def test_split_no_time() -> None:
    dataset_config = DatasetFormatCatalogAuto().build(TEST_DATASET_CONFIG_NO_TIME)
    metadata = dataset_config.metadata
    dataframe = pd.DataFrame({
        'a': range(1, 1001),
        'b': range(1001, 2001),
        'c': range(2001, 3001)})
    data = Dataset(metadata=metadata, **{DatasetKeys.DATAFRAME.value: dataframe})

    dut = ForecastingSplitter(cv_config=CrossValidationConfig({}))

    with pytest.raises(AssertionError, match='TIME'):
        dut.split(dataset=data, dataset_config=dataset_config)


def test_datetime_parse() -> None:
    dataset_config = DatasetFormatCatalogAuto().build(TEST_DATASET_CONFIG)
    metadata = dataset_config.metadata
    dataframe = pd.DataFrame({
        'a': ['2013-12-22', '2013-12-23', '2013-12-24'],
        'b': range(1000, 1003),
        'c': range(2000, 2003)})
    data = Dataset(metadata=metadata, **{
        'dataframe': dataframe,
        'static_exogenous': None})

    dut = ForecastingSplitter(cv_config=CrossValidationConfig({}))

    got = dut.split(dataset=data, dataset_config=dataset_config)
    assert len(got.folds) == 1
    assert is_datetime(got.folds[0].train.get_dataframe()['a'])
    assert is_datetime(got.folds[0].validate.get_dataframe()['a'])
    assert got.ground_truth is not None
    assert is_datetime(got.ground_truth.ground_truth['a'])
