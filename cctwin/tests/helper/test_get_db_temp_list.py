from cctwin.helper.helper import get_db_temp_list


def test_get_db_temps_for_minus18():
    db = -18
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(-20, -20 + 11))


def test_get_db_temps_for_minus19():
    db = -19
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(-20, -20 + 11))


def test_get_db_temps_for_minus19_5():
    db = -19.5
    db_temps = get_db_temp_list(db)
    assert db_temps == [-19.5, -19, -18, -17, -16, -15, -14, -13, -12, -11, -10]


def test_get_db_temps_for_minus18_2():
    db = -18.2
    db_temps = get_db_temp_list(db)
    assert db_temps == [-20, -19, -18.2, -17, -16, -15, -14, -13, -12, -11, -10]


def test_get_db_temps_for_minus16():
    db = -16
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(-20, -20 + 11))


def test_get_db_temps_for_minus15():
    db = -15
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(-20, -20 + 11))


def test_get_db_temps_for_minus15_51():
    db = -15.51
    db_temps = get_db_temp_list(db)
    assert db_temps == [-20, -19, -18, -17, -15.51, -15, -14, -13, -12, -11, -10]


def test_get_db_temps_for_minus15_2():
    db = -15.2
    db_temps = get_db_temp_list(db)
    assert db_temps == [-20, -19, -18, -17, -16, -15.2, -14, -13, -12, -11, -10]


def test_get_db_temps_for_minus14_9():
    db = -14.9
    db_temps = get_db_temp_list(db)
    assert db_temps == [-20, -19, -18, -17, -16, -14.9, -14, -13, -12, -11, -10]


def test_get_db_temps_for_minus14():
    db = -14
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(-19, -19 + 11))


def test_get_db_temps_for_minus14_49():
    db = -14.49
    db_temps = get_db_temp_list(db)
    assert db_temps == [-19, -18, -17, -16, -15, -14.49, -13, -12, -11, -10, -9]


def test_get_db_temps_for_plus6():
    db = 6
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(1, 1 + 11))


def test_get_db_temps_for_plus6_49():
    db = 6.49
    db_temps = get_db_temp_list(db)
    assert db_temps == [1, 2, 3, 4, 5, 6.49, 7, 8, 9, 10, 11]


def test_get_db_temps_for_plus6_51():
    db = 6.51
    db_temps = get_db_temp_list(db)
    assert db_temps == [2, 3, 4, 5, 6, 6.51, 8, 9, 10, 11, 12]


def test_get_db_temps_for_plus14():
    db = 14
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(9, 9 + 11))


def test_get_db_temps_for_plus114():
    db = 114
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(109, 109 + 11))


def test_get_db_temps_for_plus114_49():
    db = 114.49
    db_temps = get_db_temp_list(db)
    assert db_temps == [109, 110, 111, 112, 113, 114.49, 115, 116, 117, 118, 119]


def test_get_db_temps_for_plus114_51():
    db = 114.51
    db_temps = get_db_temp_list(db)
    assert db_temps == [110, 111, 112, 113, 114, 114.51, 116, 117, 118, 119, 120]


def test_get_db_temps_for_plus115():
    db = 115
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(121 - 11, 121))


def test_get_db_temps_for_plus116():
    db = 116
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(121 - 11, 121))


def test_get_db_temps_for_plus117():
    db = 117
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(121 - 11, 121))


def test_get_db_temps_for_plus118():
    db = 118
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(121 - 11, 121))


def test_get_db_temps_for_plus119():
    db = 119
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(121 - 11, 121))


def test_get_db_temps_for_plus119_49():
    db = 119.49
    db_temps = get_db_temp_list(db)
    assert db_temps == [110, 111, 112, 113, 114, 115, 116, 117, 118, 119.49, 120]


def test_get_db_temps_for_plus119_51():
    db = 119.51
    db_temps = get_db_temp_list(db)
    assert db_temps == [110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 119.51]


def test_get_db_temps_for_plus120():
    db = 120
    db_temps = get_db_temp_list(db)
    assert db_temps == list(range(121 - 11, 121))
