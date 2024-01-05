'''An AutonML implementation of neuralforecast.models.NHITS'''
# pylint: disable=invalid-name, duplicate-code

# Copyright (c) 2023 Carnegie Mellon University
# This code is subject to the license terms contained in the LICENSE file.

import abc
from typing import Any, Dict

from pandas.api.types import is_datetime64_any_dtype as is_datetime

import neuralforecast as nf  # type: ignore[import]
from neuralforecast.common._base_windows import BaseWindows  # type: ignore[import]

from ngautonml.algorithms.impl.algorithm import Algorithm, AlgorithmCatalog, InputValueError
from ngautonml.algorithms.impl.algorithm_instance import DatasetError
from ngautonml.algorithms.impl.fittable_algorithm_instance import FittableAlgorithmInstance
from ngautonml.wrangler.constants import Defaults
from ngautonml.wrangler.dataset import Column, Dataset, DatasetKeys, RoleName


class NeuralForecastModel(Algorithm, metaclass=abc.ABCMeta):
    '''Base class for neuralforecast.models.*'''
    _name: str = 'unnamed_neuralforecast_model'
    _default_hyperparams: Dict[str, Any] = {
        'futr_exog_list': None,
        'hist_exog_list': None,
        'stat_exog_list': None,
    }


class NeuralForecastModelInstance(FittableAlgorithmInstance):
    '''Wrapper for neuralforecast.models.*'''
    _impl: nf.core.NeuralForecast
    _constructor: BaseWindows  # BaseWindows is the base class for all neuralforecast models.
    _default_hyperparams: Dict[str, Any]

    def __init__(self, parent: Algorithm, **overrides: Any):
        super().__init__(parent=parent)
        if ('true' in parent.tags.get('supports_random_seed', ['false'])
                and 'random_seed' not in overrides):
            overrides['random_seed'] = Defaults.SEED
        self._default_hyperparams = self._algorithm.hyperparams(**overrides)
        # check if default hyp has a seed and if not add it

    def _combine_and_rename(self, dataset: Dataset) -> Dataset:
        time_cols = dataset.metadata.roles.get(RoleName.TIME, [])
        assert len(time_cols) == 1, (
            f'BUG: validation should catch missing or non-unique time column: {time_cols}')
        time_col = time_cols[0]

        target_cols = dataset.metadata.roles.get(RoleName.TARGET, [])
        assert len(time_cols) == 1, (
            f'BUG: validation should catch missing or nonunique target column: {target_cols}'
        )
        target_col = target_cols[0]

        variable_cols = dataset.metadata.roles.get(RoleName.TIMESERIES_ID, [])
        assert len(variable_cols) == 1, (
            f'BUG: validation should catch missing or nonunique timeseries_id: {variable_cols}'
        )
        # TODO(Merritt): assert that this column is present in the data
        variable_col = variable_cols[0]

        roles = dataset.metadata.roles.copy()

        roles.update({
            RoleName.TIME: [Column('ds')],
            RoleName.TIMESERIES_ID: [Column('unique_id')],
            RoleName.TARGET: [Column('y')]
        })

        retval = dataset.output(
            override_metadata=dataset.metadata.override_roles(roles=roles)
        )

        # Combine covariates and target into one dataframe.
        df = dataset[DatasetKeys.COVARIATES.value]
        target = dataset[DatasetKeys.TARGET.value]
        df[target_col.name] = target
        retval.dataframe = df.rename(columns={
            str(variable_col.name): 'unique_id',
            str(time_col.name): 'ds',
            str(target_col.name): 'y',
        })

        if DatasetKeys.STATIC_EXOGENOUS in dataset:
            retval[DatasetKeys.STATIC_EXOGENOUS.value] = dataset[DatasetKeys.STATIC_EXOGENOUS.value]

        if not is_datetime(retval.dataframe['ds']):
            raise InputValueError(
                'Time column is not of datetime type: '
                f'instead found {retval.dataframe["ds"].dtype}.')

        return retval

    def hyperparams(self, **overrides: Any) -> Dict[str, Any]:
        '''Apply overrides to the default hyperparams.'''
        default_hyperparams = self._default_hyperparams.copy()
        default_hyperparams.update(**overrides)
        return default_hyperparams

    def fit(self, dataset: Dataset) -> None:
        '''Fit a model based on train data.

        Fit for neuralforecast models instantiates the model.
        '''
        self._trained = True

        # The next 4 lines are to work around a bug in
        # pytorch_lightning/utilities/parsing.py:_get_init_args.
        # TODO(piggy): Put a link to the pytorch_lightning bug here.
        parent = None
        parent = parent  # pylint: disable=self-assigning-variable
        overrides: Dict[str, Any] = {}
        overrides = overrides  # pylint: disable=self-assigning-variable

        ds = self._combine_and_rename(dataset=dataset)

        futr_exog = [
            str(col.name)
            for col in dataset.metadata.roles.get(RoleName.FUTURE_EXOGENOUS, [])]
        hist_exog = [
            str(col.name)
            for col in dataset.metadata.roles.get(RoleName.PAST_EXOGENOUS, [])]
        stat_exog = []
        stat_exog_df = None
        if DatasetKeys.STATIC_EXOGENOUS.value in dataset and (
            dataset[
                DatasetKeys.STATIC_EXOGENOUS.value] is not None):
            stat_exog = dataset[DatasetKeys.STATIC_EXOGENOUS.value].columns
            stat_exog_df = dataset[DatasetKeys.STATIC_EXOGENOUS.value]

        models = [
            self._constructor(
                **self.hyperparams(
                    h=dataset.metadata.horizon, input_size=dataset.metadata.input_size,
                    futr_exog_list=futr_exog,
                    hist_exog_list=hist_exog,
                    stat_exog_list=stat_exog))
        ]
        assert dataset.metadata.frequency is not None, (
            'BUG: Neuralforecast model was given a dataset without frequency metadata.')
        self._impl = nf.NeuralForecast(models=models, freq=dataset.metadata.frequency)
        try:
            self._impl.fit(df=ds.get_dataframe(), static_df=stat_exog_df)
        except KeyError as err:
            raise DatasetError(f'fit dataset malformed: \n{ds!r}') from err

    def predict(self, dataset: Dataset) -> Dataset:
        ds = self._combine_and_rename(dataset=dataset)
        try:
            result = self._impl.predict(df=ds.dataframe)
        except KeyError as err:
            raise DatasetError(f'predict dataset malformed {ds!r}') from err
        result.rename(columns={self._algorithm.basename: 'y'}, inplace=True)
        # this is a workaround to a neuralforecast bug:
        # unique_id is incorrectly returned as an index rather than a column
        result.reset_index(inplace=True)
        retval = ds.output()
        retval.predictions = result
        return retval


def register(catalog: AlgorithmCatalog, *args, **kwargs) -> None:  # pylint: disable=unused-argument
    '''There are no objects in this file to register.'''
