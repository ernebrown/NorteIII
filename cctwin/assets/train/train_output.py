from marshmallow import Schema, fields, missing, post_dump

from cctwin.assets.ctg.ctg_output import CtgBiddingOutputSchema, CtgOutput, CtgSimulationOutputSchema
from cctwin.assets.hrsg.hrsg_output import HrsgBiddingOutputSchema, HrsgOutput, HrsgSimulationOutputSchema
from cctwin.assets.inletconditioner.inlet_conditioner_output import InletConditionerBiddingOutputSchema, \
    InletConditionerOutput, InletConditionerSimulationOutputSchema


class TrainOutput:
    def __init__(self,
                 inlet_conditioner_output: InletConditionerOutput,
                 ctg_output: CtgOutput,
                 hrsg_output: HrsgOutput
                 ):
        self.inlet_conditioner_output = inlet_conditioner_output
        self.ctg_output = ctg_output
        self.hrsg_output = hrsg_output


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


class TrainSimulationOutputSchema(BaseSchema):
    class Meta:
        ordered = True

    inlet_conditioner = fields.Nested(InletConditionerSimulationOutputSchema(), attribute='inlet_conditioner_output')
    ctg = fields.Nested(CtgSimulationOutputSchema(), attribute='ctg_output')
    hrsg = fields.Nested(HrsgSimulationOutputSchema(), attribute='hrsg_output')


class TrainBiddingOutputSchema(BaseSchema):
    class Meta:
        ordered = True

    inlet_conditioner = fields.Nested(InletConditionerBiddingOutputSchema(), attribute='inlet_conditioner_output')
    ctg = fields.Nested(CtgBiddingOutputSchema(), attribute='ctg_output')
    hrsg = fields.Nested(HrsgBiddingOutputSchema(), attribute='hrsg_output')
