from marshmallow import Schema, fields


class HrsgOutput:
    def __init__(self,
                 duct_burner_fuel,
                 hp_flow,
                 hp_press,
                 hp_temp,
                 hp_sh_temp,
                 hrh_flow,
                 hrh_press,
                 hrh_temp,
                 lp_flow,
                 lp_press,
                 lp_temp):
        self.duct_burner_fuel = duct_burner_fuel
        self.hp_flow = hp_flow
        self.hp_press = hp_press
        self.hp_temp = hp_temp
        self.hp_sh_temp = hp_sh_temp
        self.hrh_flow = hrh_flow
        self.hrh_press = hrh_press
        self.hrh_temp = hrh_temp
        self.lp_flow = lp_flow
        self.lp_press = lp_press
        self.lp_temp = lp_temp


class HrsgSimulationOutputSchema(Schema):
    class Meta:
        ordered = True

    duct_burner_fuel = fields.Method('get_first_duct_burner_fuel')
    hp_flow = fields.Method('get_first_hp_flow')
    hp_press = fields.Method('get_first_hp_press')
    hp_temp = fields.Method('get_first_hp_temp')
    hp_sh_temp = fields.Method('get_first_hp_sh_temp')
    hrh_flow = fields.Method('get_first_hrh_flow')
    hrh_press = fields.Method('get_first_hrh_press')
    hrh_temp = fields.Method('get_first_hrh_temp')
    lp_flow = fields.Method('get_first_lp_flow')
    lp_press = fields.Method('get_first_lp_press')
    lp_temp = fields.Method('get_first_lp_temp')

    @classmethod
    def get_first_duct_burner_fuel(cls, obj: HrsgOutput):
        if obj.duct_burner_fuel:
            return obj.duct_burner_fuel[0]
        return None

    @classmethod
    def get_first_hp_flow(cls, obj: HrsgOutput):
        if obj.hp_flow:
            return obj.hp_flow[0]
        return None

    @classmethod
    def get_first_hp_press(cls, obj: HrsgOutput):
        if obj.hp_press:
            return obj.hp_press[0]
        return None

    @classmethod
    def get_first_hp_temp(cls, obj: HrsgOutput):
        if obj.hp_temp:
            return obj.hp_temp[0]
        return None

    @classmethod
    def get_first_hp_sh_temp(cls, obj: HrsgOutput):
        if obj.hp_sh_temp:
            return obj.hp_sh_temp[0]
        return None

    @classmethod
    def get_first_hrh_flow(cls, obj: HrsgOutput):
        if obj.hrh_flow:
            return obj.hrh_flow[0]
        return None

    @classmethod
    def get_first_hrh_press(cls, obj: HrsgOutput):
        if obj.hrh_press:
            return obj.hrh_press[0]
        return None

    @classmethod
    def get_first_hrh_temp(cls, obj: HrsgOutput):
        if obj.hrh_temp:
            return obj.hrh_temp[0]
        return None

    @classmethod
    def get_first_lp_flow(cls, obj: HrsgOutput):
        if obj.lp_flow:
            return obj.lp_flow[0]
        return None

    @classmethod
    def get_first_lp_press(cls, obj: HrsgOutput):
        if obj.lp_press:
            return obj.lp_press[0]
        return None

    @classmethod
    def get_first_lp_temp(cls, obj: HrsgOutput):
        if obj.lp_temp:
            return obj.lp_temp[0]
        return None


class HrsgBiddingOutputSchema(Schema):
    class Meta:
        ordered = True

    duct_burner_fuel = fields.List(fields.Number())
    hp_flow = fields.List(fields.Number())
    hp_press = fields.List(fields.Number())
    hp_temp = fields.List(fields.Number())
    hp_sh_temp = fields.List(fields.Number())
    hrh_flow = fields.List(fields.Number())
    hrh_press = fields.List(fields.Number())
    hrh_temp = fields.List(fields.Number())
    lp_flow = fields.List(fields.Number())
    lp_press = fields.List(fields.Number())
    lp_temp = fields.List(fields.Number())
