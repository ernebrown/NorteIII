import numpy as np
import pandas as pd
from typing import Union, Optional
from scipy.optimize import fsolve

from cctwin.assets.condenser.condenser import Condenser
from cctwin.assets.condenser.condenser_input import CondenserInput
from cctwin.assets.stg.stg_input import StgInput
from cctwin.assets.stg.stg_output import StgOutput
from cctwin.helper.asset_model_executor import ModelExecutor


class SteamTurbine:
    def __init__(self,
                 name: str,
                 condenser: Condenser,
                 back_press_limit:Union[int, float],
                 shaft_limit: Union[int, float],
                 model_dict: dict):
        self.name = name
        self.condenser = condenser
        self.back_press_limit = back_press_limit
        self.shaft_limit = shaft_limit
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
    def back_press_limit(self):
        return self.__back_press_limit

    @back_press_limit.setter
    def back_press_limit(self, value: Union[int, float]):
        if value < 0:
            raise ValueError('Back pressure limit can not be less than 0')

        self.__back_press_limit = value

    def get_performance(self, stg_input: StgInput) -> StgOutput:
        condenser_input = CondenserInput(stg_input.ambient_conditions)
        circ_water_temp = self.condenser.get_performance(condenser_input)

        # TODO perform STG max check and solve for max DB
        # Get HP flows from every train
        hp_flow_list = [x.hrsg_output.hp_flow for x in stg_input.train_outputs]


        # Get HRH flows from every train
        hrh_flow_list = [x.hrsg_output.hrh_flow for x in stg_input.train_outputs]

        # Get LP flows  from every train
        lp_flow_list = [x.hrsg_output.lp_flow for x in stg_input.train_outputs]

        # Get total HP flow
        hp_flow = np.sum(hp_flow_list, axis=0)

        # Get total HRH flow
        hrh_flow = np.sum(hrh_flow_list, axis=0)

        # Get total LP flow
        lp_flow = np.sum(lp_flow_list, axis=0)

        input_dict = {'hp_flow': hp_flow,
                      'hrh_flow': hrh_flow,
                      'lp_flow':lp_flow,
                      'circ_water_temp': circ_water_temp,
                      'db': stg_input.ambient_conditions.db,
                      'rh': stg_input.ambient_conditions.rh,
                      'baro': stg_input.ambient_conditions.baro,
                      }

        df = pd.DataFrame.from_dict(input_dict)
        df['train_hp'] = 0.0
        df['mw'] = 0.0
        df['back_press'] = 0.0
        if np.count_nonzero(df['hp_flow'].values) == 0.0:
            return create_stg_output(self.name, df)


        # Get back_press prediction

        model_key = 'back_pressure<back_press><hp_flow|db|rh|baro>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        # Apply back pressure-limit, This is to account for data errors coming from instruments
        df.loc[:, 'back_press'] = [max(self.back_press_limit, bpress) for bpress in df['back_press']]

        if stg_input.site_config.startswith('1'):
            model_key = 'stg1x1<mw><hp_flow|db|rh|baro>'

            df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)
            return create_stg_output(self.name, df)

            # return StgOutput(self.name, list(df.mw), list(df.back_press), list(df.circ_water_temp),
            #                  list(df['train_hp']))

        else:
            model_key = 'stg2x1<mw><hp_flow|db|rh|baro>'
            model = self.model_executor.model_dict[model_key]
            df['old_hp_flow'] = df['hp_flow']
            df.loc[:, 'hp_flow'] = maximize_hp_flow(df, model, self.shaft_limit, 0)
            if list(df['old_hp_flow']) != list(df['hp_flow']):
                df['train_hp'] = df['hp_flow']/2
            model_key = 'back_pressure<back_press><hp_flow|db|rh|baro>'
            df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

            # Apply back pressure-limit, This is to account for data errors coming from instruments
            df.loc[:, 'back_press'] = [max(self.back_press_limit, bpress) for bpress in df['back_press']]

            model_key = 'stg2x1<mw><hp_flow|db|rh|baro>'
            df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

            return create_stg_output(self.name, df)


            # return StgOutput(self.name, list(df.mw), list(df.back_press), list(df.circ_water_temp),
            #                  list(df['train_hp']))


def create_stg_output(stg_name: str, df: pd.DataFrame) -> StgOutput:
    return StgOutput(name=stg_name, mw=list(df.mw), back_press=list(df['back_press']),
                     circ_water_temp=list(df.circ_water_temp), train_hp=list(df['train_hp']))



def __solve_for_hp_flow(hp_flow, *data):
    hp_flow = hp_flow[0]
    db, rh, baro, limit, idx, model = data
    x = np.asarray([ hp_flow,db, rh, baro]).reshape(1, -1)
    y = model.predict(x).reshape(1, -1)
    pred_value = y[0, idx]
    error = pred_value - limit
    return error


def maximize_hp_flow(df: pd.DataFrame, model, limit: Union[int, float],
                     prediction_index: int):
    max_hp_flow = []
    for x0, current_hp_flow, db, rh, baro in zip(df['hp_flow'], df['hp_flow'], df['db'], df['rh'], df['baro']):
        data = (db, rh, baro, limit, prediction_index, model)
        hp_flow = fsolve(func=__solve_for_hp_flow,
                         args=data,
                         x0=x0,
                         xtol=1e-6)
        hp_flow = hp_flow[0].reshape(1, -1)
        hp_flow = min(hp_flow[0, 0], current_hp_flow)
        max_hp_flow.append(hp_flow)
    return max_hp_flow
