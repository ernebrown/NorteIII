from typing import Union


class PagIncremental:
    def __init__(self,
                 mw: Union[int, float],
                 fuel: Union[int, float],
                 exh_temp: Union[int, float],
                 steam: Union[int, float]
                 ):
        self.mw = mw
        self.fuel = fuel
        self.exh_temp = exh_temp
        self.steam = steam

    @property
    def mw(self):
        return self.__mw

    @mw.setter
    def mw(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('PAG incremental MW should be int or float type')
        if value <= 0:
            raise ValueError('PAG incremental MW should be greater than 0')
        self.__mw = value

    @property
    def fuel(self):
        return self.__fuel

    @fuel.setter
    def fuel(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('PAG incremental FUEL should be int or float type')
        if value <= 0:
            raise ValueError('PAG incremental FUEL should be greater than 0')
        self.__fuel = value

    @property
    def exh_temp(self):
        return self.__exh_temp

    @exh_temp.setter
    def exh_temp(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('PAG incremental EXH_TEMP should be int or float type')
        if value <= 0:
            raise ValueError('PAG incremental EXH_TEMP should be greater than 0')
        self.__exh_temp = value

    @property
    def steam(self):
        return self.__steam

    @steam.setter
    def steam(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('PAG incremental STEAM should be int or float type')
        if value <= 0:
            raise ValueError('PAG incremental STEAM should be greater than 0')
        self.__steam = value


class PeakFireIncremental:
    def __init__(self,
                 mw: Union[int, float],
                 fuel: Union[int, float],
                 exh_temp: Union[int, float]
                 ):
        self.mw = mw
        self.fuel = fuel
        self.exh_temp = exh_temp

    @property
    def mw(self):
        return self.__mw

    @mw.setter
    def mw(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('PEAK-FIRE incremental MW should be int or float type')
        if value <= 0:
            raise ValueError('PEAK-FIRE incremental MW should be greater than 0')
        self.__mw = value

    @property
    def fuel(self):
        return self.__fuel

    @fuel.setter
    def fuel(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('PEAK-FIRE incremental FUEL should be int or float type')
        if value <= 0:
            raise ValueError('PEAK-FIRE incremental FUEL should be greater than 0')
        self.__fuel = value

    @property
    def exh_temp(self):
        return self.__exh_temp

    @exh_temp.setter
    def exh_temp(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('PEAK-FIRE incremental EXH_TEMP should be int or float type')
        if value <= 0:
            raise ValueError('PEAK-FIRE incremental EXH_TEMP should be greater than 0')
        self.__exh_temp = value

class WCIncremental:
    def __init__(self,
                 mw: Union[int, float],
                 fuel: Union[int, float],
                 exh_temp: Union[int, float]
                 ):
        self.mw = mw
        self.fuel = fuel
        self.exh_temp = exh_temp

    @property
    def mw(self):
        return self.__mw

    @mw.setter
    def mw(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('Wet-Compression incremental MW should be int or float type')
        if value <= 0:
            raise ValueError('Wet-Compression incremental MW should be greater than 0')
        self.__mw = value

    @property
    def fuel(self):
        return self.__fuel

    @fuel.setter
    def fuel(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('Wet-Compression incremental FUEL should be int or float type')
        if value <= 0:
            raise ValueError('Wet-Compression incremental FUEL should be greater than 0')
        self.__fuel = value

    @property
    def exh_temp(self):
        return self.__exh_temp

    @exh_temp.setter
    def exh_temp(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError('Wet-Compression incremental EXH_TEMP should be int or float type')
        if value < 0:
            raise ValueError('Wet-Compression incremental EXH_TEMP should be greater than or equal to 0')
        self.__exh_temp = value