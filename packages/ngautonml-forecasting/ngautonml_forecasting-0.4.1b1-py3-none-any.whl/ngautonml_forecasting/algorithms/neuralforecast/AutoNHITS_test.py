'''Tests for AutoNHITS.py'''
# pylint: disable=invalid-name, missing-function-docstring, duplicate-code
import warnings

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

from neuralforecast.utils import AirPassengersDF  # type: ignore[import]

import pandas as pd
from pytorch_lightning.utilities.warnings import PossibleUserWarning
import pytest
import torch

from ngautonml.algorithms.impl.algorithm_instance import DatasetError
from ngautonml.wrangler.dataset import Column, Dataset, DatasetKeys, Metadata, RoleName
from .AutoNHITS import AutoNHITSModel


def test_sunny_day() -> None:
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=PossibleUserWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    if not torch.cuda.is_available():
        print('test disabled due to lack of GPU.')
        return

    model = AutoNHITSModel(num_samples=2)
    dut = model.instantiate()

    AirPassengersCovariates = AirPassengersDF[['unique_id', 'ds']]
    AirPassengersTarget = AirPassengersDF[['y']]

    metadata = Metadata(
        roles={
            RoleName.TIMESERIES_ID: [Column('unique_id')],
            RoleName.TIME: [Column('ds')],
            RoleName.TARGET: [Column('y')]
        },
        forecasting={'horizon': 12, 'input_size': 24, 'frequency': 'M'})
    dataset = Dataset(metadata=metadata, **{
        DatasetKeys.COVARIATES.value: AirPassengersCovariates,
        DatasetKeys.TARGET.value: AirPassengersTarget,
    })
    dut.fit(dataset)

    got = dut.predict(dataset)

    first = got.predictions.head(n=1)
    assert first['ds'][0] == pd.Timestamp('1961-01-31 00:00:00')
    assert first['y'][0] == pytest.approx(451.5, 0.001)


def test_missing_input_size() -> None:
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=PossibleUserWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    model = AutoNHITSModel(num_samples=2)
    dut = model.instantiate()

    AirPassengersCovariates = AirPassengersDF[['unique_id', 'ds']]
    AirPassengersTarget = AirPassengersDF[['y']]

    metadata = Metadata(
        roles={
            RoleName.TIMESERIES_ID: [Column('unique_id')],
            RoleName.TIME: [Column('ds')],
            RoleName.TARGET: [Column('y')]
        },
        forecasting={'horizon': 12, 'frequency': 'M'})  # Missing input size
    dataset = Dataset(metadata=metadata, **{
        DatasetKeys.COVARIATES.value: AirPassengersCovariates,
        DatasetKeys.TARGET.value: AirPassengersTarget,
    })

    with pytest.raises(DatasetError, match='input_size'):
        dut.fit(dataset)
