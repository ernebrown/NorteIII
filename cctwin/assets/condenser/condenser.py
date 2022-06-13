import pandas as pd

from cctwin.assets.condenser.condenser_cooling_type import CondenserCoolingType
from cctwin.assets.condenser.condenser_input import CondenserInput
from cctwin.helper.asset_model_executor import ModelExecutor


class Condenser:
    def __init__(self,
                 cooling_type: CondenserCoolingType,
                 model_dict: dict):
        self.cooling_type = cooling_type
        self.model_executor = ModelExecutor(model_dict)

    def get_performance(self, condenser_input: CondenserInput):
        if self.cooling_type == CondenserCoolingType.AIR:
            return self.__get_performance_of_air_cooled_condenser(condenser_input)

        if self.cooling_type == CondenserCoolingType.WATER_COOLING_TOWER:
            return self.__get_performance_of_cooling_tower_condenser(condenser_input)

        if self.cooling_type == CondenserCoolingType.WATER_BODY:
            return self.__get_performance_of_water_body_condenser(condenser_input)

        else:
            raise NotImplementedError('Condenser cooling type not found')

    def __get_performance_of_water_body_condenser(self, inputs: CondenserInput):

        input_dict = {'db': inputs.ambient_conditions.db,
                      'rh': inputs.ambient_conditions.rh,
                      'baro': inputs.ambient_conditions.baro}
        df = pd.DataFrame.from_dict(input_dict)

        # Get circ water temp
        model_key = 'condenser<circ_water_temp><db|rh|baro>'
        df = self.model_executor.append_predictions(model_key=model_key, df=df, custom_output_names=None)

        return list(df['circ_water_temp'])

    def __get_performance_of_cooling_tower_condenser(self, inputs: CondenserInput):
        pass

    def __get_performance_of_air_cooled_condenser(self, inputs: CondenserInput):
        pass
