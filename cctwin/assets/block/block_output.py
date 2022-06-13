from datetime import datetime

from cctwin.assets.block.ambient_conditions import AmbientConditions, AmbientConditionsSimulationSchema
from cctwin.assets.stg.stg_output import StgBiddingOutputSchema, StgOutput, StgSimulationOutputSchema
from cctwin.assets.train.train_output import TrainBiddingOutputSchema, TrainOutput, TrainSimulationOutputSchema
from cctwin.helper.chart_schemas import *


class BlockSimulationOutput:
    def __init__(self,
                 ambient_conditions: AmbientConditions,
                 net_mw: Union[int, float, List[Union[int, float]]],
                 net_fuel: Union[int, float, List[Union[int, float]]],
                 net_heat_rate: Union[int, float, List[Union[int, float]]],
                 aux_load: Union[int, float, List[Union[int, float]]],
                 train_outputs: List[TrainOutput],
                 stg_output: StgOutput,
                 ):
        self.ambient_conditions = ambient_conditions
        self.net_mw = net_mw
        self.net_fuel = net_fuel
        self.net_heat_rate = net_heat_rate
        self.aux_load = aux_load
        self.train_outputs = train_outputs
        self.stg_output = stg_output
        self.charts = self.get_chart_data()

    def get_chart_data(self):
        from cctwin.twin import block_twin

        ctg8_name = block_twin.trains[0].ctg.name
        ctg8_output = next((train_output.ctg_output for train_output in self.train_outputs if
                            train_output.ctg_output.name == ctg8_name), None)

        ctg9_name = block_twin.trains[1].ctg.name
        ctg9_output = next((train_output.ctg_output for train_output in self.train_outputs if
                            train_output.ctg_output.name == ctg9_name), None)

        site_chart_data = ChartData(title='Site Performance vs. Ambient Dry-Bulb Temperature',
                                    x_axis_data=AxisData(label='Ambient Dry-Bulb Temperature (°F)',
                                                         data=self.ambient_conditions.db[1:]),
                                    y_axis_data=[
                                        AxisData(label='Net Output (MW)', data=self.net_mw[1:]),
                                        AxisData(label='Net Heat Rate (Btu/kWhr)', data=self.net_heat_rate[1:]),
                                    ])

        ctg8_chart_data = ChartData(title=f'{ctg8_name} Performance vs. Ambient Dry-Bulb Temperature',
                                    x_axis_data=AxisData(label='Ambient Dry-Bulb Temperature (°F)',
                                                         data=self.ambient_conditions.db[1:]),
                                    y_axis_data=[
                                        AxisData(label='Compressor Inlet Temperature (°F)',
                                                 data=ctg8_output.cit[1:]),
                                        AxisData(label='Gross Output (MW)', data=ctg8_output.mw[1:]),
                                    ])

        ctg9_chart_data = ChartData(title=f'{ctg9_name} Performance vs. Ambient Dry-Bulb Temperature',
                                    x_axis_data=AxisData(label='Ambient Dry-Bulb Temperature (°F)',
                                                         data=self.ambient_conditions.db[1:]),
                                    y_axis_data=[
                                        AxisData(label='Compressor Inlet Temperature (°F)',
                                                 data=ctg9_output.cit[1:]),
                                        AxisData(label='Gross Output (MW)', data=ctg9_output.mw[1:]),
                                    ])

        stg_chart_data = ChartData(title=f'{self.stg_output.name} Performance vs. Ambient Dry-Bulb Temperature',
                                   x_axis_data=AxisData(label='Ambient Dry-Bulb Temperature (°F)',
                                                        data=self.ambient_conditions.db[1:]),
                                   y_axis_data=[
                                       AxisData(label='Gross Output (MW)', data=self.stg_output.mw[1:]),
                                   ])

        return [site_chart_data, ctg8_chart_data, ctg9_chart_data, stg_chart_data]

    def convert_to_bidding_output(self, config_name: str):
        net_mws = self.net_mw
        net_fuels = self.net_fuel
        net_heat_rates = self.net_heat_rate
        aux_loads = self.aux_load
        train_outputs = self.train_outputs
        stg_outputs = self.stg_output

        block_bidding_output = BlockBiddingOutput(config_name, net_mws, net_fuels,
                                                  net_heat_rates, aux_loads, train_outputs, stg_outputs)

        return block_bidding_output


class BlockBiddingOutput:
    def __init__(self,
                 config_name: str,
                 net_mws: List[Union[int, float]],
                 net_fuels: List[Union[int, float]],
                 net_heat_rates: List[Union[int, float]],
                 aux_loads: List[Union[int, float]],
                 train_outputs: List[TrainOutput],
                 stg_outputs: StgOutput
                 ):
        self.config_name = config_name
        self.net_mws = net_mws
        self.net_fuels = net_fuels
        self.net_heat_rates = net_heat_rates
        self.aux_loads = aux_loads
        self.train_outputs = train_outputs
        self.stg_outputs = stg_outputs


class BlockSimulationOutputSchema(Schema):
    class Meta:
        ordered = True

    ambient_conditions = fields.Nested(AmbientConditionsSimulationSchema())
    net_mw = fields.Method('get_first_net_mw')
    net_fuel = fields.Method('get_first_net_fuel')
    net_heat_rate = fields.Method('get_first_net_heat_rate')
    aux_load = fields.Method('get_first_aux_load')
    trains = fields.Nested(TrainSimulationOutputSchema(), many=True, attribute='train_outputs')
    stg = fields.Nested(StgSimulationOutputSchema(), attribute='stg_output')
    charts = fields.Nested(ChartDataSchema(), many=True)

    @classmethod
    def get_first_net_mw(cls, obj: BlockSimulationOutput):
        if isinstance(obj.net_mw, list):
            return obj.net_mw[0]
        return obj.net_mw

    @classmethod
    def get_first_net_fuel(cls, obj: BlockSimulationOutput):
        if isinstance(obj.net_fuel, list):
            return obj.net_fuel[0]
        return obj.net_fuel

    @classmethod
    def get_first_net_heat_rate(cls, obj: BlockSimulationOutput):
        if isinstance(obj.net_heat_rate, list):
            return obj.net_heat_rate[0]
        return obj.net_heat_rate

    @classmethod
    def get_first_aux_load(cls, obj: BlockSimulationOutput):
        if isinstance(obj.aux_load, list):
            return obj.aux_load[0]
        return obj.aux_load


class BlockBiddingOutputSchema(Schema):
    class Meta:
        ordered = True

    config_name = fields.String()
    net_mws = fields.List(fields.Number())
    net_fuels = fields.List(fields.Number())
    net_heat_rates = fields.List(fields.Number())
    aux_loads = fields.List(fields.Number())
    train_outputs = fields.Nested(TrainBiddingOutputSchema(), many=True)
    stg_outputs = fields.Nested(StgBiddingOutputSchema())
