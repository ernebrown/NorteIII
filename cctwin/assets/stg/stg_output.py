from marshmallow import Schema, fields, missing, post_dump
from typing import Optional, Union


class StgOutput:
    def __init__(self,
                 name: str,
                 mw: list,
                 back_press: list,
                 circ_water_temp: list,
                 train_hp: Optional[Union[list, None]]):

        if not isinstance(name, str):
            raise TypeError('NAME should be a string representing STG\'s name')

        if not isinstance(mw, list):
            raise TypeError('MW should be a list of values')

        if not isinstance(back_press, list):
            raise TypeError('BACK PRESSURE should be a list of values')

        if not isinstance(circ_water_temp, list):
            raise TypeError('CIRC WATER TEMPERATURE should be a list of values')

        self.name = name
        self.mw = mw
        self.back_press = back_press
        self.circ_water_temp = circ_water_temp
        self.train_hp = train_hp


class BaseSchema(Schema):
    def on_bind_field(self, field_name, field_obj):
        # Override default missing attribute so
        # that missing values deserialize to None
        if field_obj.missing == missing:
            field_obj.missing = None
            field_obj.allow_none = True

    @post_dump
    def clean_missing(self, data, **kwargs):
        ret = data.copy()
        for key in filter(lambda key: data[key] is None, data):
            del ret[key]
        return ret


class StgSimulationOutputSchema(BaseSchema):
    class Meta:
        ordered = True

    name = fields.String()
    mw = fields.Method('get_first_mw')
    back_press = fields.Method('get_first_back_press')
    circ_water_temp = fields.Method('get_first_circ_water_temp')

    @classmethod
    def get_first_mw(cls, obj: StgOutput):
        return obj.mw[0]

    @classmethod
    def get_first_back_press(cls, obj: StgOutput):
        return obj.back_press[0]

    @classmethod
    def get_first_circ_water_temp(cls, obj: StgOutput):
        return obj.circ_water_temp[0]


class StgBiddingOutputSchema(BaseSchema):
    class Meta:
        ordered = True

    name = fields.String()
    mw = fields.List(fields.Number())
    back_press = fields.List(fields.Number())
    circ_water_temp = fields.List(fields.Number())
