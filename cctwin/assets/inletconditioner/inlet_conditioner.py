import pandas as pd
import psychrolib

from cctwin.assets.inletconditioner.inlet_conditioner_constants import InletConditionerConstants
from cctwin.assets.inletconditioner.inlet_conditioner_input import InletConditionerInput
from cctwin.assets.inletconditioner.inlet_conditioner_output import InletConditionerOutput
from cctwin.assets.inletconditioner.inlet_conditioner_type import InletConditionerType
from cctwin.helper.asset_model_executor import ModelExecutor


class InletConditioner:
    def __init__(self, inlet_conditioning_system: InletConditionerType,
                 model_dict: dict):
        self._conditioning_system = inlet_conditioning_system
        self.model_executor = ModelExecutor(model_dict)
        psychrolib.SetUnitSystem(psychrolib.IP)

    @property
    def conditioning_system(self):
        return self._conditioning_system

    @conditioning_system.setter
    def conditioning_system(self, value: InletConditionerType):
        if not isinstance(value, InletConditionerType):
            raise TypeError('conditioning system should be of InletConditioningType')
        self._conditioning_system = value

    def get_performance(self, inlet_conditioner_input: InletConditionerInput):

        input_dict = {'db': inlet_conditioner_input.db,
                      'rh': inlet_conditioner_input.rh,
                      'baro': inlet_conditioner_input.baro,
                      }
        df = pd.DataFrame.from_dict(input_dict)

        # create a list of availability numbers based on requested dry-bulb temperature.
        # if requested db-temp is less than min db-temp limit, set availability to 0.
        # Here, availability is set to Max availability.

        avlblty = [inlet_conditioner_input.avlblty]
        avlblty_updated = [avlblty[i] if df.loc[i, 'db'] >= InletConditionerConstants.MIN_AMBIENT_DB_TEMP else 0.0
                           for i in range(len(avlblty))]
        df.loc[:, 'avlblty'] = avlblty_updated

        df.loc[:, 'wb'] = df.apply(lambda df_row:
                                   psychrolib.GetTWetBulbFromRelHum(df_row.db, df_row.rh, df_row.baro),
                                   axis=1)
        df.loc[:, 'dp'] = df.apply(lambda df_row:
                                   psychrolib.GetTDewPointFromRelHum(df_row.db, df_row.rh), axis=1)

        df.loc[:, 'cit'] = df['db']
        if self.conditioning_system == InletConditionerType.FOGGERS:

            performance_data = InletConditionerOutput(list(df.avlblty),
                                                      list(df.cit), load=None,
                                                      ton=None, evap_out=None)
            df.loc[:, 'approach'] = InletConditionerConstants.APPROACH_ADD

            df_for_prediction = df[df['avlblty'] > 0].copy()
            df_pass_through = df[df['avlblty'] == 0.0].copy()

            if len(df_for_prediction) > 0:
                model_key = 'forgger<cit><db|wb|approach|avlblty>'
                df_for_prediction = self.model_executor.append_predictions(model_key, df=df_for_prediction,
                                                                           custom_output_names=None)
            df_all: pd.DataFrame = pd.concat([df_pass_through, df_for_prediction], axis=0,
                                             ignore_index=False, sort=False).sort_index()

            df_all = df_all.reset_index()
            df_all.loc[:, 'cit'] = df_all['cit'].apply(lambda x: min(120, x))
            df_all.loc[:, 'new_cit'] = df_all.apply(lambda df_row: df_row.cit if df_row.cit <= df_row.db else df_row.db,
                                                    axis=1)
            performance_data.cit = list(df_all['new_cit'])

        if self.conditioning_system == InletConditionerType.EVAPORATIVE_COOLERS:


            performance_data = InletConditionerOutput(list(df.avlblty),
                                                      list(df.cit), load=None,
                                                      ton=None, evap_out=None)

            df_for_prediction = df[df['avlblty'] > 0].copy()
            df_pass_through = df[df['avlblty'] == 0.0].copy()

            if len(df_for_prediction) > 0:
                model_key = 'evap<cit><db|wb|avlblty>'
                df_for_prediction = self.model_executor.append_predictions(model_key, df=df_for_prediction,
                                                                           custom_output_names=None)
            df_all: pd.DataFrame = pd.concat([df_pass_through, df_for_prediction], axis=0,
                                             ignore_index=False, sort=False).sort_index()

            df_all = df_all.reset_index()
            df_all.loc[:, 'cit'] = df_all['cit'].apply(lambda x: min(120, x))

            df_all.loc[:,'new_cit']= df_all.apply(lambda df_row: df_row.cit if df_row.cit<=df_row.db else df_row.db,
                                                  axis=1)
            performance_data.cit = list(df_all['new_cit'])

        if self.conditioning_system == InletConditionerType.CHILLERS:

            df.loc[:, 'load'] = 0.0
            df.loc[:, 'ton'] = 0.0
            # df.loc[:, 'evap_in'] = df['db']
            df.loc[:, 'evap_out'] = df['db']
            df.loc[:, 'avlblty'] = df['avlblty'].apply(lambda x:
                                                       min(100, 100 * x / InletConditionerConstants.TON_DEFAULT))

            performance_data = InletConditionerOutput(list(df.avlblty),
                                                      list(df.cit), load=None,
                                                      ton=None, evap_out=None)

            df_for_prediction = df[df['avlblty'] > 0].copy()
            df_pass_through = df[df['avlblty'] == 0.0].copy()

            if len(df_for_prediction) > 0:
                model_key = 'chillerton<ton><db|rh|baro|avlblty>'
                df_for_prediction = self.model_executor.append_predictions(model_key, df=df_for_prediction,
                                                                           custom_output_names=['max_ton_used'])

                # If user requested tonnage is more than max ton used, set availability to 100
                # else calculate availability as percent of max ton available for given ambient conditions
                df_for_prediction.loc[:, 'newavlblty'] = df_for_prediction['max_ton_used'].apply(
                    lambda x: min(100, 100 * x/inlet_conditioner_input.avlblty))
                df_for_prediction['avlblty'] = df_for_prediction[['avlblty', 'newavlblty']].min(axis=1)

                model_key = 'chillercit<cit><db|rh|baro|avlblty>'
                df_for_prediction = self.model_executor.append_predictions(model_key, df=df_for_prediction,
                                                                           custom_output_names=None)
                model_key = 'chillerload<load><db|rh|baro|avlblty>'
                df_for_prediction = self.model_executor.append_predictions(model_key, df=df_for_prediction,
                                                                           custom_output_names=None)
                model_key = 'chillerton<ton><db|rh|baro|avlblty>'
                df_for_prediction = self.model_executor.append_predictions(model_key, df=df_for_prediction,
                                                                           custom_output_names=None)
                model_key = 'chillerevap<evap_out><db|rh|baro|avlblty>'
                df_for_prediction = self.model_executor.append_predictions(model_key, df=df_for_prediction,
                                                                           custom_output_names=None)

            df_all: pd.DataFrame = pd.concat([df_pass_through, df_for_prediction], axis=0,
                                             ignore_index=False, sort=False).sort_index()

            # Reset all tons from model which are higher than user requested ton
            df_all.loc[:, 'ton'] = df_all['ton'].apply(lambda x: min(inlet_conditioner_input.avlblty, x))

            # make sure CIT stays at or below amb
            df_all.loc[:, 'new_cit'] = df_all.apply(lambda df_row: df_row.cit if df_row.cit <= df_row.db else df_row.db,
                                                    axis=1)
            df_all = df_all.reset_index()
            performance_data.cit = list(df_all['new_cit'])
            performance_data.load = list(df_all.load)
            performance_data.ton = list(df_all.ton)
            # performance_data.evap_in = list(df.evap_in)
            performance_data.evap_out = list(df_all.evap_out)

        return performance_data
