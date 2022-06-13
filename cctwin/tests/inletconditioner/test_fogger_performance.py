import time

from cctwin.assets.inletconditioner.inlet_conditioner_input import InletConditionerInput


def test_speed_of_fogger_performance_calculation(fake_fogger):
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
    performance = fake_fogger.get_performance(inlet_conditioner_input)
    end_time = time.time()
    duration_in_seconds = end_time - start_time
    print(f'\n\nTime taken: {duration_in_seconds:0.2f} secs')
    assert len(performance.cit) == num_of_cases
    assert duration_in_seconds <= 1
