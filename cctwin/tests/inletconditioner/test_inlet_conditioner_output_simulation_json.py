from marshmallow import ValidationError, pprint

from cctwin.assets.inletconditioner.inlet_conditioner_input import InletConditionerInput
from cctwin.assets.inletconditioner.inlet_conditioner_output import InletConditionerSimulationOutputSchema
from cctwin.assets.inletconditioner.inlet_conditioner_type import InletConditionerType


def test_chiller_to_json(chiller):
    avlblty = 100
    db = 95
    rh = 52 / 100
    baro = 14.7
    inlet_conditioner_input = InletConditionerInput(avlblty=avlblty,
                                                    db=db,
                                                    rh=rh,
                                                    baro=baro)

    performance = chiller.get_performance(inlet_conditioner_input)

    exclude = []
    if chiller.conditioning_system != InletConditionerType.CHILLERS:
        exclude.append('ton')
        # exclude.append('evap_in')
        exclude.append('evap_out')

    schema = InletConditionerSimulationOutputSchema(exclude=exclude)

    print('\n\n')
    try:
        json_dict = schema.dump(performance)
        assert isinstance(json_dict, dict)

        expected_keys = ['cit', 'load', 'ton', 'evap_out']
        assert len(expected_keys) == len(json_dict.keys())
        assert set(json_dict.keys()) == set(expected_keys)
        pprint(json_dict, indent=4)
    except ValidationError as err:
        print(err.valid_data)
        print(err.messages)
        assert len(err.messages) == 0


def test_fogger_to_json(fake_fogger):
    avlblty = 100
    db = 95
    rh = 52 / 100
    baro = 14.7
    inlet_conditioner_input = InletConditionerInput(avlblty=avlblty,
                                                    db=db,
                                                    rh=rh,
                                                    baro=baro)

    performance = fake_fogger.get_performance(inlet_conditioner_input)

    exclude = []
    if fake_fogger.conditioning_system != InletConditionerType.CHILLERS:
        exclude.append('ton')
        # exclude.append('evap_in')
        exclude.append('evap_out')

    schema = InletConditionerSimulationOutputSchema(exclude=exclude)

    print('\n\n')

    try:
        json_dict = schema.dump(performance)
        assert isinstance(json_dict, dict)

        expected_keys = ['cit', 'load']
        assert len(expected_keys) == len(json_dict.keys())
        assert all(k in json_dict.keys() for k in expected_keys)

        pprint(json_dict, indent=4)

    except ValidationError as err:
        print(err.valid_data)
        print(err.messages)
        assert len(err.messages) == 0
