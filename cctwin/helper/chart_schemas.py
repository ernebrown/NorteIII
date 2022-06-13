from typing import List, Union

from marshmallow import Schema, fields


class AxisData:
    def __init__(self, label: str,
                 data: List[Union[int, float]]):
        self.label = label
        self.data = data


class AxisDataSchema(Schema):
    class Meta:
        ordered = True

    label = fields.String()
    data = fields.List(fields.Number())


class ChartData:
    def __init__(self, title: str,
                 x_axis_data: AxisData,
                 y_axis_data: List[AxisData]):
        self.title = title
        self.x_axis_data = x_axis_data
        self.y_axis_data = y_axis_data


class ChartDataSchema(Schema):
    class Meta:
        ordered = True

    title = fields.String()
    x_axis_data = fields.Nested(AxisDataSchema(), many=False)
    y_axis_data = fields.Nested(AxisDataSchema(), many=True)
