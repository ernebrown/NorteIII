from datetime import datetime
from typing import List

from marshmallow import Schema, fields, post_load

from cctwin.assets.block.ambient_conditions import AmbientConditions, AmbientConditionsSimulationSchema
from cctwin.assets.train.train_request import TrainBiddingRequest, TrainBiddingRequestSchema, TrainSimulationRequest, \
    TrainSimulationRequestSchema


class BlockSimulationRequest:
    def __init__(self,
                 ambient_conditions: AmbientConditions,
                 trains: List[TrainSimulationRequest],
                 is_stg_online: bool
                 ):
        self.ambient_conditions = ambient_conditions
        self.trains = trains
        self.is_stg_online = is_stg_online


class BlockBiddingRequest:
    def __init__(self,
                 times: List[datetime],
                 ambient_conditions: AmbientConditions,
                 trains: List[TrainBiddingRequest],
                 is_stg_online: bool
                 ):
        self.times = times
        self.ambient_conditions = ambient_conditions
        self.trains = trains
        self.is_stg_online = is_stg_online


class BlockSimulationRequestSchema(Schema):
    class Meta:
        ordered = True

    ambient_conditions = fields.Nested(AmbientConditionsSimulationSchema())
    trains = fields.Nested(TrainSimulationRequestSchema, many=True)
    is_stg_online = fields.Boolean()

    @post_load
    def create_block_request(self, data, **kwargs):
        return BlockSimulationRequest(**data)


class BlockBiddingRequestSchema(Schema):
    class Meta:
        ordered = True

    times = fields.List(fields.DateTime())
    ambient_conditions = fields.Nested(AmbientConditionsSimulationSchema())
    trains = fields.Nested(TrainBiddingRequestSchema, many=True)
    is_stg_online = fields.Boolean()

    @post_load
    def create_block_bidding_request(self, data, **kwargs):
        return BlockBiddingRequest(**data)
