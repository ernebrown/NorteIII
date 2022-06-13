from typing import List, Union

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator as baseEstimator
from sklearn.ensemble.base import BaseEstimator as ensembleEstimator

from cctwin.helper import parsers


class ModelExecutor:
    def __init__(self, model_dict: dict):
        self.model_dict = model_dict

    @property
    def model_dict(self):
        return self.__model_dict

    @model_dict.setter
    def model_dict(self, value: dict):
        for model_key, model in value.items():
            if not parsers.is_valid_model_key(model_key):
                raise ValueError(f'Model info string {model_key} does not match expected format.'
                                 f'It should be formatted as desc<outputs><inputs>. '
                                 f'Each output and input should be separated by a pipe "|"')
            if not isinstance(model, (baseEstimator, ensembleEstimator)):
                raise TypeError('Given model is not an estimator from sklearn.base or sklearn.ensemble.base modules')
        self.__model_dict = value

    def append_predictions(self, model_key: str, df: pd.DataFrame, custom_output_names: Union[None, List[str]]):
        model = self.model_dict[model_key]
        inputs, predictor, outputs = parsers.get_sklearn_predictor(model_key, model)

        if custom_output_names:
            if len(custom_output_names) != len(outputs):
                raise ValueError('Number of requested custom output names '
                                 'does not match the number of outputs for this model')
        else:
            custom_output_names = outputs

        x = np.reshape(df[inputs].values, (-1, len(inputs)))
        y = np.reshape(predictor.predict(x), (-1, len(outputs)))

        columns = list(df.columns.values)
        for index, output_name in enumerate(custom_output_names):
            if output_name in columns:
                df.loc[:, output_name] = y[:, index]
            else:
                df[output_name] = y[:, index]
        return df
