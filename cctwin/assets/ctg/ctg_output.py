import json
from typing import Union

from marshmallow import Schema, fields, missing, post_dump


class CtgOutput:
    def __init__(self,
                 name: str,
                 cit: list,
                 igv: list,
                 mw: list,
                 fuel: list,
                 cpd: list,
                 ctd: list,
                 exh_temp: list,
                 pag_mw: Union[None, list],
                 pag_fuel: Union[None, list],
                 pag_exh_temp: Union[None, list],
                 pag_steam: Union[None, list],
                 peak_fire_mw: Union[None, list],
                 peak_fire_fuel: Union[None, list],
                 peak_fire_exh_temp: Union[None, list],
                 wc_mw: Union[None, list],
                 wc_fuel: Union[None, list],
                 wc_exh_temp: Union[None, list]
                 ):

        if not isinstance(name, str):
            raise TypeError('NAME should be a string representing CTG\'s name')

        if not isinstance(cit, list):
            raise TypeError('CIT should be a list of values')

        if not isinstance(mw, list):
            raise TypeError('MW should be a list of values')

        if not isinstance(fuel, list):
            raise TypeError('FUEL should be a list of values')

        if not isinstance(igv, list):
            raise TypeError('IGV should be a list of values')

        if not isinstance(cpd, list):
            raise TypeError('CPD should be a list of values')

        if not isinstance(ctd, list):
            raise TypeError('CTD should be a list of values')

        if not isinstance(exh_temp, list):
            raise TypeError('EXH_TEMP should be a list of values')

        self.name = name
        self.cit = cit
        self.mw = mw
        self.fuel = fuel
        self.igv = igv
        self.cpd = cpd
        self.ctd = ctd
        self.exh_temp = exh_temp

        self.pag_mw = pag_mw
        self.pag_fuel = pag_fuel
        self.pag_exh_temp = pag_exh_temp
        self.pag_steam = pag_steam
        self.peak_fire_mw = peak_fire_mw
        self.peak_fire_fuel = peak_fire_fuel
        self.peak_fire_exh_temp = peak_fire_exh_temp
        self.wc_mw = wc_mw
        self.wc_fuel = wc_fuel
        self.wc_exh_temp = wc_exh_temp

    def to_dict(self):
        data = {
            'mw': self.mw,
            'fuel': self.fuel,
            'igv': self.igv,
            'cpd': self.cpd,
            'ctd': self.ctd,
            'exh_temp': self.exh_temp,
            'pag_mw': self.pag_mw,
            'pag_fuel': self.pag_fuel,
            'pag_exh_temp': self.pag_exh_temp,
            'pag_steam': self.pag_steam,
            'peak_fire_mw': self.peak_fire_mw,
            'peak_fire_fuel': self.peak_fire_fuel,
            'peak_fire_exh_temp': self.peak_fire_exh_temp,
            'wc_mw': self.wc_mw,
            'wc_fuel': self.wc_fuel,
            'wc_exh_temp': self.wc_exh_temp
        }
        return data

    def to_json(self):
        data = self.to_dict()
        return json.dumps(data)


class BaseSchema(Schema):
    def on_bind_field(self, field_name, field_obj):
        # Override default missing attribute so
        # that missing values deserialize to None
        if field_obj.missing == missing:
            field_obj.missing = None
            field_obj.allow_none = True

    @post_dump
    def clean_missing(self, data, **kwargs):
        ret = data.copy()
        for key in filter(lambda key: data[key] is None, data):
            del ret[key]
        return ret


class CtgSimulationOutputSchema(BaseSchema):
    class Meta:
        ordered = True

    name = fields.String()
    mw = fields.Method('get_first_mw')
    fuel = fields.Method('get_first_fuel')
    cpd = fields.Method('get_first_cpd')
    ctd = fields.Method('get_first_ctd')
    exh_temp = fields.Method('get_first_exh_temp')
    pag_mw = fields.Method('get_first_pag_mw')
    pag_fuel = fields.Method('get_first_pag_fuel')
    pag_exh_temp = fields.Method('get_first_pag_exh_temp')
    pag_steam = fields.Method('get_first_pag_steam')
    peak_fire_mw = fields.Method('get_first_peak_fire_mw')
    peak_fire_fuel = fields.Method('get_first_peak_fire_fuel')
    peak_fire_exh_temp = fields.Method('get_first_peak_fire_exh_temp')
    wc_mw = fields.Method('get_first_wc_mw')
    wc_fuel = fields.Method('get_first_wc_fuel')
    wc_exh_temp = fields.Method('get_first_wc_exh_temp')

    @classmethod
    def get_first_mw(cls, obj: CtgOutput):
        return obj.mw[0]

    @classmethod
    def get_first_fuel(cls, obj: CtgOutput):
        return obj.fuel[0]

    @classmethod
    def get_first_cpd(cls, obj: CtgOutput):
        return obj.cpd[0]

    @classmethod
    def get_first_ctd(cls, obj: CtgOutput):
        return obj.ctd[0]

    @classmethod
    def get_first_exh_temp(cls, obj: CtgOutput):
        return obj.exh_temp[0]

    @classmethod
    def get_first_pag_mw(cls, obj: CtgOutput):
        if obj.pag_mw:
            return obj.pag_mw[0]
        return None

    @classmethod
    def get_first_pag_fuel(cls, obj: CtgOutput):
        if obj.pag_fuel:
            return obj.pag_fuel[0]
        return None

    @classmethod
    def get_first_pag_exh_temp(cls, obj: CtgOutput):
        if obj.pag_exh_temp:
            return obj.pag_exh_temp[0]
        return None

    @classmethod
    def get_first_pag_steam(cls, obj: CtgOutput):
        if obj.pag_steam:
            return obj.pag_steam[0]
        return None

    @classmethod
    def get_first_peak_fire_mw(cls, obj: CtgOutput):
        if obj.peak_fire_mw:
            return obj.peak_fire_mw[0]
        return None

    @classmethod
    def get_first_peak_fire_fuel(cls, obj: CtgOutput):
        if obj.peak_fire_fuel:
            return obj.peak_fire_fuel[0]
        return None

    @classmethod
    def get_first_peak_fire_exh_temp(cls, obj: CtgOutput):
        if obj.peak_fire_exh_temp:
            return obj.peak_fire_exh_temp[0]
        return None

    @classmethod
    def get_first_wc_mw(cls, obj: CtgOutput):
        if obj.wc_mw:
            return obj.wc_mw[0]
        return None

    @classmethod
    def get_first_wc_fuel(cls, obj: CtgOutput):
        if obj.wc_fuel:
            return obj.wc_fuel[0]
        return None

    @classmethod
    def get_first_wc_exh_temp(cls, obj: CtgOutput):
        if obj.wc_exh_temp:
            return obj.wc_exh_temp[0]
        return None

class CtgBiddingOutputSchema(BaseSchema):
    class Meta:
        ordered = True

    name = fields.String()
    mw = fields.List(fields.Number())
    fuel = fields.List(fields.Number())
    cpd = fields.List(fields.Number())
    ctd = fields.List(fields.Number())
    exh_temp = fields.List(fields.Number())
    pag_mw = fields.List(fields.Number())
    pag_fuel = fields.List(fields.Number())
    pag_exh_temp = fields.List(fields.Number())
    pag_steam = fields.List(fields.Number())
    peak_fire_mw = fields.List(fields.Number())
    peak_fire_fuel = fields.List(fields.Number())
    peak_fire_exh_temp = fields.List(fields.Number())
    wc_mw = fields.List(fields.Number())
    wc_fuel = fields.List(fields.Number())
    wc_exh_temp = fields.List(fields.Number())
