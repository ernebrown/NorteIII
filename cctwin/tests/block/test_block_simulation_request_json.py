from marshmallow import ValidationError, pprint

from cctwin.assets.block.ambient_conditions import AmbientConditions
from cctwin.assets.block.block_request import BlockSimulationRequest, BlockSimulationRequestSchema
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.hrsg.duct_burner_mode import DuctBurnerMode
from cctwin.assets.hrsg.hrsg_constants import HrsgConstants
from cctwin.assets.inletconditioner.inlet_conditioner_constants import InletConditionerConstants
from cctwin.assets.train.train_request import TrainSimulationRequest


def test_from_json(ctg8, ctg9):
    db = 90
    rh = 60
    baro = 14.67

    ctg8_ctg_mode = CtgOperationMode.MINLOAD
    ctg8_ctg_availability = 100
    ctg8_is_inlet_conditioner_on = True
    ctg8_inlet_conditioner_availability = InletConditionerConstants.TON_DEFAULT
    ctg8_duct_burner_mode = DuctBurnerMode.MAX
    ctg8_duct_burner_fuel = HrsgConstants.MAX_FUEL
    ctg8_is_pag_on = False
    ctg8_pag_availability = 100
    ctg8_is_peak_fire_on = False

    ctg9_ctg_mode = CtgOperationMode.MINLOAD
    ctg9_ctg_availability = 100
    ctg9_is_inlet_conditioner_on = True
    ctg9_inlet_conditioner_availability = InletConditionerConstants.TON_DEFAULT
    ctg9_duct_burner_mode = DuctBurnerMode.MAX
    ctg9_duct_burner_fuel = HrsgConstants.MAX_FUEL
    ctg9_is_pag_on = False
    ctg9_pag_availability = 100
    ctg9_is_peak_fire_on = False

    is_stg_online = True

    json_dict = {
        'ambient_conditions':
            {
                'db': db,
                'rh': rh,
                'baro': baro
            },
        'trains': [
            {
                'ctg': ctg8.name,
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
                'ctg': ctg9.name,
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
        block_request = schema.load(json_dict)

        assert isinstance(block_request, BlockSimulationRequest)
        assert isinstance(block_request.ambient_conditions, AmbientConditions)
        assert isinstance(block_request.trains, list)
        assert all(isinstance(train, TrainSimulationRequest) for train in block_request.trains)

        assert block_request.ambient_conditions.db[0] == db
        assert block_request.ambient_conditions.rh[0] == rh / 100
        assert block_request.ambient_conditions.baro[0] == baro

        assert block_request.is_stg_online == is_stg_online

        assert block_request.trains[0].ctg == ctg8.name
        assert block_request.trains[0].ctg_mode == ctg8_ctg_mode.value
        assert block_request.trains[0].ctg_availability == ctg8_ctg_availability
        assert block_request.trains[0].is_inlet_conditioner_on == ctg8_is_inlet_conditioner_on
        assert block_request.trains[0].inlet_conditioner_availability == ctg8_inlet_conditioner_availability
        assert block_request.trains[0].duct_burner_mode == ctg8_duct_burner_mode.value
        assert block_request.trains[0].is_pag_on == ctg8_is_pag_on
        assert block_request.trains[0].pag_availability == ctg8_pag_availability
        assert block_request.trains[0].is_peak_fire_on == ctg8_is_peak_fire_on

        assert block_request.trains[1].ctg == ctg9.name
        assert block_request.trains[1].ctg_mode == ctg9_ctg_mode.value
        assert block_request.trains[1].ctg_availability == ctg9_ctg_availability
        assert block_request.trains[1].is_inlet_conditioner_on == ctg9_is_inlet_conditioner_on
        assert block_request.trains[1].inlet_conditioner_availability == ctg9_inlet_conditioner_availability
        assert block_request.trains[1].duct_burner_mode == ctg9_duct_burner_mode.value
        assert block_request.trains[1].is_pag_on == ctg9_is_pag_on
        assert block_request.trains[1].pag_availability == ctg9_pag_availability
        assert block_request.trains[1].is_peak_fire_on == ctg9_is_peak_fire_on

    except ValidationError as err:
        assert print(err.valid_data)
        assert len(err.messages) == 0


def test_to_json(block):
    db = 90
    rh = 60 / 100
    baro = 14.67
    ambient_conditions = AmbientConditions(db=db, rh=rh, baro=baro)

    ctg8_ctg_mode = CtgOperationMode.MINLOAD
    ctg8_ctg_availability = 100
    ctg8_is_inlet_conditioner_on = True
    ctg8_inlet_conditioner_availability = InletConditionerConstants.TON_DEFAULT
    ctg8_duct_burner_mode = DuctBurnerMode.MAX
    ctg8_duct_burner_fuel = HrsgConstants.MAX_FUEL
    ctg8_is_pag_on = False
    ctg8_pag_availability = 100
    ctg8_is_peak_fire_on = False

    ctg9_ctg_mode = CtgOperationMode.MINLOAD
    ctg9_ctg_availability = 100
    ctg9_is_inlet_conditioner_on = True
    ctg9_inlet_conditioner_availability = InletConditionerConstants.TON_DEFAULT
    ctg9_duct_burner_mode = DuctBurnerMode.MAX
    ctg9_duct_burner_fuel = HrsgConstants.MAX_FUEL
    ctg9_is_pag_on = False
    ctg9_pag_availability = 100
    ctg9_is_peak_fire_on = False

    train_8_request = TrainSimulationRequest(ctg=block.trains[0].ctg.name,
                                             ctg_mode=ctg8_ctg_mode,
                                             ctg_availability=ctg8_ctg_availability,
                                             is_inlet_conditioner_on=ctg8_is_inlet_conditioner_on,
                                             inlet_conditioner_availability=ctg8_inlet_conditioner_availability,
                                             duct_burner_mode=ctg8_duct_burner_mode,
                                             duct_burner_fuel=ctg8_duct_burner_fuel,
                                             is_pag_on=ctg8_is_pag_on,
                                             pag_availability=ctg8_pag_availability,
                                             is_peak_fire_on=ctg8_is_peak_fire_on
                                             )

    train_9_request = TrainSimulationRequest(ctg=block.trains[1].ctg.name,
                                             ctg_mode=ctg9_ctg_mode,
                                             ctg_availability=ctg9_ctg_availability,
                                             is_inlet_conditioner_on=ctg9_is_inlet_conditioner_on,
                                             inlet_conditioner_availability=ctg9_inlet_conditioner_availability,
                                             duct_burner_mode=ctg9_duct_burner_mode,
                                             duct_burner_fuel=ctg9_duct_burner_fuel,
                                             is_pag_on=ctg9_is_pag_on,
                                             pag_availability=ctg9_pag_availability,
                                             is_peak_fire_on=ctg9_is_peak_fire_on
                                             )

    trains = [train_8_request, train_9_request]

    is_stg_online = True

    block_request = BlockSimulationRequest(ambient_conditions=ambient_conditions, trains=trains,
                                           is_stg_online=is_stg_online)

    print('\n\n')
    schema = BlockSimulationRequestSchema()

    try:
        json_dict = schema.dump(block_request)

        pprint(json_dict, indent=4)

        assert isinstance(json_dict, dict)

        assert json_dict['ambient_conditions']['db'] == db
        assert json_dict['ambient_conditions']['rh'] == rh * 100
        assert json_dict['ambient_conditions']['baro'] == baro

        assert json_dict['is_stg_online'] == is_stg_online

        assert json_dict['trains'][0]['ctg'] == block.trains[0].ctg.name
        assert json_dict['trains'][0]['ctg_mode'] == ctg8_ctg_mode.value
        assert json_dict['trains'][0]['ctg_availability'] == ctg8_ctg_availability
        assert json_dict['trains'][0]['is_inlet_conditioner_on'] == ctg8_is_inlet_conditioner_on
        assert json_dict['trains'][0][
                   'inlet_conditioner_availability'] == ctg8_inlet_conditioner_availability
        assert json_dict['trains'][0]['duct_burner_mode'] == ctg8_duct_burner_mode.value
        assert json_dict['trains'][0]['duct_burner_fuel'] == ctg8_duct_burner_fuel
        assert json_dict['trains'][0]['is_pag_on'] == ctg8_is_pag_on
        assert json_dict['trains'][0]['pag_availability'] == ctg8_pag_availability
        assert json_dict['trains'][0]['is_peak_fire_on'] == ctg8_is_peak_fire_on

        assert json_dict['trains'][1]['ctg'] == block.trains[1].ctg.name
        assert json_dict['trains'][1]['ctg_mode'] == ctg9_ctg_mode.value
        assert json_dict['trains'][1]['ctg_availability'] == ctg9_ctg_availability
        assert json_dict['trains'][1]['is_inlet_conditioner_on'] == ctg9_is_inlet_conditioner_on
        assert json_dict['trains'][1][
                   'inlet_conditioner_availability'] == ctg9_inlet_conditioner_availability
        assert json_dict['trains'][1]['duct_burner_mode'] == ctg9_duct_burner_mode.value
        assert json_dict['trains'][1]['duct_burner_fuel'] == ctg9_duct_burner_fuel
        assert json_dict['trains'][1]['is_pag_on'] == ctg9_is_pag_on
        assert json_dict['trains'][1]['pag_availability'] == ctg9_pag_availability
        assert json_dict['trains'][1]['is_peak_fire_on'] == ctg9_is_peak_fire_on
    except ValidationError as err:
        print(err.valid_data)
        print(err.messages)
        assert len(err.messages) == 0
