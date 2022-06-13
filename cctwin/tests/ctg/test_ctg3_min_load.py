import numpy as np
import pytest

from cctwin.assets.ctg.ctg_input import CtgInput
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode

# List of tuples ('site_config', 'input_cit', 'input_baro', 'expected_mw', 'expected_fuel', 'tol_mw', 'tol_fuel')
test_data_list = [
    ('2X1', 110.5367778, 14.7, 70.01300815, 1009.361457, 4, 75),
    ('2X1', 91.58094387, 14.7, 70.92007422, 1034.135138, 4, 75),
    ('2X1', 66.60246840, 14.7, 70.97103709, 1034.408572, 5, 75),
    ('1X1', 105.2814578, 14.7, 90.00268704, 1166.962032, 4, 75),
    ('1X1', 88.20936915, 14.7, 87.11959586, 1152.816511, 4, 75),
    ('1X1', 81.84717499, 14.7, 87.26967322, 1181.251886, 4, 75)
]


def id_function(data):
    site_config, cit, baro, expected_mw, expected_fuel, tol_mw, tol_fuel = data
    return f'config:{site_config}, cit:{cit:0.2f}, baro:{baro:0.2f}, tolerance_mw: {tol_mw}, tolerance_fuel: {tol_fuel}'


@pytest.fixture(params=test_data_list, ids=id_function)
def ctg8_min_load_test_data(request):
    return request.param


def test_min_load_performance_for(ctg8, ctg8_min_load_test_data):
    site_config, cit, baro, expected_mw, expected_fuel, tol_mw, tol_fuel = ctg8_min_load_test_data
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.MINLOAD.value,
                         site_config=site_config,
                         ctg_avlblty=100,
                         pag_avlblty=0,
                         is_peak_fire_on=False,
                         cit=cit,
                         baro=baro)
    performance = ctg8.get_performance(ctg_input=ctg_input)
    mw = performance.mw[0]
    fuel = performance.fuel[0]
    assert mw == pytest.approx(expected_mw, abs=tol_mw)
    assert fuel == pytest.approx(expected_fuel, abs=tol_fuel)


def test_min_load_performance_single_case(ctg8):
    cit = 110.54
    baro = 14.7
    expected_mw = 70.01
    expected_fuel = 1009.36
    tol_mw = 4
    tol_fuel = 75
    site_config = '2X1'
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.MINLOAD.value,
                         site_config=site_config,
                         ctg_avlblty=100,
                         pag_avlblty=0,
                         is_peak_fire_on=False,
                         cit=cit,
                         baro=baro)
    performance = ctg8.get_performance(ctg_input=ctg_input)
    mw = performance.mw[0]
    fuel = performance.fuel[0]
    print(f'\n\nMW Tolerance: {tol_mw}\nFUEL Tolerance: {tol_fuel}\n')
    print(performance.to_json())
    assert mw == pytest.approx(expected_mw, abs=tol_mw)
    assert fuel == pytest.approx(expected_fuel, abs=tol_fuel)


def test_2x1_minload_trends(ctg8):
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

    performance = ctg8.get_performance(ctg_input=ctg_input)
    heat_rate = np.divide(performance.fuel, performance.mw)
    mw_diffs = np.diff(performance.mw)
    hr_diffs = np.diff(heat_rate)

    print('\n\n')
    for temp, mw, mw_diff, hr, hr_diff in zip(cit, performance.mw, mw_diffs, heat_rate, hr_diffs):
        print(f'CIT: {temp}\tMW: {mw}\tMW_DIFF: {mw_diff}\tHeat_Rate: {hr}\tHR_DIFF: {hr_diff}')
    assert len(performance.mw) == len(cit)
    assert np.all(mw_diffs <= 0)
    assert np.all(hr_diffs >= 0)


def test_1x1_minload_trends(ctg8):
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

    performance = ctg8.get_performance(ctg_input=ctg_input)
    heat_rate = np.divide(performance.fuel, performance.mw)
    mw_diffs = np.diff(performance.mw)
    hr_diffs = np.diff(heat_rate)

    print('\n\n')
    for temp, mw, mw_diff, hr, hr_diff in zip(cit, performance.mw, mw_diffs, heat_rate, hr_diffs):
        print(f'CIT: {temp}\tMW: {mw}\tMW_DIFF: {mw_diff}\tHeat_Rate: {hr}\tHR_DIFF: {hr_diff}')
    assert len(performance.mw) == len(cit)
    assert np.all(mw_diffs <= 0)
    assert np.all(hr_diffs >= 0)
