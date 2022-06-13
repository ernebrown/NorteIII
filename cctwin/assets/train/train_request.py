from typing import Union

from marshmallow import Schema, fields, post_load

from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.hrsg.duct_burner_mode import DuctBurnerMode
from cctwin.assets.inletconditioner.inlet_conditioner_constants import InletConditionerConstants


class TrainSimulationRequest:
    def __init__(self,
                 ctg: str,
                 ctg_mode: Union[str, CtgOperationMode],
                 ctg_availability: Union[int, float],
                 is_inlet_conditioner_on: bool,
                 inlet_conditioner_availability: Union[int, float],
                 duct_burner_mode: [str, DuctBurnerMode],
                 duct_burner_fuel: Union[int, float],
                 is_pag_on: bool,
                 pag_availability: Union[int, float],
                 is_wc_on: bool,
                 wc_availability: Union[int, float],
                 is_peak_fire_on: bool,
                 igv_input: Union[None,bool],
                 igv: Union[None, float]
                 ):
        self.ctg = ctg
        if isinstance(ctg_mode, str):
            self.ctg_mode = ctg_mode
        elif isinstance(ctg_mode, CtgOperationMode):
            self.ctg_mode = ctg_mode.value
        self.ctg_availability = ctg_availability
        self.is_inlet_conditioner_on = is_inlet_conditioner_on
        self.inlet_conditioner_availability = inlet_conditioner_availability
        if isinstance(duct_burner_mode, str):
            self.duct_burner_mode = duct_burner_mode
        elif isinstance(duct_burner_mode, DuctBurnerMode):
            self.duct_burner_mode = duct_burner_mode.value
        self.duct_burner_fuel = duct_burner_fuel
        self.is_pag_on = is_pag_on
        self.pag_availability = pag_availability
        self.is_wc_on = is_wc_on
        self.wc_availability = wc_availability
        self.is_peak_fire_on = is_peak_fire_on
        self.igv_input = igv_input
        self.igv = igv


class TrainBiddingRequest:
    def __init__(self,
                 ctg: str,
                 ctg_availability: Union[int, float],
                 inlet_conditioner_availability: Union[int, float],
                 duct_burner_availability: Union[int, float],
                 pag_availability: Union[int, float],
                 wc_availability: Union[int, float]
                 ):
        self.ctg = ctg
        self.ctg_availability = ctg_availability
        self.inlet_conditioner_availability = inlet_conditioner_availability
        self.duct_burner_availability = duct_burner_availability
        self.pag_availability = pag_availability
        self.wc_availability = wc_availability


class TrainSimulationRequestSchema(Schema):
    class Meta:
        ordered = True

    ctg = fields.String()
    ctg_mode = fields.String()
    ctg_availability = fields.Number()
    is_inlet_conditioner_on = fields.Bool()
    inlet_conditioner_availability = fields.Number()
    duct_burner_mode = fields.String()
    duct_burner_fuel = fields.Number()
    is_pag_on = fields.Bool()
    pag_availability = fields.Number()
    is_wc_on = fields.Bool()
    wc_availability = fields.Number()
    is_peak_fire_on = fields.Bool()
    igv_input = fields.Bool(allow_none=True)
    igv = fields.Number(allow_none=True)

    @post_load
    def create_train_simulation_request(self, data, **kwargs):
        return TrainSimulationRequest(**data)


class TrainBiddingRequestSchema(Schema):
    class Meta:
        ordered = True

    ctg = fields.String()
    ctg_availability = fields.Number()
    inlet_conditioner_availability = fields.Number()
    duct_burner_availability = fields.Number()
    pag_availability = fields.Number()
    wc_availability = fields.Number()

    @post_load
    def create_train_bidding_request(self, data, **kwargs):
        return TrainBiddingRequest(**data)
