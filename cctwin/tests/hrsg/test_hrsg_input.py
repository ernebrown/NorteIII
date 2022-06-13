import pytest

from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.hrsg.hrsg_input import HrsgInput


def test_hrsg_input_constructor():
    ctg_mw = [120]
    ctg_exh_temp = [1100]
    db_fuel = [695]
    ctg_mode = CtgOperationMode.BASELOAD
    hrsg_input = HrsgInput(ctg_mode=ctg_mode,
                           ctg_mw=ctg_mw,
                           ctg_exh_temp=ctg_exh_temp,
                           db_fuel=db_fuel)
    assert isinstance(hrsg_input, HrsgInput)
    assert isinstance(hrsg_input.ctg_mw, (int, float, list))
    assert isinstance(hrsg_input.ctg_exh_temp, (int, float, list))
    assert isinstance(hrsg_input.db_fuel, (int, float, list))


def test_hrsg_input_raises_exception_ctg_mw():
    ctg_mw = [-1]
    ctg_exh_temp = [1100]
    db_fuel = [695]
    ctg_mode = CtgOperationMode.BASELOAD
    with pytest.raises(ValueError):
        HrsgInput(ctg_mode=ctg_mode,
                  ctg_mw=ctg_mw,
                  ctg_exh_temp=ctg_exh_temp,
                  db_fuel=db_fuel)


def test_hrsg_input_raises_exception_ctg_exh_temp():
    ctg_mw = [150]
    ctg_exh_temp = [-1]
    db_fuel = [695]
    ctg_mode = CtgOperationMode.BASELOAD
    with pytest.raises(ValueError):
        HrsgInput(ctg_mode=ctg_mode,
                  ctg_mw=ctg_mw,
                  ctg_exh_temp=ctg_exh_temp,
                  db_fuel=db_fuel)


def test_hrsg_input_raises_exception_db_fuel_percent():
    ctg_mw = [150]
    ctg_exh_temp = [1100]
    db_fuel= [730]
    ctg_mode = CtgOperationMode.BASELOAD
    with pytest.raises(ValueError):
        HrsgInput(ctg_mode=ctg_mode,
                  ctg_mw=ctg_mw,
                  ctg_exh_temp=ctg_exh_temp,
                  db_fuel=db_fuel)


def test_hrsg_input_raises_exception_empty_ctg_mw():
    ctg_mw = []
    ctg_exh_temp = [1100]
    db_fuel = [695]
    ctg_mode = CtgOperationMode.BASELOAD
    with pytest.raises(IndexError):
        HrsgInput(ctg_mode=ctg_mode,
                  ctg_mw=ctg_mw,
                  ctg_exh_temp=ctg_exh_temp,
                  db_fuel=db_fuel)


def test_hrsg_input_raises_exception_empty_ctg_exh_temp():
    ctg_mw = [150]
    ctg_exh_temp = []
    db_fuel = [695]
    ctg_mode = CtgOperationMode.BASELOAD
    with pytest.raises(IndexError):
        HrsgInput(ctg_mode=ctg_mode,
                  ctg_mw=ctg_mw,
                  ctg_exh_temp=ctg_exh_temp,
                  db_fuel=db_fuel)


def test_hrsg_input_raises_exception_empty_db_fuel():
    ctg_mw = [150]
    ctg_exh_temp = [1100]
    db_fuel = []
    ctg_mode = CtgOperationMode.BASELOAD
    with pytest.raises(IndexError):
        HrsgInput(ctg_mode=ctg_mode,
                  ctg_mw=ctg_mw,
                  ctg_exh_temp=ctg_exh_temp,
                  db_fuel=db_fuel)


# noinspection PyTypeChecker
def test_hrsg_input_raises_exception_str_ctg_mw():
    ctg_mw = ['150']
    ctg_exh_temp = [1100]
    db_fuel = [695]
    ctg_mode = CtgOperationMode.BASELOAD
    with pytest.raises(TypeError):
        HrsgInput(ctg_mode=ctg_mode,
                  ctg_mw=ctg_mw,
                  ctg_exh_temp=ctg_exh_temp,
                  db_fuel=db_fuel)


# noinspection PyTypeChecker
def test_hrsg_input_raises_exception_str_ctg_exh_temp():
    ctg_mw = [150]
    ctg_exh_temp = ['1100']
    db_fuel = [695]
    ctg_mode = CtgOperationMode.BASELOAD
    with pytest.raises(TypeError):
        HrsgInput(ctg_mode=ctg_mode,
                  ctg_mw=ctg_mw,
                  ctg_exh_temp=ctg_exh_temp,
                  db_fuel=db_fuel)


# noinspection PyTypeChecker
def test_hrsg_input_raises_exception_str_db_fuel():
    ctg_mw = [150]
    ctg_exh_temp = [1100]
    db_fuel = ['695']
    ctg_mode = CtgOperationMode.BASELOAD
    with pytest.raises(TypeError):
        HrsgInput(ctg_mode=ctg_mode,
                  ctg_mw=ctg_mw,
                  ctg_exh_temp=ctg_exh_temp,
                  db_fuel=db_fuel)


def test_hrsg_input_raises_exception_unequal_lists_1():
    ctg_mw = [150]
    ctg_exh_temp = [1100, 1105]
    db_fuel = [695]
    ctg_mode = CtgOperationMode.BASELOAD
    with pytest.raises(IndexError):
        HrsgInput(ctg_mode=ctg_mode,
                  ctg_mw=ctg_mw,
                  ctg_exh_temp=ctg_exh_temp,
                  db_fuel=db_fuel)


def test_hrsg_input_raises_exception_unequal_lists_2():
    ctg_mw = [150, 151]
    ctg_exh_temp = [1100]
    db_fuel = [695]
    ctg_mode = CtgOperationMode.BASELOAD
    with pytest.raises(IndexError):
        HrsgInput(ctg_mode=ctg_mode,
                  ctg_mw=ctg_mw,
                  ctg_exh_temp=ctg_exh_temp,
                  db_fuel=db_fuel)


def test_hrsg_input_raises_exception_unequal_lists_3():
    ctg_mw = [150]
    ctg_exh_temp = [1100]
    db_fuel = [695, 690]
    ctg_mode = CtgOperationMode.BASELOAD
    with pytest.raises(IndexError):
        HrsgInput(ctg_mode=ctg_mode,
                  ctg_mw=ctg_mw,
                  ctg_exh_temp=ctg_exh_temp,
                  db_fuel=db_fuel)
