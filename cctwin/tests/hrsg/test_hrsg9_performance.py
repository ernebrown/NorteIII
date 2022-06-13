import pytest

from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.hrsg.hrsg_constants import HrsgConstants
from cctwin.assets.hrsg.hrsg_input import HrsgInput
from cctwin.helper.asset_model_executor import ModelExecutor


def test_hrsg9_constructor(hrsg9):
    assert isinstance(hrsg9.model_executor, ModelExecutor)


# List of tuples ('ctg_mw', 'ctg_exh_temp', 'db_fuel', 'expected_db_fuel', 'tol_db_fuel')
test_data_list = [
    (190.8, 1080.1, 529.0, 529.0, 10),
    (178.4, 1109.9, 592.5, 592.5, 10),
    (179.4, 1098.5, 611.2, 611.2, 10),
    (152.1, 1139.6, 624.3, 624.3, 10),
    # TODO: Following test cases need to be validated
    # (176.3, 1106.8, 697.0, 697.0, 10),
    # (175.4, 1107.7, 714.2, 714.2, 10)
]


def id_function(data):
    ctg_mw, ctg_exh_temp, db_fuel, expected_db_fuel, tol_db_fuel = data
    return f'ctg_mw:{ctg_mw:0.1f}, ctg_exh_temp:{ctg_exh_temp:0.0f}, ' \
           f'db_fuel_:{db_fuel:0.0f}, tolerance_db_fuel: {tol_db_fuel}'


@pytest.fixture(params=test_data_list, ids=id_function)
def hrsg9_test_data(request):
    return request.param


def test_hrsg9_performance_at_given_conditions(hrsg9, hrsg9_test_data):
    ctg_mw, ctg_exh_temp, db_fuel, expected_db_fuel, tol_db_fuel = hrsg9_test_data

    ctg_mode = CtgOperationMode.BASELOAD
    hrsg_input = HrsgInput(ctg_mode=ctg_mode,
                           ctg_mw=ctg_mw,
                           ctg_exh_temp=ctg_exh_temp,
                           db_fuel=db_fuel)

    performance = hrsg9.get_performance(hrsg_input)
    db_fuel = performance.duct_burner_fuel[0]
    hp_press = performance.hp_press[0]
    hp_sh_temp = performance.hp_sh_temp[0]
    assert hp_press <= HrsgConstants.HP_PRESS_LIMIT
    assert hp_sh_temp <= HrsgConstants.HP_SH_TEMP_LIMIT
    assert db_fuel == pytest.approx(expected_db_fuel, abs=tol_db_fuel)


def test_hrsg9_performance_single_case(hrsg9):
    ctg_mw = 150
    ctg_exh_temp = 1100
    db_fuel = 695

    ctg_mode = CtgOperationMode.BASELOAD
    hrsg_input = HrsgInput(ctg_mode=ctg_mode,
                           ctg_mw=ctg_mw,
                           ctg_exh_temp=ctg_exh_temp,
                           db_fuel=db_fuel)

    performance = hrsg9.get_performance(hrsg_input)
    db_fuel = performance.duct_burner_fuel[0]
    hp_press = performance.hp_press[0]
    hp_sh_temp = performance.hp_sh_temp[0]
    print(f'\n\n'
          f'Actual DB FUEL:{db_fuel}\n'
          f'MAX DB FUEL:{HrsgConstants.MAX_FUEL}\n\n')
    assert hp_press <= HrsgConstants.HP_PRESS_LIMIT
    assert hp_sh_temp <= HrsgConstants.HP_SH_TEMP_LIMIT
    assert db_fuel <= HrsgConstants.MAX_FUEL
