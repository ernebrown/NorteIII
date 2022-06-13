from typing import Union
from cctwin.assets.inletconditioner.inlet_conditioner_type import InletConditionerType
from marshmallow import Schema, fields, missing, post_dump


class InletConditionerOutput:
    def __init__(self,
                 avlblty: list,
                 cit: list,
                 load: Union[None, list],
                 ton: Union[None, list],
                 # evap_in: Union[None, list],
                 evap_out: Union[None, list]
                 ):
        if not isinstance(avlblty, list):
            raise TypeError('AVAILABILITY should be a list of values')

        if not isinstance(cit, list):
            raise TypeError('CIT should be a list of values')

        self.avlblty = avlblty
        self.cit = cit
        self.load = load
        self.ton = ton
        # self.evap_in = evap_in
        self.evap_out = evap_out


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


class InletConditionerSimulationOutputSchema(BaseSchema):
    class Meta:
        ordered = True


    cit = fields.Method('get_first_cit')
    load = fields.Method('get_first_load',required=False)
    ton = fields.Method('get_first_ton', required=False)
    # evap_in = fields.Method('get_first_evap_in', required=False)
    evap_out = fields.Method('get_first_evap_out', required=False)

    @classmethod
    def get_first_cit(cls, obj: InletConditionerOutput):
        return obj.cit[0]

    @classmethod
    def get_first_load(cls, obj: InletConditionerOutput):
        if obj.load:
            return obj.load[0]
        return None

    @classmethod
    def get_first_ton(cls, obj: InletConditionerOutput):
        if obj.ton:
            return obj.ton[0]
        return None

    # @classmethod
    # def get_first_evap_in(cls, obj: InletConditionerOutput):
    #     if obj.evap_in:
    #         return obj.evap_in[0]
    #     return None

    @classmethod
    def get_first_evap_out(cls, obj: InletConditionerOutput):
        if obj.evap_out:
            return obj.evap_out[0]
        return None


class InletConditionerBiddingOutputSchema(BaseSchema):
    class Meta:
        ordered = True

    cit = fields.List(fields.Number())
    load = fields.List(fields.Number(), required=False)
    ton = fields.List(fields.Number(), required=False)
    evap_out = fields.List(fields.Number(), required=False)
