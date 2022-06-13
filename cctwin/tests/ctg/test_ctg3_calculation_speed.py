import time

import numpy as np

from cctwin.assets.ctg.ctg_input import CtgInput
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode


def test_speed_baseload_calculations(ctg8):
    cit = list(np.arange(-20, 120, 1))
    baro = [14.7] * len(cit)
    site_config = '2X1'
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.BASELOAD.value,
                         site_config=site_config,
                         ctg_avlblty=100,
                         pag_avlblty=0,
                         is_peak_fire_on=False,
                         cit=cit,
                         baro=baro)

    start_time = time.time()
    performance = ctg8.get_performance(ctg_input=ctg_input)
    end_time = time.time()
    duration_in_seconds = end_time - start_time

    print(
        f'\n\nTime taken: {duration_in_seconds:0.2f} secs '
        f'to run {len(cit)} cases of {ctg_input.ctg_operation_mode}-Load operation of {ctg8.name}')

    assert len(performance.mw) == len(cit)
    assert duration_in_seconds <= 0.5


def test_speed_2x1_minload_calculations(ctg8):
    cit = list(np.arange(-20, 120, 1))
    baro = [14.7] * len(cit)
    site_config = '2X1'
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.MINLOAD.value,
                         site_config=site_config,
                         ctg_avlblty=100,
                         pag_avlblty=0,
                         is_peak_fire_on=False,
                         cit=cit,
                         baro=baro)

    start_time = time.time()
    performance = ctg8.get_performance(ctg_input=ctg_input)
    end_time = time.time()
    duration_in_seconds = end_time - start_time

    print(
        f'\n\nTime taken: {duration_in_seconds:0.2f} secs '
        f'to run {len(cit)} cases of {ctg_input.ctg_operation_mode}-Load operation of {ctg8.name}')

    assert len(performance.mw) == len(cit)
    assert duration_in_seconds <= 0.5


def test_speed_1x1_minload_calculations(ctg8):
    cit = list(np.arange(-20, 120, 1))
    baro = [14.7] * len(cit)
    site_config = '1X1'
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.MINLOAD.value,
                         site_config=site_config,
                         ctg_avlblty=100,
                         pag_avlblty=0,
                         is_peak_fire_on=False,
                         cit=cit,
                         baro=baro)

    start_time = time.time()
    performance = ctg8.get_performance(ctg_input=ctg_input)
    end_time = time.time()
    duration_in_seconds = end_time - start_time

    print(
        f'\n\nTime taken: {duration_in_seconds:0.2f} secs '
        f'to run {len(cit)} cases of {ctg_input.ctg_operation_mode}-Load operation of {ctg8.name}')

    assert len(performance.mw) == len(cit)
    assert duration_in_seconds <= 0.5


def test_speed_70_percent_partload_calculations(ctg8):
    cit = list(np.arange(-20, 120, 1))
    baro = [14.7] * len(cit)
    site_config = '2X1'
    ctg_avlblty = 70
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.BASELOAD.value,
                         site_config=site_config,
                         ctg_avlblty=ctg_avlblty,
                         pag_avlblty=0,
                         is_peak_fire_on=False,
                         cit=cit,
                         baro=baro)

    start_time = time.time()
    performance = ctg8.get_performance(ctg_input=ctg_input)
    end_time = time.time()
    duration_in_seconds = end_time - start_time

    print(
        f'\n\nTime taken: {duration_in_seconds:0.2f} secs '
        f'to run {len(cit)} cases of {ctg_input.ctg_operation_mode}-Load operation of {ctg8.name}')

    assert len(performance.mw) == len(cit)
    assert duration_in_seconds <= 0.5
