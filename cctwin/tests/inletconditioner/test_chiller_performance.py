import time

import pytest

from cctwin.assets.inletconditioner.inlet_conditioner import (InletConditionerType)
from cctwin.assets.inletconditioner.inlet_conditioner_constants import InletConditionerConstants
from cctwin.assets.inletconditioner.inlet_conditioner_input import InletConditionerInput
from cctwin.helper.asset_model_executor import ModelExecutor


def test_chiller_constructor(chiller):
    assert chiller.conditioning_system == InletConditionerType.CHILLERS
    assert isinstance(chiller.model_executor, ModelExecutor)


# List of tuples ('avlblty', 'db', 'rh', 'baro', 'expected_cit', 'tol_cit')
test_data_list = [
    (InletConditionerConstants.MAX_AVLBLTY, 71.85271029, 0.978204601, 14.7, 47.74232409, 3),
    (InletConditionerConstants.MAX_AVLBLTY, 82.34259474, 0.732808140, 14.7, 53.32113380, 4),
    (InletConditionerConstants.MAX_AVLBLTY, 90.95913392, 0.495175521, 14.7, 51.97406667, 3),
    (InletConditionerConstants.MAX_AVLBLTY, 74.58180760, 0.963120506, 14.7, 47.58056431, 3),
    (InletConditionerConstants.MAX_AVLBLTY, 69.99763938, 0.575587758, 14.7, 48.89870314, 3),
    (InletConditionerConstants.MAX_AVLBLTY, 90.66131304, 0.749694610, 14.7, 52.77427675, 10),
    (InletConditionerConstants.MAX_AVLBLTY, 83.74779360, 0.798510967, 14.7, 48.74270746, 6),
]


def id_function(data):
    avlblty, db, rh, baro, expected_cit, tol_cit = data
    return f'avlblty:{avlblty}, db:{db:0.2f}, rh:{rh * 100:0.2f}, baro:{baro:0.2f}, tolerance_cit: {tol_cit}'


@pytest.fixture(params=test_data_list, ids=id_function)
def chiller_test_data(request):
    return request.param


def test_chiller_performance_at_given_conditions(chiller, chiller_test_data):
    avlblty, db, rh, baro, expected_cit, tol_cit = chiller_test_data
    inlet_conditioner_input = InletConditionerInput(avlblty=avlblty,
                                                    db=db,
                                                    rh=rh,
                                                    baro=baro)

    performance = chiller.get_performance(inlet_conditioner_input)
    cit = performance.cit[0]
    assert cit == pytest.approx(expected_cit, abs=tol_cit)


def test_chiller_performance_single_case(chiller):
    avlblty = InletConditionerConstants.MAX_AVLBLTY
    db = 95
    rh = 52 / 100
    baro = 14.7
    expected_cit = 50
    tol_cit = 6
    inlet_conditioner_input = InletConditionerInput(avlblty=avlblty,
                                                    db=db,
                                                    rh=rh,
                                                    baro=baro)

    performance = chiller.get_performance(inlet_conditioner_input)
    cit = performance.cit[0]
    print(f'\nCIT Tolerance: {tol_cit}\n')
    assert cit == pytest.approx(expected_cit, abs=tol_cit)


def test_speed_of_chiller_performance_calculation(chiller):
    num_of_cases = 5
    avlblty = 100
    db = [95] * num_of_cases
    rh = [0.52] * num_of_cases
    baro = [14.7] * num_of_cases
    inlet_conditioner_input = InletConditionerInput(avlblty=avlblty,
                                                    db=db,
                                                    rh=rh,
                                                    baro=baro)

    start_time = time.time()
    performance = chiller.get_performance(inlet_conditioner_input)
    end_time = time.time()
    duration_in_seconds = end_time - start_time
    print(f'\n\nTime taken: {duration_in_seconds:0.2f} secs')
    assert len(performance.cit) == num_of_cases
    assert duration_in_seconds <= 1


def test_chiller_performance_when_turned_off(chiller):
    avlblty = 100
    db = 59.95
    rh = 52 / 100
    baro = 14.7
    inlet_conditioner_input = InletConditionerInput(avlblty=avlblty,
                                                    db=db,
                                                    rh=rh,
                                                    baro=baro)

    performance = chiller.get_performance(inlet_conditioner_input)
    assert performance.cit[0] == db


def test_chiller_performance_below_min_dry_bulb_temp_single_input(chiller):
    avlblty = 100
    db = 59.95
    rh = 52 / 100
    baro = 14.7
    inlet_conditioner_input = InletConditionerInput(avlblty=avlblty,
                                                    db=db,
                                                    rh=rh,
                                                    baro=baro)

    performance = chiller.get_performance(inlet_conditioner_input)
    assert performance.cit[0] == db


def test_chiller_performance_below_min_dry_bulb_temp_multiple_inputs(chiller):
    avlblty = 4000
    db = [91, 60.01, 59.99, 58]
    rh = [0.52] * len(db)
    baro = [14.7] * len(db)
    inlet_conditioner_input = InletConditionerInput(avlblty=avlblty,
                                                    db=db,
                                                    rh=rh,
                                                    baro=baro)

    performance = chiller.get_performance(inlet_conditioner_input)
    assert performance.cit[0] == pytest.approx(50, 0.5)
    assert performance.cit[1] == pytest.approx(db[1], 0.5)
    assert performance.cit[2] == pytest.approx(db[2], 0.5)
    assert performance.cit[3] == pytest.approx(db[3], 0.5)
