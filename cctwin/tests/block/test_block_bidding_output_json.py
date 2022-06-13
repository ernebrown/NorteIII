import json
from random import randrange

from marshmallow import ValidationError, pprint

from cctwin.assets.block.block_output import BlockBiddingOutputSchema
from cctwin.assets.block.block_request import BlockBiddingRequest, BlockBiddingRequestSchema


def test_to_json(block):
    num_of_cases = 24
    db = [randrange(70, 97) for p in range(0, num_of_cases)]
    rh = [randrange(1, 10) / 10 for p in range(0, num_of_cases)]
    baro = [randrange(1468, 1475) / 100 for p in range(0, num_of_cases)]

    import pandas as pd
    times = pd.date_range('2019-09-15', periods=num_of_cases, freq='1H')

    times = times.tolist()

    times = [time.strftime('%Y-%m-%d %H:%M:%S') for time in times]
    ctg8_name = block.trains[0].ctg.name
    ctg8_ctg_availability = 100
    ctg8_inlet_conditioner_availability = 100
    ctg8_duct_burner_availability = 100

    ctg9_name = block.trains[1].ctg.name
    ctg9_ctg_availability = 100
    ctg9_inlet_conditioner_availability = 100
    ctg9_duct_burner_availability = 100

    is_stg_online = True

    request_json_dict = {
        'times': times,
        'ambient_conditions':
            {
                'db': db,
                'rh': rh,
                'baro': baro
            },
        'trains': [
            {
                'ctg': ctg8_name,
                'ctg_availability': ctg8_ctg_availability,
                'inlet_conditioner_availability': ctg8_inlet_conditioner_availability,
                'duct_burner_availability': ctg8_duct_burner_availability,
            },
            {
                'ctg': ctg9_name,
                'ctg_availability': ctg9_ctg_availability,
                'inlet_conditioner_availability': ctg9_inlet_conditioner_availability,
                'duct_burner_availability': ctg9_duct_burner_availability,
            }],
        'is_stg_online': is_stg_online
    }

    print('\n\n')

    pprint(request_json_dict, indent=4)

    print('\n\n')

    try:
        schema = BlockBiddingRequestSchema()
        block_bidding_request = schema.load(request_json_dict)

        assert isinstance(block_bidding_request, BlockBiddingRequest)
        block_bidding_outputs = block.get_data_for_bids(block.create_block_configs(), block_bidding_request)

        assert isinstance(block_bidding_outputs, list)
        schema = BlockBiddingOutputSchema()
        json_dict = schema.dump(block_bidding_outputs, many=True)
        foo = json.dumps(json_dict, indent=4)
        print(foo)
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        assert len(err.messages) == 0
