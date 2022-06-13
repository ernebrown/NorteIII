from marshmallow import ValidationError, pprint

from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.hrsg.duct_burner_mode import DuctBurnerMode
from cctwin.assets.hrsg.hrsg_constants import HrsgConstants
from cctwin.assets.inletconditioner.inlet_conditioner_constants import InletConditionerConstants
from cctwin.assets.train.train_request import TrainSimulationRequest, TrainSimulationRequestSchema


def test_from_json(ctg8):
    ctg_mode = CtgOperationMode.MINLOAD
    ctg_availability = 100
    is_inlet_conditioner_on = True
    inlet_conditioner_availability = InletConditionerConstants.TON_DEFAULT
    duct_burner_mode = DuctBurnerMode.MAX
    duct_burner_fuel = HrsgConstants.MAX_FUEL
    is_pag_on = False
    pag_availability = 100
    is_peak_fire_on = False

    json_dict = {'ctg': ctg8.name,
                 'ctg_mode': ctg_mode.value,
                 'ctg_availability': ctg_availability,
                 'is_inlet_conditioner_on': is_inlet_conditioner_on,
                 'inlet_conditioner_availability': inlet_conditioner_availability,
                 'duct_burner_mode': duct_burner_mode.value,
                 'duct_burner_fuel': duct_burner_fuel,
                 'is_pag_on': is_pag_on,
                 'pag_availability': pag_availability,
                 'is_peak_fire_on': is_peak_fire_on
                 }
    schema = TrainSimulationRequestSchema()

    try:
        train_request = schema.load(json_dict)
        assert isinstance(train_request, TrainSimulationRequest)
        assert train_request.ctg == ctg8.name
        assert train_request.ctg_mode == ctg_mode.value
        assert train_request.ctg_availability == ctg_availability
        assert train_request.is_inlet_conditioner_on == is_inlet_conditioner_on
        assert train_request.inlet_conditioner_availability == inlet_conditioner_availability
        assert train_request.duct_burner_mode == duct_burner_mode.value
        assert train_request.is_pag_on == is_pag_on
        assert train_request.pag_availability == pag_availability
        assert train_request.is_peak_fire_on == is_peak_fire_on
    except ValidationError as err:
        print(err.valid_data)
        print(err.messages)
        assert len(err.messages) == 0


def test_to_json(ctg8):
    ctg_mode = CtgOperationMode.MINLOAD
    ctg_availability = 100
    is_inlet_conditioner_on = True
    inlet_conditioner_availability = InletConditionerConstants.TON_DEFAULT
    duct_burner_mode = DuctBurnerMode.MAX
    duct_burner_fuel = HrsgConstants.MAX_FUEL
    is_pag_on = False
    pag_availability = 100
    is_peak_fire_on = False

    train_request = TrainSimulationRequest(ctg=ctg8.name,
                                           ctg_mode=ctg_mode,
                                           ctg_availability=ctg_availability,
                                           is_inlet_conditioner_on=is_inlet_conditioner_on,
                                           inlet_conditioner_availability=inlet_conditioner_availability,
                                           duct_burner_mode=duct_burner_mode,
                                           duct_burner_fuel=duct_burner_fuel,
                                           is_pag_on=is_pag_on,
                                           pag_availability=pag_availability,
                                           is_peak_fire_on=is_peak_fire_on
                                           )

    schema = TrainSimulationRequestSchema()
    print('\n\n')

    try:
        json_dict = schema.dump(train_request)
        assert isinstance(json_dict, dict)
        assert json_dict['ctg'] == ctg8.name
        assert json_dict['ctg_mode'] == ctg_mode.value
        assert json_dict['ctg_availability'] == ctg_availability
        assert json_dict['is_inlet_conditioner_on'] == is_inlet_conditioner_on
        assert json_dict['inlet_conditioner_availability'] == inlet_conditioner_availability
        assert json_dict['duct_burner_mode'] == duct_burner_mode.value
        assert json_dict['duct_burner_fuel'] == duct_burner_fuel
        assert json_dict['is_pag_on'] == is_pag_on
        assert json_dict['pag_availability'] == pag_availability
        assert json_dict['is_peak_fire_on'] == is_peak_fire_on
        pprint(json_dict, indent=4)
    except ValidationError as err:
        print(err.valid_data)
        print(err.messages)
        assert len(err.messages) == 0
