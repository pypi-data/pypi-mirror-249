# -*- coding: utf-8 -*-
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn import linear_model
from ThymeBoost.seasonality_models.seasonality_base_class import SeasonalityBaseModel


class DynamicFourierSeasonalityModel(SeasonalityBaseModel):
    """
    Seasonality for naive decomposition method.
    """
    model = 'dynamic_fourier'

    def __init__(self,
                 seasonal_period,
                 normalize_seasonality,
                 seasonality_weights):
        self.seasonal_period = seasonal_period
        self.normalize_seasonality = normalize_seasonality
        self.seasonality_weights = seasonality_weights
        self.seasonality = None
        self.model_params = None
        return

    def __str__(self):
        return f'{self.model}({self.kwargs["fourier_order"]}, {self.seasonality_weights is not None})'

    def handle_seasonal_weights(self, y):
        if self.seasonality_weights is None:
            seasonality_weights = None
        elif isinstance(self.seasonality_weights, list):
            if self.seasonal_weights[0] is None:
                seasonality_weights = None
        elif self.seasonality_weights == 'regularize':
            seasonality_weights = 1/(0.0001 + y**2)
        elif self.seasonality_weights == 'explode':
            seasonality_weights = (y**2)
        elif callable(self.seasonality_weights):
            seasonality_weights = self.seasonality_weights(y)
        else:
            seasonality_weights = np.array(self.seasonality_weights).reshape(-1,)
            seasonality_weights = seasonality_weights[:len(y)]
        return seasonality_weights

    def get_fourier_series(self, t, fourier_order):
        x = 2 * np.pi * (np.arange(1, fourier_order + 1) /
                         self.seasonal_period)
        x = x * t[:, None]
        fourier_series = np.concatenate((np.cos(x), np.sin(x)), axis=1)
        # n = len(t)
        # fourier_left = fourier_series[:int(n / 2)]
        # fourier_right = fourier_series[-int(math.ceil(n / 2)):]
        # fourier_left = np.multiply(fourier_left.T, np.linspace(0, 1, num=int(n / 2))).T
        # fourier_right = np.multiply(fourier_right.T, np.linspace(1, 0, num=math.ceil(n / 2))).T
        # exo_stoch = np.append(fourier_left, fourier_right, axis=0)
        # exo = np.multiply(fourier_series.T, np.linspace(0, 1, num=n)).T
        # exo = np.append(exo, np.flip(exo), axis=1)
        # exo = np.append(exo, exo_stoch, axis=1)
        # exo = np.append(fourier_series, exo_stoch, axis=1)
        return fourier_series

    def fit(self, y, **kwargs):
        """
        Fit the seasonal component for fourier basis function method in the boosting loop.

        Parameters
        ----------
        y : TYPE
            DESCRIPTION.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.kwargs = kwargs
        fourier_order = kwargs['fourier_order']
        alpha = kwargs['fourier_alpha']
        if alpha is None:
            alpha = 1
        seasonality_weights = self.handle_seasonal_weights(y)
        n = len(y)
        ####
        period = self.seasonal_period
        full_stochastic = []
        stoch_len = len(y)
        stoch = self.get_fourier_series(np.arange(period),
                                 fourier_order)
        stochastic = None
        n_seas = int((n / period) * -1 // 1 * -1)
        for i in range(n_seas):
            zero_stoch = np.zeros((len(y), fourier_order * 2))
            if stoch_len - int(period) >= 0:
                zero_stoch[i * int(period): (i + 1) * int(period), :] = stoch
            else:
                zero_stoch[-stoch_len:, :] = stoch[:stoch_len]
            if stochastic is None:
                stochastic = zero_stoch
            else:
                stochastic = np.concatenate((stochastic, zero_stoch), axis=1)
            stoch_len -= int(period)
        full_stochastic.append(stochastic)
        X = np.hstack(full_stochastic)
        # X = np.append(X, np.resize(stoch, (len(y), -1)), axis=1)
        ####
        # X = self.get_fourier_series(np.arange(len(y)), fourier_order)
        # plt.plot(X)
        # plt.show()
        clf = linear_model.Lasso(alpha=alpha)
        clf.fit(X, y)
        self.seasonality = clf.predict(X)
#       If normalize_seasonality we call normalize function from base class
        if self.normalize_seasonality:
            self.seasonality = self.normalize()
        self.seasonality = self.seasonality * kwargs['seasonality_lr']
        single_season = self.seasonality[-self.seasonal_period:]
        future_seasonality = np.resize(single_season, len(y) + self.seasonal_period)
        self.model_params = future_seasonality[-self.seasonal_period:]
        return self.seasonality

    def predict(self, forecast_horizon, model_params):
        return np.resize(model_params, forecast_horizon)



                # self.full_stochastic = full_stochastic
                # self.stochastic_size = np.shape(full_stochastic)[1]
                # X = np.concatenate((X, full_stochastic), axis=1)


