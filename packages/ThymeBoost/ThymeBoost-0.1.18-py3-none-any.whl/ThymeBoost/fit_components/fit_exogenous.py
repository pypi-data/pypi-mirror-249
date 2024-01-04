# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import inspect
from ThymeBoost.exogenous_models import (ols_exogenous,
                                         decision_tree_exogenous,
                                         glm_exogenous)


class FitExogenous:
    def __init__(self,
                 exo_estimator='ols',
                 exogenous_lr=1,
                 **kwargs):
        self.exo_estimator = exo_estimator
        self.exogenous_lr = exogenous_lr
        self.custom_estimator = False
        self.kwargs = kwargs
        return
        
    def set_estimator(self, exo_estimator):
        if exo_estimator == 'ols':
            fit_obj = ols_exogenous.OLS
        elif exo_estimator == 'glm':
            fit_obj = glm_exogenous.GLM
        elif exo_estimator == 'decision_tree':
            fit_obj = decision_tree_exogenous.DecisionTree
        elif inspect.isclass(exo_estimator):
            fit_obj = exo_estimator
            self.custom_estimator = True
        else:
            raise NotImplementedError('That Exo estimation is not availale yet, add it to the road map!')
        return fit_obj

    def fit_exogenous_component(self, time_residual, exogenous):
        self.model_obj = self.set_estimator(self.exo_estimator)()
        if isinstance(exogenous, pd.DataFrame):
            exogenous = exogenous.to_numpy()
        if self.custom_estimator:
            exo_fitted = self.model_obj.fit(time_residual, exogenous)
        else:
            exo_fitted = self.model_obj.fit(time_residual, exogenous, **self.kwargs)
        return self.exogenous_lr*np.array(exo_fitted)
