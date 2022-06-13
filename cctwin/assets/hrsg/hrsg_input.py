from typing import List, Union

from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.ctg.ctg_input import CtgInput
from cctwin.assets.hrsg.hrsg_constants import HrsgConstants


class HrsgInput:
    def __init__(self,
                 ctg_mode: CtgOperationMode,
                 ctg_avail: CtgInput.ctg_avlblty,
                 ctg_mw: Union[int, float, List[Union[int, float]]],
                 ctg_exh_temp: Union[int, float, List[Union[int, float]]],
                 db_fuel: Union[int, float, List[Union[int, float]]]
                 ):
        self.ctg_mode = ctg_mode
        self.ctg_avail = ctg_avail
        self.ctg_mw = ctg_mw
        self.ctg_exh_temp = ctg_exh_temp
        self.db_fuel = db_fuel

        it = iter([self.ctg_mw, self.ctg_exh_temp, self.db_fuel])
        length = len(next(it))

        if not all(len(l) == length for l in it):
            raise IndexError('Lists of CTG MW, CTG Fuel,  CTG EXH TEMP and DB FUEL values should be of equal length')

    @property
    def ctg_mw(self):
        return self.__gt_mw

    @ctg_mw.setter
    def ctg_mw(self, value: Union[Union[int, float], List[Union[int, float]]]):
        if isinstance(value, list):
            values = value
            if len(values) == 0:
                raise IndexError('List of CTG MW values  cannot be empty')
        else:
            values = [value]

        if not all(x >= 0 for x in values):
            raise ValueError('All CTG MW values in the list should be greater than equal to 0')
        self.__gt_mw = values

    @property
    def ctg_exh_temp(self):
        return self.__gt_exh_temp

    @ctg_exh_temp.setter
    def ctg_exh_temp(self, value: Union[Union[int, float], List[Union[int, float]]]):
        if isinstance(value, list):
            values = value
            if len(values) == 0:
                raise IndexError('List of CTG EXH TEMP values  cannot be empty')
        else:
            values = [value]

        if not all(x >= 0 for x in values):
            raise ValueError('All CTG EXH TEMP values in the list should be greater than equal to 0')
        self.__gt_exh_temp = values

    @property
    def db_fuel(self):
        return self.__db_fuel

    @db_fuel.setter
    def db_fuel(self, value: Union[Union[int, float], List[Union[int, float]]]):
        if isinstance(value, list):
            values = value
            if len(values) == 0:
                raise IndexError('List of DB FUEL values  cannot be empty')
        else:
            values = [value]

        if not all(0 <= x <= HrsgConstants.MAX_FUEL for x in values):
            raise ValueError('All DB FUEL values in the list should be between 0 and Max fuel')
        self.__db_fuel = values
