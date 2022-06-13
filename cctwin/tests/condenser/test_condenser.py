import pytest

from cctwin.assets.condenser.condenser_input import AmbientConditions, CondenserInput

# List of tuples ('db', 'rh', 'baro', 'expected_circ_water_temp', 'tolerance')
test_data_list = [
    (10, 0.6, 14.7, 10, 12),
    (20, 0.6, 14.7, 20, 10),
    (30, 0.6, 14.7, 30, 10),
    (40, 0.6, 14.7, 40, 10),
    (50, 0.6, 14.7, 50, 10),
    (60, 0.6, 14.7, 60, 10),
    (70, 0.6, 14.7, 70, 10),
    (80, 0.6, 14.7, 80, 10),
    (90, 0.6, 14.7, 80, 10),
    (100, 0.6, 14.7, 90, 10),
]


def id_function(data):
    db, rh, baro, exp_circ_water_temp, tol = data
    return f'db:{db:0.2f}, rh:{rh * 100: 0.2f}, tolerance: {tol}'


@pytest.fixture(params=test_data_list, ids=id_function)
def condenser_test_data(request):
    return request.param


def test_condenser_performance_for(condenser, condenser_test_data):
    db, rh, baro, exp_circ_water_temp, tol = condenser_test_data
    ambient_conditions = AmbientConditions(db=db, rh=rh, baro=baro)
    condenser_input = CondenserInput(ambient_conditions=ambient_conditions)
    performance = condenser.get_performance(condenser_input=condenser_input)
    circ_water_temp = performance[0]
    assert circ_water_temp == pytest.approx(exp_circ_water_temp, abs=tol)
