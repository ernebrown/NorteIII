import pytest

from cctwin.assets.inletconditioner.inlet_conditioner_constants import InletConditionerConstants
from cctwin.assets.inletconditioner.inlet_conditioner_input import InletConditionerInput


def test_inlet_conditioner_input_constructor():
    avlblty = 100
    db = [0, 0]
    rh = [0, 0]
    baro = [14.2, 15]
    inlet_conditioner_input = InletConditionerInput(avlblty=avlblty,
                                                    db=db,
                                                    rh=rh,
                                                    baro=baro)
    assert isinstance(inlet_conditioner_input, InletConditionerInput)
    assert isinstance(inlet_conditioner_input.avlblty, (int, float))
    assert isinstance(inlet_conditioner_input.db, list)
    assert isinstance(inlet_conditioner_input.rh, list)
    assert isinstance(inlet_conditioner_input.baro, list)
    assert all(isinstance(x, (int, float)) for x in inlet_conditioner_input.db)
    assert all(isinstance(x, (int, float)) for x in inlet_conditioner_input.rh)
    assert all(isinstance(x, (int, float)) for x in inlet_conditioner_input.baro)


def test_inlet_conditioner_input_raises_exception_db():
    avlblty = 60
    db = [0, 121]
    rh = [0, 1]
    baro = [14, 15]
    with pytest.raises(ValueError):
        InletConditionerInput(avlblty=avlblty,
                              db=db,
                              rh=rh,
                              baro=baro)


def test_inlet_conditioner_input_raises_exception_rh():
    avlblty = 60
    db = [0, 120]
    rh = [0, 1.01]
    baro = [14, 15]
    with pytest.raises(ValueError):
        InletConditionerInput(avlblty=avlblty,
                              db=db,
                              rh=rh,
                              baro=baro)


def test_inlet_conditioner_input_raises_exception_baro():
    avlblty = 60
    db = [0, 120]
    rh = [0, 1]
    baro = [14, 15.1]
    with pytest.raises(ValueError):
        InletConditionerInput(avlblty=avlblty,
                              db=db,
                              rh=rh,
                              baro=baro)


def test_inlet_conditioner_input_raises_exception_avlblty():
    avlblty = InletConditionerConstants.MAX_AVLBLTY + 10
    db = [0, 120]
    rh = [0, 1]
    baro = [14, 15]
    with pytest.raises(ValueError):
        InletConditionerInput(avlblty=avlblty,
                              db=db,
                              rh=rh,
                              baro=baro)


def test_inlet_conditioner_input_raises_exception_empty_db():
    avlblty = InletConditionerConstants.MAX_AVLBLTY
    db = []
    rh = [0, 1]
    baro = [14, 15]
    with pytest.raises(IndexError):
        InletConditionerInput(avlblty=avlblty,
                              db=db,
                              rh=rh,
                              baro=baro)


def test_inlet_conditioner_input_raises_exception_empty_rh():
    avlblty = InletConditionerConstants.MAX_AVLBLTY
    db = [0, 10]
    rh = []
    baro = [14, 15]
    with pytest.raises(IndexError):
        InletConditionerInput(avlblty=avlblty,
                              db=db,
                              rh=rh,
                              baro=baro)


def test_inlet_conditioner_input_raises_exception_empty_baro():
    avlblty = InletConditionerConstants.MAX_AVLBLTY
    db = [0, 10]
    rh = [0, 1]
    baro = []
    with pytest.raises(IndexError):
        InletConditionerInput(avlblty=avlblty,
                              db=db,
                              rh=rh,
                              baro=baro)


def test_inlet_conditioner_input_raises_exception_unequal_lists():
    avlblty = InletConditionerConstants.MAX_AVLBLTY
    db = [0, 10]
    rh = [0, 1]
    baro = [14]
    with pytest.raises(IndexError):
        InletConditionerInput(avlblty=avlblty,
                              db=db,
                              rh=rh,
                              baro=baro)


# noinspection PyTypeChecker
def test_inlet_conditioner_input_raises_exception_str_db():
    avlblty = InletConditionerConstants.MAX_AVLBLTY
    db = ['0', '10']
    rh = [0, 1]
    baro = [14]
    with pytest.raises(TypeError):
        InletConditionerInput(avlblty=avlblty,
                              db=db,
                              rh=rh,
                              baro=baro)


# noinspection PyTypeChecker
def test_inlet_conditioner_input_raises_exception_str_rh():
    avlblty = InletConditionerConstants.MAX_AVLBLTY
    db = [0, 10]
    rh = ['0', '1']
    baro = [14, 15]
    with pytest.raises(TypeError):
        InletConditionerInput(avlblty=avlblty,
                              db=db,
                              rh=rh,
                              baro=baro)


# noinspection PyTypeChecker
def test_inlet_conditioner_input_raises_exception_str_baro():
    avlblty = InletConditionerConstants.MAX_AVLBLTY
    db = [0, 10]
    rh = [0, 1]
    baro = ['14', '15']
    with pytest.raises(TypeError):
        InletConditionerInput(avlblty=avlblty,
                              db=db,
                              rh=rh,
                              baro=baro)
