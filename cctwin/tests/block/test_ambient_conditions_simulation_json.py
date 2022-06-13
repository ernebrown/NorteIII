from marshmallow import ValidationError, pprint

from cctwin.assets.block.ambient_conditions import AmbientConditions, AmbientConditionsSimulationSchema


def test_from_json_single():
    db = 90
    rh = 60
    baro = 14.67
    json_dict = {'db': db, 'rh': rh, 'baro': baro}
    print('\n\n')
    pprint(json_dict)
    schema = AmbientConditionsSimulationSchema()

    print('\n\n')

    try:
        result = schema.load(json_dict)
        ambient_conditions = result
        assert isinstance(ambient_conditions, AmbientConditions)
        assert ambient_conditions.db[0] == db
        assert ambient_conditions.rh[0] == rh / 100
        assert ambient_conditions.baro[0] == baro
        print(ambient_conditions.wb[0])
        print(ambient_conditions.dp[0])
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        assert len(err.messages) == 0


def test_from_json_list():
    db = [50, 70, 90]
    rh = [20, 30, 40]
    baro = [14.4, 14.5, 14.6]
    json_dict = {'db': db, 'rh': rh, 'baro': baro}
    print('\n\n')
    pprint(json_dict)
    schema = AmbientConditionsSimulationSchema()

    print('\n\n')

    try:
        result = schema.load(json_dict)
        ambient_conditions = result
        assert isinstance(ambient_conditions, AmbientConditions)
        assert ambient_conditions.db[0] == db[0]
        assert ambient_conditions.rh[0] == rh[0] / 100
        assert ambient_conditions.baro[0] == baro[0]
        print(ambient_conditions.db)
        print(ambient_conditions.rh)
        print(ambient_conditions.baro)
        print(ambient_conditions.wb)
        print(ambient_conditions.dp)
    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        assert len(err.messages) == 0


def test_to_json():
    db = 90
    rh = 60 / 100
    baro = 14.67
    ambient_conditions = AmbientConditions(db=db, rh=rh, baro=baro)
    schema = AmbientConditionsSimulationSchema()

    print('\n\n')

    try:
        json_dict = schema.dump(ambient_conditions)

        assert isinstance(json_dict, dict)
        assert json_dict['db'] == db
        assert json_dict['rh'] == rh * 100
        assert json_dict['baro'] == baro
        pprint(json_dict)
    except ValidationError as err:
        print(err.valid_data)
        print(err.messages)
        assert len(err.messages) == 0
