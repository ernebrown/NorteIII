import os

import joblib
import pytest

from cctwin.app import create_app
from cctwin.assets.block.block import Block
from cctwin.assets.condenser.condenser import Condenser, CondenserCoolingType
from cctwin.assets.ctg.ctg import GasTurbine
from cctwin.assets.ctg.ctg_constants import CtgConstants
from cctwin.assets.hrsg.hrsg import Hrsg
from cctwin.assets.inletconditioner.inlet_conditioner import (InletConditioner, InletConditionerType)
from cctwin.assets.stg.stg import SteamTurbine
from cctwin.assets.train.train import Train


@pytest.yield_fixture(scope='session')
def app():
    """
    Setup the flask test app. This function gets executed only once at the beginning of all tests

    :return: Flask app
    """
    params = {
        'DEBUG': False,
        'TESTING': True
    }

    _app = create_app(settings_override=params)

    # Establish an application context before running the tests
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(app):
    """
    Setup an app client. This function gets executed for each test function.
    :param app: PyTest fixture which returns a flask app
    :return: Flask app client
    """

    yield app.test_client()


@pytest.fixture(scope='module')
def chiller() -> InletConditioner:
    dir_name = os.path.dirname(__file__)
    pickle_file_name = os.path.join(dir_name, '../pickles/chiller.pkl')
    model_dict = joblib.load(pickle_file_name)
    inlet_conditioner = InletConditioner(InletConditionerType.CHILLERS, model_dict)
    return inlet_conditioner


@pytest.fixture(scope='module')
def fake_fogger() -> InletConditioner:
    dir_name = os.path.dirname(__file__)
    pickle_file_name = os.path.join(dir_name, '../pickles/chiller.pkl')
    model_dict = joblib.load(pickle_file_name)
    inlet_conditioner = InletConditioner(InletConditionerType.FOGGERS, model_dict)
    return inlet_conditioner


@pytest.fixture(scope='module')
def ctg3(chiller) -> GasTurbine:
    dir_name = os.path.dirname(__file__)
    pickle_file_name = os.path.join(dir_name, '../pickles/ctg3.pkl')
    model_dict = joblib.load(pickle_file_name)
    base_load_threshold = CtgConstants.MIN_BASE_LOAD_THRESHOLD
    pag_incremental = None
    peak_incremental = None
    ctg = GasTurbine('CTG-3', inlet_conditioner=chiller, model_dict=model_dict,
                     shaft_limit=205, fuel_limit=5000, exh_limit=1200, base_load_threshold=base_load_threshold,
                     pag_incremental=pag_incremental, peak_incremental=peak_incremental)
    return ctg


@pytest.fixture(scope='module')
def ctg4(chiller) -> GasTurbine:
    dir_name = os.path.dirname(__file__)
    pickle_file_name = os.path.join(dir_name, '../pickles/ctg4.pkl')
    model_dict = joblib.load(pickle_file_name)
    base_load_threshold = CtgConstants.MIN_BASE_LOAD_THRESHOLD
    pag_incremental = None
    peak_incremental = None
    ctg = GasTurbine('CTG-4', inlet_conditioner=chiller, model_dict=model_dict,
                     shaft_limit=205, fuel_limit=5000, exh_limit=1200, base_load_threshold=base_load_threshold,
                     pag_incremental=pag_incremental, peak_incremental=peak_incremental)
    return ctg


@pytest.fixture(scope='module')
def hrsg3() -> Hrsg:
    dir_name = os.path.dirname(__file__)
    pickle_file_name = os.path.join(dir_name, '../pickles/hrsg3.pkl')
    model_dict = joblib.load(pickle_file_name)
    has_duct_burner = True
    hrsg = Hrsg('Hrsg-3', has_duct_burner=has_duct_burner, model_dict=model_dict)
    return hrsg


@pytest.fixture(scope='module')
def hrsg4() -> Hrsg:
    dir_name = os.path.dirname(__file__)
    pickle_file_name = os.path.join(dir_name, '../pickles/hrsg4.pkl')
    model_dict = joblib.load(pickle_file_name)
    has_duct_burner = True
    hrsg = Hrsg('Hrsg-4', has_duct_burner=has_duct_burner, model_dict=model_dict)
    return hrsg


@pytest.fixture(scope='module')
def condenser() -> Condenser:
    dir_name = os.path.dirname(__file__)
    pickle_file_name = os.path.join(dir_name, '../pickles/condenser.pkl')
    model_dict = joblib.load(pickle_file_name)
    condenser = Condenser(CondenserCoolingType.WATER_BODY, model_dict)
    return condenser


@pytest.fixture(scope='module')
def stg(condenser) -> SteamTurbine:
    dir_name = os.path.dirname(__file__)
    pickle_file_name = os.path.join(dir_name, '../pickles/stg.pkl')
    model_dict = joblib.load(pickle_file_name)
    stg = SteamTurbine(name='STG-1', condenser=condenser, back_press_limit=2, shaft_limit=350, model_dict=model_dict)
    return stg


@pytest.fixture(scope='module')
def block(ctg3, hrsg3, ctg4, hrsg4, stg) -> Block:
    train3 = Train(ctg=ctg3, hrsg=hrsg3)
    train4 = Train(ctg=ctg4, hrsg=hrsg4)
    dir_name = os.path.dirname(__file__)
    pickle_file_name = os.path.join(dir_name, '../pickles/auxload.pkl')
    aux_load_model_dict = joblib.load(pickle_file_name)
    block = Block(name='BDEC', trains=[train3, train4], stg=stg, aux_load_model_dict=aux_load_model_dict,
                  config_mode=['1x1A', '1x1B', '2x1'], config_type=['Min', 'Base', 'Base_DB', 'Base_DB_Cool'])
    return block
