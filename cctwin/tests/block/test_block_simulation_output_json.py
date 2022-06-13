from marshmallow import ValidationError, pprint

from cctwin.assets.block.block_output import BlockSimulationOutputSchema
from cctwin.assets.block.block_request import BlockSimulationRequest, BlockSimulationRequestSchema
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.hrsg.duct_burner_mode import DuctBurnerMode
from cctwin.assets.hrsg.hrsg_constants import HrsgConstants


def test_1x1_to_json(block):
    db = 90
    rh = 60
    baro = 14.67

    ctg8_name = block.trains[0].ctg.name
    ctg8_ctg_mode = CtgOperationMode.OFFLINE
    ctg8_ctg_availability = 100
    ctg8_is_inlet_conditioner_on = True
    ctg8_inlet_conditioner_availability = 100
    ctg8_duct_burner_mode = DuctBurnerMode.OFF
    ctg8_duct_burner_fuel = HrsgConstants.MAX_FUEL
    ctg8_is_pag_on = False
    ctg8_pag_availability = 100
    ctg8_is_peak_fire_on = False

    ctg9_name = block.trains[1].ctg.name
    ctg9_ctg_mode = CtgOperationMode.BASELOAD
    ctg9_ctg_availability = 100
    ctg9_is_inlet_conditioner_on = True
    ctg9_inlet_conditioner_availability = 100
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
        schema = BlockSimulationOutputSchema()

        output_json_dict = schema.dump(block_output)
        assert isinstance(output_json_dict, dict)
        pprint(output_json_dict, indent=4)
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        assert len(err.messages) == 0


def test_2x1_to_json(block):
    db = 90
    rh = 85
    baro = 14.71

    ctg8_name = block.trains[0].ctg.name
    ctg8_ctg_mode = CtgOperationMode.BASELOAD
    ctg8_ctg_availability = 100
    ctg8_is_inlet_conditioner_on = False
    ctg8_inlet_conditioner_availability = 10
    ctg8_duct_burner_mode = DuctBurnerMode.OFF
    ctg8_duct_burner_fuel = HrsgConstants.MAX_FUEL
    ctg8_is_pag_on = False
    ctg8_pag_availability = 100
    ctg8_is_peak_fire_on = False

    ctg9_name = block.trains[1].ctg.name
    ctg9_ctg_mode = CtgOperationMode.BASELOAD
    ctg9_ctg_availability = 100
    ctg9_is_inlet_conditioner_on = True
    ctg9_inlet_conditioner_availability = 90
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

    pprint(request_json_dict, indent=4)

    try:
        schema = BlockSimulationRequestSchema()
        block_request = schema.load(request_json_dict)

        assert isinstance(block_request, BlockSimulationRequest)

        block_output = block.get_performance(block_simulation_request=block_request)
        schema = BlockSimulationOutputSchema()
        output_json_dict = schema.dump(block_output)

        assert isinstance(output_json_dict, dict)
        pprint(output_json_dict, indent=4)
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        assert len(err.messages) == 0
