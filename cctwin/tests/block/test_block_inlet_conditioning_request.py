import pytest
from marshmallow import ValidationError

from cctwin.assets.block.ambient_conditions import AmbientConditions
from cctwin.assets.block.block_request import BlockSimulationRequest, BlockSimulationRequestSchema
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.hrsg.duct_burner_mode import DuctBurnerMode
from cctwin.assets.hrsg.hrsg_constants import HrsgConstants
from cctwin.assets.inletconditioner.inlet_conditioner_constants import InletConditionerConstants

ton = InletConditionerConstants.TON_DEFAULT
# List of tuples (  AmbientConditions,
#                   is_inlet_conditioner_1_on, inlet_conditioner_1_availability, expected_cit, allowed_tolerance
#                   is_inlet_conditioner_2_on, inlet_conditioner_2_availability, expected_cit, allowed_tolerance)
test_data_list = [
    (AmbientConditions(90.00, 0.85, 14.7), True, 100 * ton / 100, 65.00, 2, True, 100 * ton / 100, 65.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), True, 90 * ton / 100, 67.5, 2, True, 90 * ton / 100, 67.5, 2),
    (AmbientConditions(90.00, 0.85, 14.7), True, 80 * ton / 100, 69.00, 2, True, 80 * ton / 100, 69.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), True, 70 * ton / 100, 71.00, 2, True, 70 * ton / 100, 71.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), True, 60 * ton / 100, 74.00, 2, True, 60 * ton / 100, 74.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), True, 50 * ton / 100, 76.00, 2, True, 50 * ton / 100, 76.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), True, 40 * ton / 100, 78.00, 2, True, 40 * ton / 100, 78.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), True, 30 * ton / 100, 81.00, 2, True, 30 * ton / 100, 81.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), True, 20 * ton / 100, 83.00, 2, True, 20 * ton / 100, 83.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), True, 10 * ton / 100, 85.00, 2, True, 10 * ton / 100, 85.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), True, 5 * ton / 100, 87.00, 2, True, 5 * ton / 100, 87.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), True, 1 * ton / 100, 89.00, 2, True, 1 * ton / 100, 89.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), True, 0 * ton / 100, 90.00, 2, True, 0 * ton / 100, 90.00, 2),

    (AmbientConditions(90.00, 0.85, 14.7), False, 100 * ton / 100, 90, 0.3, True, 100 * ton / 100, 65.00, 0.3),
    (AmbientConditions(90.00, 0.85, 14.7), False, 90 * ton / 100, 90, 0.5, True, 90 * ton / 100, 67.5, 2),
    (AmbientConditions(90.00, 0.85, 14.7), False, 80, 90, 0.5, True, 80 * ton / 100, 69.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), False, 70, 90, 0.5, True, 70 * ton / 100, 71.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), False, 60, 90, 0.5, True, 60 * ton / 100, 74.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), False, 50, 90, 0.5, True, 50 * ton / 100, 76.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), False, 40, 90, 0.5, True, 40 * ton / 100, 78.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), False, 30, 90, 0.5, True, 30 * ton / 100, 81.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), False, 20, 90, 0.5, True, 20 * ton / 100, 83.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), False, 10, 90, 0.5, True, 10 * ton / 100, 85.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), False, 5, 90, 0.2, True, 5 * ton / 100, 87.00, 2),
    (AmbientConditions(90.00, 0.85, 14.7), False, 2, 90, 0.2, True, 2 * ton / 100, 89.00, 2),

    (AmbientConditions(10.00, 0.60, 14.7), True, 100 * ton / 100, 10.00, 0.2, True, 100 * ton / 100, 10.00, 0.2),
    (AmbientConditions(59.99, 0.60, 14.7), True, 100 * ton / 100, 59.99, 0.2, True, 100 * ton / 100, 59.99, 0.2),
    (AmbientConditions(60.00, 0.60, 14.7), True, 100 * ton / 100, 50.00, 0.2, True, 100 * ton / 100, 50.00, 0.2),

    (AmbientConditions(90.00, 0.85, 14.7), False, 10, 90.00, 0.2, False, 10, 90.00, 0.2),
    (AmbientConditions(90.00, 0.85, 14.7), False, 10, 90.00, 0.2, False, 10, 90.00, 0.2),
    (AmbientConditions(90.00, 0.85, 14.7), False, 10, 90.00, 0.2, False, 10, 90.00, 0.2),

]


def id_function(data):
    ambient_conditions, \
    is_inlet_conditioner_1_on, inlet_conditioner_1_avlblty, expected_cit_1, tol_cit_1, \
    is_inlet_conditioner_2_on, inlet_conditioner_2_avlblty, expected_cit_2, tol_cit_2 = data
    return f'db:{ambient_conditions.db[0]:0.2f}, ' \
           f'rh:{ambient_conditions.rh[0] * 100:0.2f}, ' \
           f'baro:{ambient_conditions.baro[0]:0.2f}, ' \
           f'is_inlet_conditioner_1_on:{is_inlet_conditioner_1_on}, ' \
           f'inlet_conditioner_1_avlblty:{inlet_conditioner_1_avlblty}, ' \
           f'is_inlet_conditioner_2_on:{is_inlet_conditioner_2_on}, ' \
           f'inlet_conditioner_2_avlblty:{inlet_conditioner_2_avlblty}, ' \
           f'tolerance_cit_1: {tol_cit_1}, ' \
           f'tolerance_cit_2: {tol_cit_2}'


@pytest.fixture(params=test_data_list, ids=id_function)
def chiller_2x1_test_data(request):
    return request.param


def test_2x1_one_chiller_off(block, chiller_2x1_test_data):
    ambient_conditions, \
    is_inlet_conditioner_1_on, inlet_conditioner_1_avlblty, expected_cit_1, tol_cit_1, \
    is_inlet_conditioner_2_on, inlet_conditioner_2_avlblty, expected_cit_2, tol_cit_2 = chiller_2x1_test_data

    db = ambient_conditions.db
    rh = ambient_conditions.rh
    baro = ambient_conditions.baro

    ctg8_name = block.trains[0].ctg.name
    ctg8_ctg_mode = CtgOperationMode.BASELOAD
    ctg8_ctg_availability = 100
    ctg8_is_inlet_conditioner_on = is_inlet_conditioner_1_on
    ctg8_inlet_conditioner_availability = inlet_conditioner_1_avlblty
    ctg8_duct_burner_mode = DuctBurnerMode.OFF
    ctg8_duct_burner_fuel = HrsgConstants.MAX_FUEL
    ctg8_is_pag_on = False
    ctg8_pag_availability = 100
    ctg8_is_peak_fire_on = False

    ctg9_name = block.trains[1].ctg.name
    ctg9_ctg_mode = CtgOperationMode.BASELOAD
    ctg9_ctg_availability = 100
    ctg9_is_inlet_conditioner_on = is_inlet_conditioner_2_on
    ctg9_inlet_conditioner_availability = inlet_conditioner_2_avlblty
    ctg9_duct_burner_mode = DuctBurnerMode.OFF
    ctg9_duct_burner_fuel = HrsgConstants.MAX_FUEL
    ctg9_is_pag_on = False
    ctg9_pag_availability = 100
    ctg9_is_peak_fire_on = False

    is_stg_online = True

    request_json_dict = {
        'ambient_conditions':
            {
                'db': db,
                'rh': rh,
                'baro': baro
            },
        'trains': [
            {
                'ctg': ctg8_name,
                'ctg_mode': ctg8_ctg_mode.value,
                'ctg_availability': ctg8_ctg_availability,
                'is_inlet_conditioner_on': ctg8_is_inlet_conditioner_on,
                'inlet_conditioner_availability': ctg8_inlet_conditioner_availability,
                'duct_burner_mode': ctg8_duct_burner_mode.value,
                'duct_burner_fuel': ctg8_duct_burner_fuel,
                'is_pag_on': ctg8_is_pag_on,
                'pag_availability': ctg8_pag_availability,
                'is_peak_fire_on': ctg8_is_peak_fire_on
            },
            {
                'ctg': ctg9_name,
                'ctg_mode': ctg9_ctg_mode.value,
                'ctg_availability': ctg9_ctg_availability,
                'is_inlet_conditioner_on': ctg9_is_inlet_conditioner_on,
                'inlet_conditioner_availability': ctg9_inlet_conditioner_availability,
                'duct_burner_mode': ctg9_duct_burner_mode.value,
                'duct_burner_fuel': ctg9_duct_burner_fuel,
                'is_pag_on': ctg9_is_pag_on,
                'pag_availability': ctg9_pag_availability,
                'is_peak_fire_on': ctg9_is_peak_fire_on
            }],
        'is_stg_online': is_stg_online
    }

    print('\n\n')

    try:
        schema = BlockSimulationRequestSchema()
        block_request = schema.load(request_json_dict)

        assert isinstance(block_request, BlockSimulationRequest)

        block_output = block.get_performance(block_simulation_request=block_request)

        assert block_output.train_outputs[0].inlet_conditioner_output.cit[0] == pytest.approx(expected_cit_1,
                                                                                              abs=tol_cit_1)
        assert block_output.train_outputs[1].inlet_conditioner_output.cit[0] == pytest.approx(expected_cit_2,
                                                                                              abs=tol_cit_2)

    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        assert len(err.messages) == 0
