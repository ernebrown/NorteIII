from marshmallow import ValidationError, pprint

from cctwin.assets.ctg.ctg_input import CtgInput
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.ctg.ctg_output import CtgSimulationOutputSchema


def test_to_json(ctg8):
    cit = 94.5
    baro = 14.7
    site_config = '2X1'
    ctg_input = CtgInput(ctg_operation_mode=CtgOperationMode.BASELOAD.value,
                         site_config=site_config,
                         ctg_avlblty=100,
                         pag_avlblty=0,
                         is_peak_fire_on=False,
                         cit=cit,
                         baro=baro)
    performance = ctg8.get_performance(ctg_input=ctg_input)

    exclude = []
    if ctg8.pag_incremental is None:
        exclude.append('pag_mw')
        exclude.append('pag_fuel')
        exclude.append('pag_exh_temp')
        exclude.append('pag_steam')
    if ctg8.peak_fire_incremental is None:
        exclude.append('peak_fire_mw')
        exclude.append('peak_fire_fuel')
        exclude.append('peak_fire_exh_temp')

    schema = CtgSimulationOutputSchema(exclude=exclude)

    print('\n\n')

    try:
        json_dict = schema.dump(performance)

        assert isinstance(json_dict, dict)
        assert json_dict['name'] == ctg8.name
        assert isinstance(json_dict['mw'], (int, float))
        assert isinstance(json_dict['fuel'], (int, float))
        assert isinstance(json_dict['cpd'], (int, float))
        assert isinstance(json_dict['ctd'], (int, float))
        assert isinstance(json_dict['exh_temp'], (int, float))
        pprint(json_dict, indent=4)
    except ValidationError as err:
        print(err.valid_data)
        print(err.messages)
        assert len(err.messages) == 0
