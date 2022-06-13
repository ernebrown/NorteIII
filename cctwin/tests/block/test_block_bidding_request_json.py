from datetime import datetime

from marshmallow import ValidationError, pprint

from cctwin.assets.block.ambient_conditions import AmbientConditions
from cctwin.assets.block.block_request import BlockBiddingRequest, BlockBiddingRequestSchema
from cctwin.assets.inletconditioner.inlet_conditioner_constants import InletConditionerConstants
from cctwin.assets.train.train_request import TrainBiddingRequest

ton = InletConditionerConstants.TON_DEFAULT


def test_from_json(ctg8, ctg9):
    db = 90
    rh = 60
    baro = 14.67

    times = ['2019-10-05 00:00:00']
    is_stg_online = True

    ctg8_ctg_availability = 100
    ctg8_inlet_conditioner_availability = 56.24
    ctg8_duct_burner_availability = 94.26

    ctg9_ctg_availability = 100
    ctg9_inlet_conditioner_availability = 100
    ctg9_duct_burner_availability = 100

    json_dict = {
        'times': times,
        'ambient_conditions':
            {
                'db': db,
                'rh': rh,
                'baro': baro
            },
        'trains': [
            {
                'ctg': ctg8.name,
                'ctg_availability': ctg8_ctg_availability,
                'inlet_conditioner_availability': ctg8_inlet_conditioner_availability,
                'duct_burner_availability': ctg8_duct_burner_availability,
            },
            {
                'ctg': ctg9.name,
                'ctg_availability': ctg9_ctg_availability,
                'inlet_conditioner_availability': ctg9_inlet_conditioner_availability,
                'duct_burner_availability': ctg9_duct_burner_availability,
            }],
        'is_stg_online': is_stg_online
    }

    print('\n\n')

    pprint(json_dict, indent=4)
    print('\n\n')

    try:
        schema = BlockBiddingRequestSchema()
        block_bidding_request = schema.load(json_dict)

        assert isinstance(block_bidding_request, BlockBiddingRequest)
        assert isinstance(block_bidding_request.ambient_conditions, AmbientConditions)
        assert isinstance(block_bidding_request.trains, list)
        assert all(isinstance(train, TrainBiddingRequest) for train in block_bidding_request.trains)

        assert block_bidding_request.ambient_conditions.db[0] == db
        assert block_bidding_request.ambient_conditions.rh[0] == rh / 100
        assert block_bidding_request.ambient_conditions.baro[0] == baro

        assert block_bidding_request.trains[0].ctg == ctg8.name
        assert block_bidding_request.trains[0].ctg_availability == ctg8_ctg_availability
        assert block_bidding_request.trains[0].inlet_conditioner_availability == ctg8_inlet_conditioner_availability

        assert block_bidding_request.trains[1].ctg == ctg9.name
        assert block_bidding_request.trains[1].ctg_availability == ctg9_ctg_availability
        assert block_bidding_request.trains[1].inlet_conditioner_availability == ctg9_inlet_conditioner_availability

    except ValidationError as err:
        assert print(err.valid_data)
        assert len(err.messages) == 0


def test_to_json(block):
    db = 90
    rh = 60 / 100
    baro = 14.67
    ambient_conditions = AmbientConditions(db=db, rh=rh, baro=baro)

    ctg8_ctg_availability = 100
    ctg8_inlet_conditioner_availability = 58.2
    ctg8_duct_burner_availability = 90

    ctg9_ctg_availability = 100
    ctg9_inlet_conditioner_availability = 98.5
    ctg9_duct_burner_availability = 80

    times = [datetime.strptime('2019-10-05 00:00:00', '%Y-%m-%d %H:%M:%S')]
    is_stg_online = True

    train_8_request = TrainBiddingRequest(ctg=block.trains[0].ctg.name,
                                          ctg_availability=ctg8_ctg_availability,
                                          inlet_conditioner_availability=ctg8_inlet_conditioner_availability,
                                          duct_burner_availability=ctg8_duct_burner_availability
                                          )

    train_9_request = TrainBiddingRequest(ctg=block.trains[1].ctg.name,
                                          ctg_availability=ctg9_ctg_availability,
                                          inlet_conditioner_availability=ctg9_inlet_conditioner_availability,
                                          duct_burner_availability=ctg9_duct_burner_availability
                                          )

    trains = [train_8_request, train_9_request]

    block_request = BlockBiddingRequest(times=times, ambient_conditions=ambient_conditions, trains=trains,
                                        is_stg_online=is_stg_online)

    print('\n\n')
    schema = BlockBiddingRequestSchema()

    try:
        json_dict = schema.dump(block_request)

        pprint(json_dict, indent=4)

        assert isinstance(json_dict, dict)

        assert json_dict['ambient_conditions']['db'] == db
        assert json_dict['ambient_conditions']['rh'] == rh * 100
        assert json_dict['ambient_conditions']['baro'] == baro

        assert json_dict['trains'][0]['ctg'] == block.trains[0].ctg.name
        assert json_dict['trains'][0]['ctg_availability'] == ctg8_ctg_availability
        assert json_dict['trains'][0]['inlet_conditioner_availability'] == 58.2
        assert json_dict['trains'][0]['duct_burner_availability'] == 90

        assert json_dict['trains'][1]['ctg'] == block.trains[1].ctg.name
        assert json_dict['trains'][1]['ctg_availability'] == ctg9_ctg_availability
        assert json_dict['trains'][1]['inlet_conditioner_availability'] == 98.5
        assert json_dict['trains'][1]['duct_burner_availability'] == 80

    except ValidationError as err:
        print(err.valid_data)
        print(err.messages)
        assert len(err.messages) == 0
