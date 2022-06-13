from marshmallow import ValidationError, pprint

from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.hrsg.hrsg_input import HrsgInput
from cctwin.assets.hrsg.hrsg_output import HrsgSimulationOutputSchema


def test_to_json(hrsg8):
    ctg_mw = 151.8
    ctg_exh_temp = 1142.6
    db_fuel = 695

    ctg_mode = CtgOperationMode.BASELOAD
    hrsg_input = HrsgInput(ctg_mode=ctg_mode,
                           ctg_mw=ctg_mw,
                           ctg_exh_temp=ctg_exh_temp,
                           db_fuel=db_fuel)

    performance = hrsg8.get_performance(hrsg_input)

    exclude = []
    if not hrsg8.has_duct_burner:
        exclude.append('duct_burner_fuel')

    schema = HrsgSimulationOutputSchema(exclude=exclude)

    print('\n\n')

    try:
        json_dict = schema.dump(performance)
        assert isinstance(json_dict, dict)

        expected_keys = ['duct_burner_fuel', 'hp_flow', 'hp_press', 'hp_temp', 'hp_sh_temp', 'hrh_flow', 'hrh_press',
                         'hrh_temp', 'lp_flow', 'lp_temp', 'lp_press']
        assert len(expected_keys) == len(json_dict.keys())
        assert set(json_dict.keys()) == set(expected_keys)
        pprint(json_dict, indent=4)
    except ValidationError as err:
        print(err.valid_data)
        print(err.messages)
        assert len(err.messages) == 0
