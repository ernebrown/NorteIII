from typing import List, Union

from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.helper import parsers
from cctwin.assets.block.block_constants import BlockConstants
from cctwin.assets.ctg.ctg_constants import CtgConstants


class CtgInput:
    def __init__(self,
                 ctg_operation_mode: str,
                 site_config: str,
                 ctg_avlblty: Union[int, float],
                 pag_avlblty: Union[int, float],
                 is_peak_fire_on: bool,
                 wc_avlblty: Union[int, float],
                 igv_input: bool,
                 igv: Union[None, float, List[Union[None, float]]],
                 cit: Union[int, float, List[Union[int, float]]],
                 baro: Union[int, float, List[Union[int, float]]],
                 db: Union[int, float, List[Union[int, float]]],
                 rh: Union[int, float, List[Union[int, float]]]
                 ):
        self.ctg_operation_mode = ctg_operation_mode
        self.site_config = site_config
        self.ctg_avlblty = ctg_avlblty
        self.pag_avlblty = pag_avlblty
        self.wc_avlblty = wc_avlblty
        self.is_peak_fire_on = is_peak_fire_on
        self.igv_input = igv_input
        self.igv = igv
        self.cit = cit
        self.baro = baro
        self.db = db
        self.rh = rh

        if len(self.cit) != len(self.baro):
            raise IndexError('Lists of CIT and BARO PRESS values should be of equal length')

    @property
    def igv_input(self):
        return self.__igv_input

    @igv_input.setter
    def igv_input(self, value):
        if not isinstance(value, bool):
            raise TypeError('igv input should be passed as boolean')
        self.__igv_input = value

    @property
    def is_peak_fire_on(self):
        return self.__is_peak_fire_on

    @is_peak_fire_on.setter
    def is_peak_fire_on(self, value):
        if not isinstance(value, bool):
            raise TypeError('Is peak-fire on should be passed as boolean')
        self.__is_peak_fire_on = value

    @property
    def ctg_operation_mode(self):
        return self.__ctg_operation_mode

    @ctg_operation_mode.setter
    def ctg_operation_mode(self, value):
        if not isinstance(value, str):
            raise TypeError('CTG Operation mode should be of type string')
        if any(mode.value == value for mode in CtgOperationMode):
            self.__ctg_operation_mode = value
        else:
            raise ValueError(f'Could not parse {value} to any available CTG operation mode')

    @property
    def ctg_avlblty(self):
        return self.__ctg_avlblty

    @ctg_avlblty.setter
    def ctg_avlblty(self, value: Union[int, float]):
        if not 0 <= value <= CtgConstants.MAX_CTG_AVLBLTY:
            raise ValueError(f'CTG availability should be between 0 and {CtgConstants.MAX_CTG_AVLBLTY}')
        self.__ctg_avlblty = value

    @property
    def site_config(self):
        return self.__site_config

    @site_config.setter
    def site_config(self, value: str):
        if not parsers.is_valid_site_config(value):
            raise ValueError(f'Could not parse site config as MXN where M and N are number of CTGs & STGs online')
        self.__site_config = value

    @property
    def pag_avlblty(self):
        return self.__pag_avlblty

    @pag_avlblty.setter
    def pag_avlblty(self, value: Union[int, float]):
        if not 0 <= value <= 100:
            raise ValueError('PAG availability should be between 0 and 100%')
        self.__pag_avlblty = value

    @property
    def wc_avlblty(self):
        return self.__wc_avlblty

    @wc_avlblty.setter
    def wc_avlblty(self, value: Union[int, float]):
        if not 0 <= value <= 100:
            raise ValueError('Wet Compression availability should be between 0 and 100%')
        self.__wc_avlblty = value

    @property
    def cit(self):
        return self.__cit

    @cit.setter
    def cit(self, value: Union[Union[int, float], List[Union[int, float]]]):
        if isinstance(value, list):
            values = value
            if len(values) == 0:
                raise IndexError('List of CIT cannot be empty')
        else:
            values = [value]

        if not all(-20 <= x <= 120 for x in values):
            raise ValueError('All CIT in the list should be between -20 and 120 degF')
        self.__cit = values

    @property
    def baro(self):
        return self.__baro

    @baro.setter
    def baro(self, value: Union[Union[int, float], List[Union[int, float]]]):
        if isinstance(value, list):
            values = value
            if len(values) == 0:
                raise IndexError('List of barometric pressure cannot be empty')
        else:
            values = [value]

        if not all(BlockConstants.MIN_BARO <= x <= BlockConstants.MAX_BARO for x in values):
            raise ValueError('All Barometric pressures in the list should be between 14 and 15 psia')
        self.__baro = values

    @property
    def db(self):
        return self.__db

    @db.setter
    def db(self, value: Union[Union[int, float], List[Union[int, float]]]):
        if isinstance(value, list):
            values = value
            if len(values) == 0:
                raise IndexError('List of DB temperature values  cannot be empty')
        else:
            values = [value]

        if not all(-20 <= x <= 120 for x in values):
            raise ValueError('All DB temperature values in the list should be between -20 and 120 degF')
        self.__db = values

    @property
    def rh(self):
        return self.__rh

    @rh.setter
    def rh(self, value: Union[Union[int, float], List[Union[int, float]]]):
        if isinstance(value, list):
            values = value
            if len(values) == 0:
                raise IndexError('List of RH values  cannot be empty')
        else:
            values = [value]

        if not all(0 <= x <= 1 for x in values):
            raise ValueError('All RH values in the list should be between 0 and 1')
        self.__rh = values

    @property
    def igv(self):
        return self.__igv

    @igv.setter
    def igv(self, value: Union[Union[None, float], List[Union[None, float]]]):
        if isinstance(value, list):
            values = value
        else:
            values = [value]


        self.__igv = values