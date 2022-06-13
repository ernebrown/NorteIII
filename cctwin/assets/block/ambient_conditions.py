from typing import List, Union

import pandas as pd
import psychrolib
from marshmallow import Schema, fields, post_load, pre_load

from cctwin.assets.block.block_constants import BlockConstants


class AmbientConditions:
    def __init__(self,
                 db: Union[int, float, List[Union[int, float]]],
                 rh: Union[int, float, List[Union[int, float]]],
                 baro: Union[int, float, List[Union[int, float]]]):

        self.db = db
        self.rh = rh
        self.baro = baro

        it = iter([self.db, self.rh, self.baro])
        length = len(next(it))

        if not all(len(l) == length for l in it):
            raise IndexError('Lists of DB, RH and BARO values should be of equal length')

        psychrolib.SetUnitSystem(psychrolib.IP)

        input_dict = {'db': self.db,
                      'rh': self.rh,
                      'baro': self.baro}
        df = pd.DataFrame.from_dict(input_dict)

        df.loc[:, 'wb'] = df.apply(lambda df_row:
                                   psychrolib.GetTWetBulbFromRelHum(df_row.db, df_row.rh, df_row.baro),
                                   axis=1)
        df.loc[:, 'dp'] = df.apply(lambda df_row:
                                   psychrolib.GetTDewPointFromRelHum(df_row.db, df_row.rh), axis=1)

        self.wb = list(df.wb)
        self.dp = list(df.dp)

    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, value: Union[Union[int, float], List[Union[int, float]]]):
        if isinstance(value, list):
            values = value
            if len(values) == 0:
                raise IndexError('List of DB temperature values  cannot be empty')
        else:
            if not isinstance(value, (int, float)):
                raise TypeError('DB temp value must be of type int or float')
            values = [value]

        if not all(BlockConstants.MIN_DB <= x <= BlockConstants.MAX_DB for x in values):
            raise ValueError(f'All DB temperature values in the list '
                             f'should be between {BlockConstants.MIN_DB} and {BlockConstants.MAX_DB} °F')
        self.__db = values

    @property
    def rh(self):
        return self.__rh

    @rh.setter
    def rh(self, value: Union[Union[int, float], List[Union[int, float]]]):
        if isinstance(value, list):
            values = value
            if len(values) == 0:
                raise IndexError('List of RH values  cannot be empty')
        else:
            if not isinstance(value, (int, float)):
                raise TypeError('RH value must be of type int or float')
            values = [value]

        if not all(BlockConstants.MIN_RH <= x <= BlockConstants.MAX_RH for x in values):
            raise ValueError(f'All RH values in the list '
                             f'should be between {BlockConstants.MIN_RH} and {BlockConstants.MAX_RH}')
        self.__rh = values

    @property
    def baro(self):
        return self.__baro

    @baro.setter
    def baro(self, value: Union[Union[int, float], List[Union[int, float]]]):
        if isinstance(value, list):
            values = value
            if len(values) == 0:
                raise IndexError('List of BARO pressure values cannot be empty')
        else:
            if not isinstance(value, (int, float)):
                raise TypeError('BARO PRESS value must be of type int or float')
            values = [value]

        if not all(BlockConstants.MIN_BARO <= x <= BlockConstants.MAX_BARO for x in values):
            raise ValueError(f'All BARO pressure values in the list '
                             f'should be between {BlockConstants.MIN_BARO} and {BlockConstants.MAX_BARO} psia')
        self.__baro = values


class AmbientConditionsSimulationSchema(Schema):
    class Meta:
        ordered = True

    db = fields.Method('get_first_db_value', deserialize='load_value')
    rh = fields.Method('get_first_rh_value', deserialize='load_value')
    baro = fields.Method('get_first_baro_value', deserialize='load_value')
    wb = fields.Method('get_first_wb_value', deserialize='load_value')
    dp = fields.Method('get_first_dp_value', deserialize='load_value')

    @post_load
    def create_ambient_conditions(self, data, **kwargs):
        return AmbientConditions(**data)

    @pre_load
    def convert_rh_to_fraction(self, data, **kwargs):
        rh = data['rh']
        if not isinstance(rh, list):
            rh = [rh]

        values = []
        for value in rh:
            if 1 < value <= 100:
                value = value / 100
            values.append(value)
        data['rh'] = values
        return data

    @staticmethod
    def load_value(value):
        if not isinstance(value, list):
            return [value]
        return value

    @classmethod
    def get_first_rh_value(cls, obj: AmbientConditions):
        return obj.rh[0] * 100

    @classmethod
    def get_first_db_value(cls, obj: AmbientConditions):
        return obj.db[0]

    @classmethod
    def get_first_baro_value(cls, obj: AmbientConditions):
        return obj.baro[0]

    @classmethod
    def get_first_wb_value(cls, obj: AmbientConditions):
        return obj.wb[0]

    @classmethod
    def get_first_dp_value(cls, obj: AmbientConditions):
        return obj.dp[0]
