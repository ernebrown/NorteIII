import os

import joblib

from cctwin.assets.block.block import Block
from cctwin.assets.condenser.condenser import Condenser, CondenserCoolingType
from cctwin.assets.ctg.ctg import GasTurbine
from cctwin.assets.ctg.ctg_constants import CtgConstants
from cctwin.assets.hrsg.hrsg import Hrsg
from cctwin.assets.inletconditioner.inlet_conditioner import (InletConditioner, InletConditionerType)
from cctwin.assets.stg.stg import SteamTurbine
from cctwin.assets.train.train import Train
from cctwin.assets.ctg.ctg_incrementals import PagIncremental, PeakFireIncremental, WCIncremental

__dir_name = os.path.dirname(__file__)
__model_factory_directory = os.path.join(__dir_name, 'model_factory')

notebooks = []

for root, dirs, files in os.walk(__model_factory_directory):
    for file in files:
        if file.endswith("model_build.ipynb"):
            notebooks.append(os.path.join(root, file))


def inlet_conditioner() -> InletConditioner:
    pickle_file_name = os.path.join(__dir_name, 'pickles/chiller.pkl')
    model_dict = joblib.load(pickle_file_name)
    inlet_conditioner = InletConditioner(InletConditionerType.CHILLERS, model_dict)
    return inlet_conditioner


def ctg3() -> GasTurbine:
    pickle_file_name = os.path.join(__dir_name, 'pickles/ctg3.pkl')
    model_dict = joblib.load(pickle_file_name)
    base_load_threshold = CtgConstants.MIN_BASE_LOAD_THRESHOLD
    default1x1 = True
    pag_incremental = None
    peak_incremental = None
    wc_incremental = None
    ctg = GasTurbine('CTG-3', inlet_conditioner=inlet_conditioner(), model_dict=model_dict,
                     shaft_limit=205, fuel_limit=5000, exh_limit=1200,  default1x1= default1x1, base_load_threshold=base_load_threshold,
                     pag_incremental=pag_incremental, peak_incremental=peak_incremental, wc_incremental=wc_incremental)
    return ctg


def ctg4() -> GasTurbine:
    pickle_file_name = os.path.join(__dir_name, 'pickles/ctg4.pkl')
    model_dict = joblib.load(pickle_file_name)
    base_load_threshold = CtgConstants.MIN_BASE_LOAD_THRESHOLD
    default1x1 = False
    pag_incremental = None
    peak_incremental = None
    wc_incremental = None
    ctg = GasTurbine('CTG-4', inlet_conditioner=inlet_conditioner(), model_dict=model_dict,
                     shaft_limit=205, fuel_limit=5000,exh_limit=1200,  default1x1= default1x1, base_load_threshold=base_load_threshold,
                     pag_incremental=pag_incremental, peak_incremental=peak_incremental, wc_incremental=wc_incremental)
    return ctg


def hrsg3() -> Hrsg:
    pickle_file_name = os.path.join(__dir_name, 'pickles/hrsg3.pkl')
    model_dict = joblib.load(pickle_file_name)
    has_duct_burner = True
    hrsg = Hrsg('HRSG-3', has_duct_burner=has_duct_burner, model_dict=model_dict)
    return hrsg


def hrsg4() -> Hrsg:
    pickle_file_name = os.path.join(__dir_name, 'pickles/hrsg4.pkl')
    model_dict = joblib.load(pickle_file_name)
    has_duct_burner = True
    hrsg = Hrsg('HRSG-4', has_duct_burner=has_duct_burner, model_dict=model_dict)
    return hrsg


def stg() -> SteamTurbine:
    pickle_file_name = os.path.join(__dir_name, 'pickles/condenser.pkl')
    model_dict = joblib.load(pickle_file_name)
    condenser = Condenser(CondenserCoolingType.WATER_BODY, model_dict)

    pickle_file_name = os.path.join(__dir_name, 'pickles/stg.pkl')
    model_dict = joblib.load(pickle_file_name)
    stg = SteamTurbine(name='STG-1', condenser=condenser, back_press_limit=2, shaft_limit=345, model_dict=model_dict)
    return stg


def __block() -> Block:
    train3 = Train(ctg=ctg3(), hrsg=hrsg3())
    train4 = Train(ctg=ctg4(), hrsg=hrsg4())
    LSL1x1 = 134
    LSL2x1 = 250
    LSLMODE = False
    pickle_file_name = os.path.join(__dir_name, 'pickles/auxload.pkl')
    aux_load_model_dict = joblib.load(pickle_file_name)
    block = Block(name='BDEC', trains=[train3, train4], stg=stg(), aux_load_model_dict=aux_load_model_dict,
                  config_mode=['1x1A', '1x1B', '2x1'], config_type=['Min', 'AGC_Base', 'Base_DB', 'Base_DB_Cool'],
                  LSLMODE=LSLMODE, LSL1x1=LSL1x1, LSL2x1=LSL2x1)
    return block


block_twin = __block()
