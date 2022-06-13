import numpy as np
import pytest

from cctwin.assets.ctg.ctg_input import CtgInput
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode

# List of tuples ('site_config', 'input_cit', 'input_baro', 'expected_mw', 'expected_fuel', 'tol_mw', 'tol_fuel')
test_data_list = [
    ('2X1', 116.5886556, 14.7, 70.00208118, 1032.141438, 3, 75),
    ('2X1', 90.15237426, 14.7, 70.92091375, 1048.326635, 5, 75),
    ('2X1', 70.42830232, 14.7, 70.93132349, 1050.674107, 8, 75),
    ('1X1', 100.9791383, 14.7, 88.60413930, 1166.676694, 3, 75),
    ('1X1', 90.89444767, 14.7, 86.86247958, 1186.946416, 3, 75),
    ('1X1', 83.42841702, 14.7, 86.76074742, 1165.573269, 3, 75)
]


def id_function(data):
    site_config, cit, baro, expected_mw, expected_fuel, tol_mw, tol_fuel = data
    return f'config:{site_config}, cit:{cit:0.2f}, baro:{baro:0.2f}, tolerance_mw: {tol_mw}, tolerance_fuel: {tol_fuel}'


@pytest.fixture(params=test_data_list, ids=id_function)
def ctg4_min_load_test_data(request):
    return request.param


def test_min_load_performance_for(ctg9, ctg9_min_load_test_data):
    site_config, cit, baro, expected_mw, expected_fuel, tol_mw, tol_fuel = ctg9_min_load_test_data
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.MINLOAD.value,
                         site_config=site_config,
                         ctg_avlblty=100,
                         pag_avlblty=0,
                         is_peak_fire_on=False,
                         cit=cit,
                         baro=baro)
    performance = ctg9.get_performance(ctg_input=ctg_input)
    mw = performance.mw[0]
    fuel = performance.fuel[0]
    assert mw == pytest.approx(expected_mw, abs=tol_mw)
    assert fuel == pytest.approx(expected_fuel, abs=tol_fuel)


def test_min_load_performance_single_case(ctg9):
    cit = 116.59
    baro = 14.7
    expected_mw = 70.01
    expected_fuel = 1032.15
    tol_mw = 3
    tol_fuel = 75
    site_config = '2X1'
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.MINLOAD.value,
                         site_config=site_config,
                         ctg_avlblty=100,
                         pag_avlblty=0,
                         is_peak_fire_on=False,
                         cit=cit,
                         baro=baro)
    performance = ctg9.get_performance(ctg_input=ctg_input)
    mw = performance.mw[0]
    fuel = performance.fuel[0]
    print(f'\nMW Tolerance: {tol_mw}\nFUEL Tolerance: {tol_fuel}\n')
    print(performance.to_json())
    assert mw == pytest.approx(expected_mw, abs=tol_mw)
    assert fuel == pytest.approx(expected_fuel, abs=tol_fuel)


def test_2x1_minload_trends(ctg9):
    cit = list(np.arange(-20, 120, 1, ))
    baro = [14.7] * len(cit)
    site_config = '2X1'
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.MINLOAD.value,
                         site_config=site_config,
                         ctg_avlblty=100,
                         pag_avlblty=0,
                         is_peak_fire_on=False,
                         cit=cit,
                         baro=baro)

    performance = ctg9.get_performance(ctg_input=ctg_input)
    heat_rate = np.divide(performance.fuel, performance.mw)
    mw_diffs = np.diff(performance.mw)
    hr_diffs = np.diff(heat_rate)

    print('\n\n')
    for temp, mw, mw_diff, hr, hr_diff in zip(cit, performance.mw, mw_diffs, heat_rate, hr_diffs):
        print(f'CIT: {temp}\tMW: {mw}\tMW_DIFF: {mw_diff}\tHeat_Rate: {hr}\tHR_DIFF: {hr_diff}')
    assert len(performance.mw) == len(cit)
    assert np.all(mw_diffs <= 0)
    assert np.all(hr_diffs >= 0)


def test_1x1_minload_trends(ctg9):
    cit = list(np.arange(-20, 120, 1, ))
    baro = [14.7] * len(cit)
    site_config = '1X1'
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.MINLOAD.value,
                         site_config=site_config,
                         ctg_avlblty=100,
                         pag_avlblty=0,
                         is_peak_fire_on=False,
                         cit=cit,
                         baro=baro)

    performance = ctg9.get_performance(ctg_input=ctg_input)
    heat_rate = np.divide(performance.fuel, performance.mw)
    mw_diffs = np.diff(performance.mw)
    hr_diffs = np.diff(heat_rate)

    print('\n\n')
    for temp, mw, mw_diff, hr, hr_diff in zip(cit, performance.mw, mw_diffs, heat_rate, hr_diffs):
        print(f'CIT: {temp}\tMW: {mw}\tMW_DIFF: {mw_diff}\tHeat_Rate: {hr}\tHR_DIFF: {hr_diff}')
    assert len(performance.mw) == len(cit)
    assert np.all(mw_diffs <= 0)
    assert np.all(hr_diffs >= 0)
