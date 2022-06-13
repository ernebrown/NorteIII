import pytest

from cctwin.assets.ctg.ctg_input import CtgInput
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode


def test_ctg_input_constructor():
    ctg_operation_mode = CtgOperationMode.BASELOAD.value
    ctg_avlblty = 60
    pag_avlblty = 60
    is_peak_fire_on = False
    cit = [0, 0]
    baro = [14.2, 15]
    site_config = '1X1'
    ctg_input = CtgInput(ctg_operation_mode=ctg_operation_mode,
                         site_config=site_config,
                         ctg_avlblty=ctg_avlblty,
                         pag_avlblty=pag_avlblty,
                         is_peak_fire_on=is_peak_fire_on,
                         cit=cit,
                         baro=baro)

    assert isinstance(ctg_input, CtgInput)
    assert isinstance(ctg_input.ctg_operation_mode, str)
    assert isinstance(ctg_input.ctg_avlblty, (int, float))
    assert isinstance(ctg_input.pag_avlblty, (int, float))
    assert isinstance(ctg_input.is_peak_fire_on, (int, float))
    assert isinstance(ctg_input.cit, list)
    assert isinstance(ctg_input.baro, list)
    assert all(isinstance(x, (int, float)) for x in ctg_input.cit)
    assert all(isinstance(x, (int, float)) for x in ctg_input.baro)


def test_ctg_input_raises_exception_cit():
    ctg_operation_mode = CtgOperationMode.BASELOAD.value
    ctg_avlblty = 60
    pag_avlblty = 60
    is_peak_fire_on = False
    cit = [0, 125]
    baro = [14.2, 15]
    site_config = '1X1'
    with pytest.raises(ValueError):
        CtgInput(ctg_operation_mode=ctg_operation_mode,
                 site_config=site_config,
                 ctg_avlblty=ctg_avlblty,
                 pag_avlblty=pag_avlblty,
                 is_peak_fire_on=is_peak_fire_on,
                 cit=cit,
                 baro=baro)


def test_ctg_input_raises_exception_baro():
    ctg_operation_mode = CtgOperationMode.BASELOAD.value
    ctg_avlblty = 60
    pag_avlblty = 60
    is_peak_fire_on = False
    cit = [0, 0]
    baro = [14.2, 15.1]
    site_config = '1X1'
    with pytest.raises(ValueError):
        CtgInput(ctg_operation_mode=ctg_operation_mode,
                 site_config=site_config,
                 ctg_avlblty=ctg_avlblty,
                 pag_avlblty=pag_avlblty,
                 is_peak_fire_on=is_peak_fire_on,
                 cit=cit,
                 baro=baro)


def test_ctg_input_raises_exception_ctg_avlblty():
    ctg_operation_mode = CtgOperationMode.BASELOAD.value
    ctg_avlblty = 120
    pag_avlblty = 60
    is_peak_fire_on = False
    cit = [0, 0]
    baro = [14.2, 15]
    site_config = '1X1'
    with pytest.raises(ValueError):
        CtgInput(ctg_operation_mode=ctg_operation_mode,
                 site_config=site_config,
                 ctg_avlblty=ctg_avlblty,
                 pag_avlblty=pag_avlblty,
                 is_peak_fire_on=is_peak_fire_on,
                 cit=cit,
                 baro=baro)


def test_ctg_input_raises_exception_pag_avlblty():
    ctg_operation_mode = CtgOperationMode.BASELOAD.value
    ctg_avlblty = 100
    pag_avlblty = -2
    is_peak_fire_on = False
    cit = [0, 0]
    baro = [14.2, 15]
    site_config = '1X1'
    with pytest.raises(ValueError):
        CtgInput(ctg_operation_mode=ctg_operation_mode,
                 site_config=site_config,
                 ctg_avlblty=ctg_avlblty,
                 pag_avlblty=pag_avlblty,
                 is_peak_fire_on=is_peak_fire_on,
                 cit=cit,
                 baro=baro)


# noinspection PyTypeChecker
def test_ctg_input_raises_exception_is_peak_fire_on():
    ctg_operation_mode = CtgOperationMode.BASELOAD.value
    ctg_avlblty = 100
    pag_avlblty = 0
    is_peak_fire_on = 'false'
    cit = [0, 0]
    baro = [14.2, 15]
    site_config = '1X1'
    with pytest.raises(TypeError):
        CtgInput(ctg_operation_mode=ctg_operation_mode,
                 site_config=site_config,
                 ctg_avlblty=ctg_avlblty,
                 pag_avlblty=pag_avlblty,
                 is_peak_fire_on=is_peak_fire_on,
                 cit=cit,
                 baro=baro)


def test_ctg_input_raises_exception_empty_cit():
    ctg_operation_mode = CtgOperationMode.BASELOAD.value
    ctg_avlblty = 100
    pag_avlblty = 0
    is_peak_fire_on = True
    cit = []
    baro = [14.2, 15]
    site_config = '1X1'
    with pytest.raises(IndexError):
        CtgInput(ctg_operation_mode=ctg_operation_mode,
                 site_config=site_config,
                 ctg_avlblty=ctg_avlblty,
                 pag_avlblty=pag_avlblty,
                 is_peak_fire_on=is_peak_fire_on,
                 cit=cit,
                 baro=baro)


# noinspection PyTypeChecker
def test_ctg_input_raises_exception_str_cit():
    ctg_operation_mode = CtgOperationMode.BASELOAD.value
    ctg_avlblty = 100
    pag_avlblty = 0
    is_peak_fire_on = True
    cit = ['a', 'b']
    baro = [14.2, 15]
    site_config = '1X1'
    with pytest.raises(TypeError):
        CtgInput(ctg_operation_mode=ctg_operation_mode,
                 site_config=site_config,
                 ctg_avlblty=ctg_avlblty,
                 pag_avlblty=pag_avlblty,
                 is_peak_fire_on=is_peak_fire_on,
                 cit=cit,
                 baro=baro)


def test_ctg_input_raises_exception_empty_baro():
    ctg_operation_mode = CtgOperationMode.BASELOAD.value
    ctg_avlblty = 100
    pag_avlblty = 0
    is_peak_fire_on = True
    cit = [14.2, 15]
    baro = []
    site_config = '1X1'
    with pytest.raises(IndexError):
        CtgInput(ctg_operation_mode=ctg_operation_mode,
                 site_config=site_config,
                 ctg_avlblty=ctg_avlblty,
                 pag_avlblty=pag_avlblty,
                 is_peak_fire_on=is_peak_fire_on,
                 cit=cit,
                 baro=baro)


# noinspection PyTypeChecker
def test_ctg_input_raises_exception_str_baro():
    ctg_operation_mode = CtgOperationMode.BASELOAD.value
    ctg_avlblty = 100
    pag_avlblty = 0
    is_peak_fire_on = True
    cit = [14.2, 15]
    baro = ['a', 'b']
    site_config = '1X1'
    with pytest.raises(TypeError):
        CtgInput(ctg_operation_mode=ctg_operation_mode,
                 site_config=site_config,
                 ctg_avlblty=ctg_avlblty,
                 pag_avlblty=pag_avlblty,
                 is_peak_fire_on=is_peak_fire_on,
                 cit=cit,
                 baro=baro)


def test_ctg_input_raises_exception_unequal_cit_baro():
    ctg_operation_mode = CtgOperationMode.BASELOAD.value
    ctg_avlblty = 100
    pag_avlblty = 0
    is_peak_fire_on = True
    cit = [20, 30, 40]
    baro = [14.2, 15]
    site_config = '1X1'
    with pytest.raises(IndexError):
        CtgInput(ctg_operation_mode=ctg_operation_mode,
                 site_config=site_config,
                 ctg_avlblty=ctg_avlblty,
                 pag_avlblty=pag_avlblty,
                 is_peak_fire_on=is_peak_fire_on,
                 cit=cit,
                 baro=baro)
