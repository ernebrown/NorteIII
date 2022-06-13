import json
from typing import Union

import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.optimize import (fsolve, minimize)

from cctwin.assets.ctg.ctg_constants import CtgConstants
from cctwin.assets.ctg.ctg_incrementals import PagIncremental, PeakFireIncremental, WCIncremental
from cctwin.assets.ctg.ctg_input import CtgInput
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.ctg.ctg_output import CtgOutput
from cctwin.assets.inletconditioner.inlet_conditioner import InletConditioner
from cctwin.helper.asset_model_executor import ModelExecutor


class GasTurbine:
    def __init__(self, name: str,
                 inlet_conditioner: InletConditioner,
                 shaft_limit: Union[int, float],
                 fuel_limit: Union[int, float],
                 exh_limit:Union[int, float],
                 model_dict: dict,
                 pag_incremental: Union[None, PagIncremental],
                 peak_incremental: Union[None, PeakFireIncremental],
                 wc_incremental: Union[None, WCIncremental],
                 base_load_threshold: Union[int, float],
                 default1x1: bool
                 ):
        self.name = name
        self.inlet_conditioner = inlet_conditioner
        self.shaft_limit = shaft_limit
        self.fuel_limit = fuel_limit
        self.exh_limit = exh_limit
        self.pag_incremental = pag_incremental
        self.peak_fire_incremental = peak_incremental
        self.wc_incremental = wc_incremental
        self.base_load_threshold = base_load_threshold
        self.default1x1 = default1x1
        self.model_executor = ModelExecutor(model_dict)

    @property
    def shaft_limit(self):
        return self.__shaft_limit

    @shaft_limit.setter
    def shaft_limit(self, value: Union[int, float]):
        if not value > 0:
            raise ValueError('Shaft limit cannot be equal to or less than 0')
        self.__shaft_limit = value

    @property
    def fuel_limit(self):
        return self.__fuel_limit

    @fuel_limit.setter
    def fuel_limit(self, value: Union[int, float]):
        if not value > 0:
            raise ValueError('Fuel limit cannot be equal to or less than 0')
        self.__fuel_limit = value

    @property
    def exh_limit(self):
        return self.__exh_limit

    @exh_limit.setter
    def exh_limit(self, value: Union[int, float]):
        if not value > 0:
            raise ValueError('Exhaust Temp limit cannot be equal to or less than 0')
        self.__exh_limit = value

    @property
    def base_load_threshold(self):
        return self.__base_load_threshold

    @base_load_threshold.setter
    def base_load_threshold(self, value: Union[int, float]):
        if not 80 <= value <= 100:
            raise ValueError('Base load threshold should be a value between 80 and 100')
        self.__base_load_threshold = value

    def to_dict(self):
        data = {
            'name': self.name,
            'shaft_limit': self.shaft_limit,
            'fuel_limit': self.fuel_limit,
        }
        return data

    def from_dict(self, data):
        for field in []:
            if field in data:
                setattr(self, field, data[field])

    def to_json(self):
        data = self.to_dict()
        return json.dumps(data, indent=4)

    def get_performance(self, ctg_input: CtgInput) -> CtgOutput:

        input_dict = {'cit': ctg_input.cit, 'baro': ctg_input.baro,
                      'db': ctg_input.db, 'rh': ctg_input.rh}
        df: DataFrame = pd.DataFrame.from_dict(input_dict)
        df['mw'] = 0.0
        df['fuel'] = 0.0
        df['cpd'] = 0.0
        df['ctd'] = 0.0
        df['exh_temp'] = 0.0
        df['igv'] = 0.0

        if self.pag_incremental:
            df['pag_mw'] = 0.0
            df['pag_fuel'] = 0.0
            df['pag_exh_temp'] = 0.0
            df['pag_steam'] = 0.0
        if self.peak_fire_incremental:
            df['peak_fire_mw'] = 0.0
            df['peak_fire_fuel'] = 0.0
            df['peak_fire_exh_temp'] = 0.0
        if self.wc_incremental:
            df['wc_mw'] = 0.0
            df['wc_fuel'] = 0.0
            df['wc_exh_temp'] = 0.0

        if ctg_input.ctg_operation_mode == CtgOperationMode.OFFLINE.value:
            return create_ctg_output(self.name, df)

        if ctg_input.ctg_avlblty == 0.0:
            return create_ctg_output(self.name, df)

        # If operation mode is set to Base-Load

        if ctg_input.ctg_operation_mode == CtgOperationMode.BASELOAD.value:
            # when ctg avail changes we go to part load performance
            if ctg_input.ctg_avlblty < 100:
                df = self.__get_part_load_performance(ctg_avlblty=ctg_input.ctg_avlblty, df=df)
            else:
                df = self.__get_base_load_performance(ctg_input, df)
            return create_ctg_output(self.name, df)

        # If operation mode is set to Min-Load then run as MINLOAD
        if ctg_input.ctg_operation_mode == CtgOperationMode.MINLOAD.value:
            df = self.__get_min_load_performance(ctg_input.site_config, df)
            return create_ctg_output(self.name, df)

        # If operation mode is set to Part-Load with IGV Input
        if ctg_input.ctg_operation_mode == CtgOperationMode.PARTLOAD.value:
            df = self.__get_part_igv_performance(ctg_input.igv, df)
            return create_ctg_output(self.name, df)


        # If operation mode is set to AGC Mode
        if ctg_input.ctg_operation_mode == CtgOperationMode.AGCLOAD.value:
            if ctg_input.ctg_avlblty < CtgConstants.AGC_SETPT:
                df = self.__get_part_load_performance(ctg_avlblty=ctg_input.ctg_avlblty, df=df)
            else:
                df = self.__get_part_load_performance(ctg_avlblty=CtgConstants.AGC_SETPT, df=df)
            return create_ctg_output(self.name, df)


    def __get_min_load_performance(self, site_config: str, df: pd.DataFrame) -> pd.DataFrame:

        # Get CIT for Min-load by selecting right model based on MXN run config
        model_key = 'min2x1<igv><cit>'
        if site_config.startswith('1'):
            model_key = 'min1x1<igv><cit>'

        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Get CPD, CTD for Min-load
        model_key = 'part<cpd><baro|cit|igv>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        model_key = 'part<ctd><baro|cit|igv>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Get ExhTemp for Min-load
        model_key = 'part<exh_temp><igv|cpd>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)
        # Apply Exhaust-limit to min load
        df.loc[:, 'exh_temp'] = [min(self.exh_limit, exhtemp ) for exhtemp in df['exh_temp']]

        # Get MW for Min-load
        model_key = 'part<mw><cit|igv>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Get Fuel for Min-load
        model_key = 'part<fuel><igv|mw>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        return df

    def __get_part_load_performance(self, ctg_avlblty: Union[int, float], df: pd.DataFrame) -> pd.DataFrame:

        # Get CPD and CTD for Base-load
        model_key = 'base<cpd><baro|cit>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        model_key = 'base<ctd><baro|cit>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Get ExhTemp for Base-load
        model_key = 'base<exh_temp><cpd>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Get output for Base-load mw
        model_key = 'base<mw><cit|cpd|ctd|exh_temp>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Apply Ctg availability
        df.loc[:, 'mw'] = df['mw'] * ctg_avlblty / 100

        # Solve for IGV with given baro and cit such that output matches part-load mw.
        # set starting point for solver as min_igv setting
        df.loc[:, 'igv'] = CtgConstants.MIN_IGV
        model_key = 'part<mw><cit|igv>'
        model = self.model_executor.model_dict[model_key]

        df.loc[:, 'igv'] = predict_igv_using_fsolve(df, model)

        # Get CPD, CTD for Part-load using predicted IGV
        model_key = 'part<cpd><baro|cit|igv>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        model_key = 'part<ctd><baro|cit|igv>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Get ExhTemp for Part-load
        model_key = 'part<exh_temp><igv|cpd>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Apply Exhaust-limit to min load
        df.loc[:, 'exh_temp'] = [min(self.exh_limit, exhtemp) for exhtemp in df['exh_temp']]

        # Get MW for Part-load
        model_key = 'part<mw><cit|igv>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Get Fuel for Part-load
        model_key = 'part<fuel><igv|mw>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        return df

    def __get_base_load_performance(self, ctg_input: CtgInput, df: pd.DataFrame) -> pd.DataFrame:

        # Get CPD and CTD for Base-load
        model_key = 'base<cpd><baro|cit>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        model_key = 'base<ctd><baro|cit>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Get ExhTemp for Base-load
        model_key = 'base<exh_temp><cpd>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Get output for Base-load
        model_key = 'base<mw><cit|cpd|ctd|exh_temp>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Apply shaft-limit to Base-Load output
        df.loc[:, 'mw'] = [min(self.shaft_limit, base_output * ctg_input.ctg_avlblty / 100) for base_output in df['mw']]

        df.loc[:, 'igv'] = CtgConstants.BASE_IGV

        # Get Fuel for Base-load
        model_key = 'base<fuel><mw>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Apply PAG incremental values if PAG incremental object exists
        if self.pag_incremental:
            pag_incremental_output = self.pag_incremental.mw * (ctg_input.pag_avlblty / 100)
            if pag_incremental_output > 0:
                # Apply pag incremental output while keeping shaft-limit in check
                df.loc[:, 'pag_mw'] = [(min(pag_incremental_output, max(0, self.shaft_limit - base_output)))
                                       for base_output in df['mw']]

                ratio_pag_incremental_mw = df['pag_mw'] / self.pag_incremental.mw

                # Apply incremental pag fuel, exh_temp and steam proportional to applied incremental pag output
                df.loc[:, 'pag_fuel'] = self.pag_incremental.fuel * ratio_pag_incremental_mw
                df.loc[:, 'pag_steam'] = self.pag_incremental.steam * ratio_pag_incremental_mw
                df.loc[:, 'pag_exh_temp'] = self.pag_incremental.exh_temp * ratio_pag_incremental_mw

                df.loc[:, 'mw'] += df['pag_mw']
                df.loc[:, 'fuel'] += df['pag_fuel']
                df.loc[:, 'exh_temp'] += df['pag_exh_temp']

        # Apply Wet Compression incremental values if Wet Compression incremental object exists
        if self.wc_incremental:
            avlblty = [(ctg_input.wc_avlblty)]
            avlblty_updated = [avlblty[i] if df.loc[i,'db'] >= CtgConstants.MIN_WC_DB else 0
                               for i in range(len(avlblty))]

            wc_incremental_output = [self.wc_incremental.mw * (avlblty_updated[i] / 100) for i in range(len(avlblty))]
            wc_mw=[min(wc_incremental_output[i],max(0, self.shaft_limit - df.loc[i,'mw']))
                   for i in range(len(wc_incremental_output))]
            #df['wc_mw'] = df['wc_incremental'].apply(lambda incr_mw: (min(incr_mw, max(0, self.shaft_limit - base_output))))
            #                           for base_output in df['mw']]

            df.loc[:,'wc_mw']=wc_mw
            ratio_wc_incremental_mw = df['wc_mw'] / self.wc_incremental.mw

                # Apply incremental Wet Compression fuel, exh_temp to applied incremental Wet Compression output
            df.loc[:, 'wc_fuel'] = self.wc_incremental.fuel * ratio_wc_incremental_mw
            df.loc[:, 'wc_exh_temp'] = self.wc_incremental.exh_temp * ratio_wc_incremental_mw

            df.loc[:, 'mw'] += df['wc_mw']
            df.loc[:, 'fuel'] += df['wc_fuel']
            df.loc[:, 'exh_temp'] += df['wc_exh_temp']

        # Apply PEAK-FIRE incremental values if PEAK-FIRE incremental object exists
        if self.peak_fire_incremental:
            peak_incremental_output = self.peak_fire_incremental.mw * (ctg_input.is_peak_fire_on / 100)
            if peak_incremental_output > 0:
                # Apply peak-fire incremental output while keeping shaft-limit in check
                df.loc[:, 'peak_fire_mw'] = [(min(peak_incremental_output, max(0, self.shaft_limit - base_output)))
                                             for base_output in df['mw']]

                ratio_peak_fire_incremental_mw = df['peak_fire_mw'] / self.peak_fire_incremental.mw

                # Apply incremental peak-fire fuel and exh_temp proportional to applied incremental peak-fire output
                df.loc[:, 'peak_fire_fuel'] = self.peak_fire_incremental.fuel * ratio_peak_fire_incremental_mw
                df.loc[:, 'peak_fire_exh_temp'] = self.peak_fire_incremental.exh_temp * ratio_peak_fire_incremental_mw

                df.loc[:, 'mw'] += df['peak_fire_mw']
                df.loc[:, 'fuel'] += df['peak_fire_fuel']
                df.loc[:, 'exh_temp'] += df['peak_fire_exh_temp']

        return df

# This is mainly for using with Part load monitoring where IGV gets passed as input

    def __get_part_igv_performance(self, igv: Union[None, float], df: pd.DataFrame) -> pd.DataFrame:
        df.loc[:, 'igv'] = igv
        # Get CPD, CTD for Part-load using predicted IGV
        model_key = 'part<cpd><baro|cit|igv>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)
        model_key = 'part<ctd><baro|cit|igv>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Get ExhTemp for Part-load
        model_key = 'part<exh_temp><igv|cpd>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Apply Exhaust-limit to min load
        df.loc[:, 'exh_temp'] = [min(self.exh_limit, exhtemp) for exhtemp in df['exh_temp']]

        # Get MW for Part-load
        model_key = 'part<mw><cit|igv>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Get Fuel for Part-load
        model_key = 'part<fuel><igv|mw>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        return df

def create_ctg_output(ctg_name: str, df: pd.DataFrame) -> CtgOutput:
    try:
        pag_mw = list(df.pag_mw)
        pag_fuel = list(df.pag_fuel)
        pag_steam = list(df.pag_steam)
        pag_exh_temp = list(df.pag_exh_temp)
    except AttributeError:
        pag_mw = None
        pag_fuel = None
        pag_steam = None
        pag_exh_temp = None

    try:
        peak_fire_mw = list(df.peak_fire_mw)
        peak_fire_fuel = list(df.peak_fire_fuel)
        peak_fire_exh_temp = list(df.peak_fire_exh_temp)
    except AttributeError:
        peak_fire_mw = None
        peak_fire_fuel = None
        peak_fire_exh_temp = None

    ctg_output = CtgOutput(name=ctg_name, cit=list(df.cit), igv=list(df.igv),
                           mw=list(df.mw), fuel=list(df.fuel),
                           cpd=list(df.cpd), ctd=list(df.ctd), exh_temp=list(df.exh_temp),
                           pag_mw=pag_mw, pag_fuel=pag_fuel, pag_exh_temp=pag_exh_temp, pag_steam=pag_steam,
                           wc_mw=pag_mw, wc_fuel=pag_fuel, wc_exh_temp=pag_exh_temp,
                           peak_fire_mw=peak_fire_mw, peak_fire_fuel=peak_fire_fuel,
                           peak_fire_exh_temp=peak_fire_exh_temp)
    return ctg_output


def __minimize_prediction_error(igv, *data) -> float:
    igv = igv[0]
    cit, mw, model = data
    x = np.asarray([cit, igv]).reshape(1, -1)
    y = model.predict(x).reshape(1, -1)
    pred_mw = y[0, 2]
    error = abs(pred_mw - mw)
    return error


def __solve_for_output(igv, *data) -> float:
    igv = igv[0]
    cit, mw, model = data
    x = np.asarray([cit, igv]).reshape(1, -1)
    y = model.predict(x).reshape(1, -1)
    pred_mw = y[0,0]
    error = pred_mw - mw
    return error


def predict_igv_using_minimize(df: pd.DataFrame, model) -> list:
    min_igv = []
    for c, o, x0 in zip(df['cit'], df['mw'], df['igv']):
        data = (c, o, model)
        result = minimize(fun=__minimize_prediction_error,
                          args=data,
                          x0=x0,
                          method='Nelder-Mead',
                          options={'gtol': 1e-6, 'disp': True})
        igv = result.x.reshape(1, -1)
        min_igv.append(igv[0, 0])
    return min_igv


def predict_igv_using_fsolve(df: pd.DataFrame, model) -> list:
    min_igv = []
    for c, o, x0 in zip(df['cit'], df['mw'], df['igv']):
        data = (c, o, model)
        igv = fsolve(func=__solve_for_output,
                     args=data,
                     x0=x0,
                     xtol=1e-6)
        igv = igv[0].reshape(1, -1)
        min_igv.append(igv[0, 0])
    return min_igv
