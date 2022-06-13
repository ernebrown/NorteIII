import pytest

from cctwin.assets.ctg.ctg_input import CtgInput
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode

# List of tuples ('site_config', 'input_cit', 'input_baro', 'load_percent', 'tolerance')
test_data_list = [
    ('2x1', 10, 14.7, 70, 6),
    ('2x1', 20, 14.7, 70, 4),
    ('2x1', 30, 14.7, 70, 1),
    ('2x1', 40, 14.7, 70, 2),
    ('2x1', 50, 14.7, 70, 4),
    ('2x1', 60, 14.7, 70, 6),
    ('2x1', 70, 14.7, 70, 9),
    ('2x1', 80, 14.7, 70, 11),
    ('2x1', 90, 14.7, 70, 14),
    ('2x1', 100, 14.7, 70, 17)
]


def id_function(data):
    site_config, cit, baro, load_percent, tol = data
    return f'site_config:{site_config}, cit:{cit:0.2f}, baro:{baro:0.2f}, ' \
           f'load_percent: {load_percent}, tolerance: {tol}'


@pytest.fixture(params=test_data_list, ids=id_function)
def ctg4_part_load_test_data(request):
    return request.param


def test_part_load_performance_for(ctg9, ctg9_part_load_test_data):
    site_config, cit, baro, load_percent, tol = ctg9_part_load_test_data
    ctg_input_part_load = CtgInput(ctg_operation_mode=CtgOperationMode.BASELOAD.value,
                                   site_config=site_config,
                                   ctg_avlblty=load_percent,
                                   pag_avlblty=0,
                                   is_peak_fire_on=False,
                                   cit=cit,
                                   baro=baro)
    ctg_input_base_load = CtgInput(ctg_operation_mode=CtgOperationMode.BASELOAD.value,
                                   site_config=site_config,
                                   ctg_avlblty=100,
                                   pag_avlblty=0,
                                   is_peak_fire_on=False,
                                   cit=cit,
                                   baro=baro)
    performance_part_load = ctg9.get_performance(ctg_input=ctg_input_part_load)
    performance_base_load = ctg9.get_performance(ctg_input=ctg_input_base_load)
    part_mw = performance_part_load.mw[0]
    base_mw = performance_base_load.mw[0]
    percent = part_mw / base_mw * 100
    assert percent == pytest.approx(load_percent, abs=tol)


def test_part_load_performance_single_case(ctg9):
    site_config = '2x1'
    cit = 50
    baro = 14.7
    load_percent = 70
    tol = 4
    ctg_input_part_load = CtgInput(ctg_operation_mode=CtgOperationMode.BASELOAD.value,
                                   site_config=site_config,
                                   ctg_avlblty=load_percent,
                                   pag_avlblty=0,
                                   is_peak_fire_on=False,
                                   cit=cit,
                                   baro=baro)
    ctg_input_base_load = CtgInput(ctg_operation_mode=CtgOperationMode.BASELOAD.value,
                                   site_config=site_config,
                                   ctg_avlblty=100,
                                   pag_avlblty=0,
                                   is_peak_fire_on=False,
                                   cit=cit,
                                   baro=baro)
    performance_part_load = ctg9.get_performance(ctg_input=ctg_input_part_load)
    performance_base_load = ctg9.get_performance(ctg_input=ctg_input_base_load)
    part_mw = performance_part_load.mw[0]
    base_mw = performance_base_load.mw[0]
    percent = part_mw / base_mw * 100
    print(
        f'\n\nExpected Load Percent: {load_percent / 100:.00%}\n'
        f'Actual Load Percent: {percent:.02f}%\nTolerance: {tol / 100:.00%}')
    print(performance_part_load.to_json())
    assert percent == pytest.approx(load_percent, abs=tol)
