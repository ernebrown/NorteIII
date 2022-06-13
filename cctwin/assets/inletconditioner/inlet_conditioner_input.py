from typing import List, Union

from cctwin.assets.inletconditioner.inlet_conditioner_constants import InletConditionerConstants


class InletConditionerInput:
    def __init__(self,
                 avlblty: Union[int, float],
                 db: Union[int, float, List[Union[int, float]]],
                 rh: Union[int, float, List[Union[int, float]]],
                 baro: Union[int, float, List[Union[int, float]]]
                 ):
        self.avlblty = avlblty
        self.db = db
        self.rh = rh
        self.baro = baro

        it = iter([self.db, self.rh, self.baro])
        length = len(next(it))

        if not all(len(l) == length for l in it):
            raise IndexError('Lists of DB, RH and BARO values should be of equal length')

    @property
    def avlblty(self):
        return self.__avlblty

    @avlblty.setter
    def avlblty(self, value: Union[int, float]):
        #if not isinstance(value, (int, float)):
        #    raise TypeError('Inlet conditioner\'s availability should be passed as an integer of float')
        if not InletConditionerConstants.MIN_AVLBLTY <= value <= InletConditionerConstants.MAX_AVLBLTY:
            raise ValueError(f'Inlet conditioner\'s availability should be between '
                             f'{InletConditionerConstants.MIN_AVLBLTY} '
                             f'and {InletConditionerConstants.MAX_AVLBLTY}%')
        self.__avlblty = value

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
    def baro(self):
        return self.__baro

    @baro.setter
    def baro(self, value: Union[Union[int, float], List[Union[int, float]]]):
        if isinstance(value, list):
            values = value
            if len(values) == 0:
                raise IndexError('List of BARO pressure values cannot be empty')
        else:
            values = [value]

        if not all(14 <= x <= 15 for x in values):
            raise ValueError('All BARO pressure values in the list should be between 14 and 15 psia')
        self.__baro = values
