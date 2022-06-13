import pytest

from cctwin.assets.block.ambient_conditions import AmbientConditions
from cctwin.assets.block.block_constants import BlockConstants


def test_ambient_valid_ranges():
    db = 90
    rh = 60 / 100
    baro = 14.67

    ambient_conditions = AmbientConditions(db=db, rh=rh, baro=baro)

    assert isinstance(ambient_conditions, AmbientConditions)
    assert isinstance(ambient_conditions.db, list)
    assert isinstance(ambient_conditions.rh, list)
    assert isinstance(ambient_conditions.baro, list)
    assert all(x == db for x in ambient_conditions.db)
    assert all(x == rh for x in ambient_conditions.rh)
    assert all(x == baro for x in ambient_conditions.baro)


def test_ambient_db_invalid_range_high():
    db = BlockConstants.MAX_DB + 1
    rh = 60 / 100
    baro = 14.67

    with pytest.raises(ValueError):
        AmbientConditions(db=db, rh=rh, baro=baro)


def test_ambient_db_invalid_range_low():
    db = BlockConstants.MIN_DB - 1
    rh = 60 / 100
    baro = 14.67

    with pytest.raises(ValueError):
        AmbientConditions(db=db, rh=rh, baro=baro)


def test_ambient_rh_invalid_range_high():
    db = 90
    rh = BlockConstants.MAX_RH + 1 / 100
    baro = 14.67

    with pytest.raises(ValueError):
        AmbientConditions(db=db, rh=rh, baro=baro)


def test_ambient_rh_invalid_range_low():
    db = 90
    rh = BlockConstants.MIN_RH - 1 / 100
    baro = 14.67

    with pytest.raises(ValueError):
        AmbientConditions(db=db, rh=rh, baro=baro)


def test_ambient_baro_invalid_range_high():
    db = 90
    rh = 60 / 100
    baro = BlockConstants.MAX_BARO + 1

    with pytest.raises(ValueError):
        AmbientConditions(db=db, rh=rh, baro=baro)


def test_ambient_baro_invalid_range_low():
    db = 90
    rh = 60 / 100
    baro = BlockConstants.MIN_BARO - 1

    with pytest.raises(ValueError):
        AmbientConditions(db=db, rh=rh, baro=baro)
