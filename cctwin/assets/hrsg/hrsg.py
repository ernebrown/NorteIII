from typing import Union, Optional

import numpy as np
import pandas as pd
from scipy.optimize import fsolve
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.hrsg.hrsg_constants import HrsgConstants
from cctwin.assets.hrsg.hrsg_input import HrsgInput
from cctwin.assets.hrsg.hrsg_output import HrsgOutput
from cctwin.helper.asset_model_executor import ModelExecutor
from cctwin.assets.stg.stg_output import StgOutput
class Hrsg:
    def __init__(self,
                 name: str,
                 has_duct_burner: bool,
                 model_dict: dict):
        self.name = name
        self.has_duct_burner = has_duct_burner
        self.model_executor = ModelExecutor(model_dict)

    def get_performance(self, hrsg_input: HrsgInput, stg_fdbk: Optional[StgOutput]) -> HrsgOutput:

        input_dict = {
            'mw': hrsg_input.ctg_mw,
            'exh_temp': hrsg_input.ctg_exh_temp
        }
        df = pd.DataFrame.from_dict(input_dict)
        df['db_fuel'] = 0.0
        df['hp_flow'] = 0.0
        df['hp_press'] = 0.0
        df['hp_temp'] = 0.0
        df['hp_sh_temp'] = 0.0
        df['hrh_flow'] = 0.0
        df['hrh_press'] = 0.0
        df['hrh_temp'] = 0.0
        df['lp_flow'] = 0.0
        df['lp_temp'] = 0.0
        df['lp_press'] = 0.0
        if hrsg_input.ctg_mode == CtgOperationMode.OFFLINE.value or hrsg_input.ctg_avail == 0:
            return create_hrsg_output(df)

        if self.has_duct_burner and hrsg_input.ctg_mode != CtgOperationMode.OFFLINE.value:
            df.loc[:, 'db_fuel'] = hrsg_input.db_fuel

            # TODO skip solver except for when DB avail is more than 0

            # Solve for db fuel such that HP SH Temp limit is not violated
            model_key = 'hp<super_heat_temp><mw|exh_temp|db_fuel>'
            model = self.model_executor.model_dict[model_key]

            df.loc[:, 'db_fuel'] = maximize_db_fuel(df, model, HrsgConstants.MAX_FUEL,
                                                    HrsgConstants.HP_SH_TEMP_LIMIT,0)

            # Solve for db fuel such that HP Press limit is not violated
            model_key = 'hp<press|temp><mw|exh_temp|db_fuel>'
            model = self.model_executor.model_dict[model_key]

            df.loc[:, 'db_fuel'] = maximize_db_fuel(df, model, HrsgConstants.MAX_FUEL,
                                                    HrsgConstants.HP_PRESS_LIMIT, 0)

            # Use the calculated DB fuel to get HP Flow, Press and Temp values
            model_key = 'hp<flow><mw|exh_temp|db_fuel>'
            df = self.model_executor.append_predictions(model_key=model_key, df=df,
                                                        custom_output_names=['hp_flow'])
            model_key = 'hp<press|temp><mw|exh_temp|db_fuel>'
            df = self.model_executor.append_predictions(model_key=model_key, df=df,
                                                        custom_output_names=['hp_press', 'hp_temp'])
            model_key = 'hp<super_heat_temp><mw|exh_temp|db_fuel>'
            df = self.model_executor.append_predictions(model_key=model_key, df=df,
                                                        custom_output_names=['hp_sh_temp'])

            # Use the calculated DB fuel to get HRH Flow, Press and Temp values
            model_key = 'hrh<flow><mw|exh_temp|db_fuel>'
            df = self.model_executor.append_predictions(model_key=model_key, df=df,
                                                        custom_output_names=['hrh_flow'])

            model_key = 'hrh<press|temp><mw|exh_temp|db_fuel>'
            df = self.model_executor.append_predictions(model_key=model_key, df=df,
                                                        custom_output_names=['hrh_press', 'hrh_temp'])
            # Use the calculated DB fuel to get LP Flow, Press and Temp values
            model_key = 'lp<flow><mw|exh_temp|db_fuel>'
            df = self.model_executor.append_predictions(model_key=model_key, df=df,
                                                        custom_output_names=['lp_flow'])

            model_key = 'lp<press|temp><mw|exh_temp|db_fuel>'
            df = self.model_executor.append_predictions(model_key=model_key, df=df,
                                                        custom_output_names=['lp_press', 'lp_temp'])

            if stg_fdbk and 0 not in stg_fdbk.train_hp:
                df['hp_stg'] = np.asarray(stg_fdbk.train_hp)
                df['hp_flow'] = df['hp_stg']
                model_key = 'hp<flow><mw|exh_temp|db_fuel>'
                model = self.model_executor.model_dict[model_key]
                df.loc[:, 'db_fuel'] = maximize_db_fuel_hpflow(df, model, 0)

                model_key = 'hp<press|temp><mw|exh_temp|db_fuel>'
                df = self.model_executor.append_predictions(model_key=model_key, df=df,
                                                            custom_output_names=['hp_press', 'hp_temp'])
                model_key = 'hp<super_heat_temp><mw|exh_temp|db_fuel>'
                df = self.model_executor.append_predictions(model_key=model_key, df=df,
                                                            custom_output_names=['hp_sh_temp'])

                # Use the calculated DB fuel to get HRH Flow, Press and Temp values
                model_key = 'hrh<flow><mw|exh_temp|db_fuel>'
                df = self.model_executor.append_predictions(model_key=model_key, df=df,
                                                            custom_output_names=['hrh_flow'])

                model_key = 'hrh<press|temp><mw|exh_temp|db_fuel>'
                df = self.model_executor.append_predictions(model_key=model_key, df=df,
                                                            custom_output_names=['hrh_press', 'hrh_temp'])
                # Use the calculated DB fuel to get LP Flow, Press and Temp values
                model_key = 'lp<flow><mw|exh_temp|db_fuel>'
                df = self.model_executor.append_predictions(model_key=model_key, df=df,
                                                            custom_output_names=['lp_flow'])

                model_key = 'lp<press|temp><mw|exh_temp|db_fuel>'
                df = self.model_executor.append_predictions(model_key=model_key, df=df,
                                                            custom_output_names=['lp_press', 'lp_temp'])

            return create_hrsg_output(df)


def create_hrsg_output(df: pd.DataFrame) -> HrsgOutput:
    columns = df.columns.values

    duct_burner_fuel = None
    if 'db_fuel' in columns:
        duct_burner_fuel = list(df.db_fuel)

    hp_flow = list(df.hp_flow)
    hp_press = list(df.hp_press)
    hp_temp = list(df.hp_temp)
    hp_sh_temp = list(df.hp_sh_temp)

    hrh_flow = list(df.hrh_flow)
    hrh_press = list(df.hrh_press)
    hrh_temp = list(df.hrh_temp)

    lp_flow = list(df.lp_flow)
    lp_press = list(df.lp_press)
    lp_temp = list(df.lp_temp)

    return HrsgOutput(duct_burner_fuel=duct_burner_fuel,
                      hp_flow=hp_flow, hp_press=hp_press, hp_temp=hp_temp, hp_sh_temp=hp_sh_temp,
                      hrh_flow=hrh_flow, hrh_press=hrh_press, hrh_temp=hrh_temp,
                      lp_flow=lp_flow, lp_press=lp_press, lp_temp=lp_temp)



def __solve_for_db_fuel(db_fuel, *data):
    db_fuel = db_fuel[0]
    mw, exh_temp, limit, idx, model = data
    x = np.asarray([mw, exh_temp, db_fuel]).reshape(1, -1)
    y = model.predict(x).reshape(1, -1)
    pred_value = y[0, idx]
    error = pred_value - limit
    return error


def maximize_db_fuel(df: pd.DataFrame, model, max_fuel: Union[int, float], limit: Union[int, float],
                     prediction_index: int):
    max_db_fuel = []
    for mw, exh_temp, x0, current_fuel in zip(df['mw'], df['exh_temp'], df['db_fuel'], df['db_fuel']):
        data = (mw, exh_temp, limit, prediction_index, model)
        db_fuel = fsolve(func=__solve_for_db_fuel,
                         args=data,
                         x0=x0,
                         xtol=1e-6)
        db_fuel = db_fuel[0].reshape(1, -1)
        db_fuel = min(max_fuel, db_fuel[0, 0], current_fuel)
        max_db_fuel.append(db_fuel)
    return max_db_fuel


def maximize_db_fuel_hpflow(df: pd.DataFrame, model,prediction_index: int):
    max_db_fuel = []
    for mw, exh_temp, limit, x0, current_fuel in zip(df['mw'], df['exh_temp'], df['hp_flow'], df['db_fuel'], df['db_fuel']):
        data = (mw, exh_temp,limit, prediction_index, model)
        db_fuel = fsolve(func=__solve_for_db_fuel,
                         args=data,
                         x0=x0,
                         xtol=1e-6)
        db_fuel = db_fuel[0].reshape(1, -1)
        db_fuel = min(db_fuel[0, 0], current_fuel)
        max_db_fuel.append(db_fuel)
    return max_db_fuel
