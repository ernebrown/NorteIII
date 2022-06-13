import numpy as np
import pytest

from cctwin.assets.ctg.ctg_input import CtgInput
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode

# List of tuples ('site_config', 'input_cit', 'input_baro', 'expected_mw', 'expected_fuel', 'tol_mw', 'tol_fuel')
test_data_list = [
    ('2x1', 94.49581337, 14.6, 152.4800916, 1643.813053, 3, 50),
    ('2x1', 81.89024203, 14.6, 161.6765461, 1672.438067, 2, 50),
    ('2x1', 74.07157331, 14.6, 168.6582701, 1752.452876, 3, 50),
    ('2x1', 48.79502885, 14.6, 180.0035215, 1840.374545, 2, 50),
    ('2x1', 93.11199056, 14.6, 151.7987836, 1639.250612, 4, 50),
    ('2x1', 53.62907386, 14.6, 180.0711081, 1836.058870, 3, 50),
    ('2x1', 31.10585602, 14.6, 193.4726502, 1949.975616, 4, 50),
    ('2x1', 53.13848871, 14.6, 177.5748142, 1830.189551, 2, 50),
    ('2x1', 52.23622329, 14.6, 178.2592568, 1841.552853, 2, 50),
    ('2x1', 48.72216133, 14.6, 179.8651330, 1845.818259, 2, 50),
    ('1x1', 88.57220283, 14.6, 156.4707614, 1664.068675, 2, 50),
    ('1x1', 78.49331161, 14.6, 163.6409277, 1724.710818, 2, 50),
    ('1x1', 48.89870314, 14.6, 179.7629589, 1819.706152, 2, 50),
    ('1x1', 84.03627957, 14.6, 158.9663192, 1686.990338, 2, 50),
    ('1x1', 71.64716518, 14.6, 167.1526173, 1747.957935, 2, 50),
    ('1x1', 48.79335260, 14.6, 180.5163598, 1883.822550, 2, 50),
    ('1x1', 52.77427675, 14.6, 177.9297753, 1812.905399, 2, 50)
]


def id_function(data):
    site_config, cit, baro, expected_mw, expected_fuel, tol_mw, tol_fuel = data
    return f'config:{site_config}, cit:{cit:0.2f}, baro:{baro:0.2f}, tolerance_mw: {tol_mw}, tolerance_fuel: {tol_fuel}'


@pytest.fixture(params=test_data_list, ids=id_function)
def ctg3_base_load_test_data(request):
    return request.param


def test_base_load_performance_for(ctg8, ctg8_base_load_test_data):
    site_config, cit, baro, expected_mw, expected_fuel, tol_mw, tol_fuel = ctg8_base_load_test_data
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.BASELOAD.value,
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


def test_base_load_performance_single_case(ctg8):
    cit = 94.5
    baro = 14.7
    expected_mw = 152.5
    expected_fuel = 1643.8
    tol_mw = 4
    tol_fuel = 500
    site_config = '2X1'
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.BASELOAD.value,
                         site_config=site_config,
                         ctg_avlblty=100,
                         pag_avlblty=0,
                         is_peak_fire_on=False,
                         cit=cit,
                         baro=baro)
    performance = ctg8.get_performance(ctg_input=ctg_input)
    mw = performance.mw[0]
    fuel = performance.fuel[0]
    print(f'\nMW Tolerance: {tol_mw}\nFUEL Tolerance: {tol_fuel}\n')
    print(performance.to_json())
    assert mw == pytest.approx(expected_mw, abs=tol_mw)
    assert fuel == pytest.approx(expected_fuel, abs=tol_fuel)


def test_baseload_trends(ctg8):
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

    performance = ctg8.get_performance(ctg_input=ctg_input)
    heat_rate = np.divide(performance.fuel, performance.mw)
    mw_diffs = np.diff(performance.mw)
    hr_diffs = np.diff(heat_rate)

    print('\n\n')
    for temp, mw, mw_diff, hr, hr_diff in zip(cit, performance.mw, mw_diffs, heat_rate, hr_diffs):
        print(f'CIT: {temp}\tMW: {mw}\tMW_DIFF: {mw_diff}\tHeat_Rate: {hr}\tHR_DIFF: {hr_diff}')

    print('\n\n')
    print('mw,fuel,exh_temp')
    for mw, fuel, exh_temp in zip(performance.mw, performance.fuel, performance.exh_temp):
        print(f'{mw},{fuel},{exh_temp}')

    assert len(performance.mw) == len(cit)
    assert np.all(mw_diffs <= 0)
    assert np.all(hr_diffs >= 0)

    print('\n\n')
    print('mw,fuel,exh_temp')
    for mw, fuel, exh_temp in zip(performance.mw, performance.fuel, performance.exh_temp):
        print(f'{mw},{fuel},{exh_temp}')
