from marshmallow import Schema, fields

from cctwin.assets.ctg.ctg import GasTurbine
from cctwin.assets.ctg.ctg_input import CtgInput
from cctwin.assets.ctg.ctg_constants import CtgConstants
from cctwin.assets.hrsg.hrsg import Hrsg
from cctwin.assets.hrsg.hrsg_constants import HrsgConstants
from cctwin.assets.inletconditioner.inlet_conditioner_constants import InletConditionerConstants
from cctwin.assets.inletconditioner.inlet_conditioner_type import InletConditionerType


class Train:
    def __init__(self, ctg: GasTurbine, hrsg: Hrsg):
        self.ctg = ctg
        self.hrsg = hrsg

        self.has_inlet_conditioning = self.ctg.inlet_conditioner != InletConditionerType.NONE
        self.has_duct_burner = hrsg.has_duct_burner
        self.default1x1 = ctg.default1x1
        self.can_pag = self.ctg.pag_incremental is not None
        self.can_peak_fire = self.ctg.peak_fire_incremental is not None
        self.can_wc = self.ctg.wc_incremental is not None


class TrainSimulationSchema(Schema):
    class Meta:
        ordered = True

    ctg = fields.Method('get_ctg_name')
    has_inlet_conditioning = fields.Boolean()
    min_dry_bulb_for_inlet_conditioning = fields.Number(default=InletConditionerConstants.MIN_AMBIENT_DB_TEMP)
    min_inlet_conditioning_avlblty = fields.Number(default=InletConditionerConstants.MIN_AVLBLTY)
    max_inlet_conditioning_avlblty = fields.Number(default=InletConditionerConstants.MAX_AVLBLTY)
    default_inlet_conditioning_avlblty = fields.Number(default=InletConditionerConstants.TON_DEFAULT)
    min_ctg_avlblty = fields.Number(default=CtgConstants.MIN_CTG_AVLBLTY)
    max_ctg_avlblty = fields.Number(default=CtgConstants.MAX_CTG_AVLBLTY)
    default_ctg_avlblty = fields.Number(default=CtgConstants.BASE_CTG_AVLBLTY)
    default_wc_avlblty = fields.Number(default=CtgConstants.DEFAULT_WC_AVLBLTY)
    max_wc_avlblty = fields.Number(default=CtgConstants.MAX_WC_AVLBLTY)
    default_pag_avlblty = fields.Number(default=CtgConstants.DEFAULT_PAG_AVLBLTY)
    max_pag_avlblty = fields.Number(default=CtgConstants.MAX_PAG_AVLBLTY)
    default_pf_avlblty = fields.Number(default=CtgConstants.DEFAULT_PF_AVLBLTY)
    max_pf_avlblty = fields.Number(default=CtgConstants.MAX_PF_AVLBLTY)
    min_base_load_threshold = fields.Number(default=CtgConstants.MIN_BASE_LOAD_THRESHOLD)
    has_duct_burner = fields.Boolean()
    max_db_fuel = fields.Number(default=HrsgConstants.MAX_FUEL)
    can_pag = fields.Boolean()
    can_wc= fields.Boolean()
    can_peak_fire = fields.Boolean()
    base_igv=fields.Number(default=CtgConstants.BASE_IGV)
    default1x1 = fields.Boolean()

    @classmethod
    def get_ctg_name(cls, obj: Train):
        return obj.ctg.name


class TrainBiddingSchema(Schema):
    class Meta:
        ordered = True

    ctg = fields.Method('get_ctg_name')
    has_inlet_conditioning = fields.Boolean()
    min_inlet_conditioning_avlblty = fields.Number(default=InletConditionerConstants.MIN_AVLBLTY)
    max_inlet_conditioning_avlblty = fields.Number(default=InletConditionerConstants.MAX_AVLBLTY)
    default_inlet_conditioning_avlblty = fields.Number(default=InletConditionerConstants.TON_DEFAULT)
    min_ctg_avlblty = fields.Number(default=0)
    max_ctg_avlblty = fields.Number(default=CtgConstants.MAX_CTG_AVLBLTY)
    default_ctg_avlblty = fields.Number(default=CtgConstants.BASE_CTG_AVLBLTY)
    default_ctg_avlblty = fields.Number(default=CtgConstants.BASE_CTG_AVLBLTY)
    default_wc_avlblty = fields.Number(default=CtgConstants.DEFAULT_WC_AVLBLTY)
    default_pag_avlblty = fields.Number(default=CtgConstants.DEFAULT_PAG_AVLBLTY)
    max_pag_avlblty = fields.Number(default=CtgConstants.MAX_PAG_AVLBLTY)
    default_pf_avlblty = fields.Number(default=CtgConstants.DEFAULT_PF_AVLBLTY)
    max_pf_avlblty = fields.Number(default=CtgConstants.MAX_PF_AVLBLTY)
    has_duct_burner = fields.Boolean()
    can_pag = fields.Boolean()
    can_wc = fields.Boolean()
    can_peak_fire = fields.Boolean()
    min_db_fuel_avlblty = fields.Number(default=0)
    max_db_fuel_avlblty = fields.Number(default=100)
    default1x1 = fields.Boolean()

    @classmethod
    def get_ctg_name(cls, obj: Train):
        return obj.ctg.name
