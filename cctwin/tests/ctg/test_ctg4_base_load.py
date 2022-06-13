import numpy as np
import pytest

from cctwin.assets.ctg.ctg_input import CtgInput
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode

# List of tuples ('site_config', 'input_cit', 'input_baro', 'expected_mw', 'expected_fuel', 'tol_mw', 'tol_fuel')
test_data_list = [
    ('2X1', 94.62954541, 14.7, 151.3828486, 1658.676745, 3, 50),
    ('2X1', 81.42273036, 14.7, 160.1567999, 1679.877437, 2, 50),
    ('2X1', 71.08907575, 14.7, 168.9314025, 1758.583224, 2, 50),
    ('2X1', 46.68961932, 14.7, 179.5427873, 1846.864386, 2, 50),
    ('2X1', 91.26118980, 14.7, 152.1240098, 1649.022902, 5, 50),
    ('2X1', 52.76780905, 14.7, 178.3854398, 1834.465666, 2, 50),
    ('2X1', 31.03591828, 14.7, 190.8271347, 1941.580979, 2, 50),
    ('2X1', 53.50377888, 14.7, 175.4283411, 1830.709567, 2, 50),
    ('2X1', 51.71191004, 14.7, 176.2970708, 1838.622459, 4, 50),
    ('2X1', 46.43896729, 14.7, 179.3535419, 1854.287126, 2, 50),
    ('1X1', 86.35046401, 14.7, 157.0422530, 1666.951547, 2, 50),
    ('1X1', 85.62939439, 14.7, 157.8563995, 1699.022421, 2, 50),
    ('1X1', 79.59702463, 14.7, 160.1071228, 1706.354598, 4, 50),
    ('1X1', 48.74270746, 14.7, 175.5042017, 1815.332017, 4, 50)
]


def id_function(data):
    site_config, cit, baro, expected_mw, expected_fuel, tol_mw, tol_fuel = data
    return f'config:{site_config}, cit:{cit:0.2f}, baro:{baro:0.2f}, tolerance_mw: {tol_mw}, tolerance_fuel: {tol_fuel}'


@pytest.fixture(params=test_data_list, ids=id_function)
def ctg9_base_load_test_data(request):
    return request.param


def test_base_load_performance_for(ctg9, ctg9_base_load_test_data):
    site_config, cit, baro, expected_mw, expected_fuel, tol_mw, tol_fuel = ctg9_base_load_test_data
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.BASELOAD.value,
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


def test_base_load_performance_single_case(ctg9):
    cit = 94.6
    baro = 14.7
    expected_mw = 151.4
    expected_fuel = 1658.7
    tol_mw = 3
    tol_fuel = 50
    site_config = '2X1'
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.BASELOAD.value,
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


def test_baseload_trends(ctg9):
    cit = list(np.arange(-20, 120, 1, ))
    baro = [14.7] * len(cit)
    site_config = '2X1'
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.BASELOAD.value,
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
