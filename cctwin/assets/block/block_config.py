from typing import List

from cctwin.assets.block.block_request import BlockBiddingRequest
from cctwin.assets.hrsg.hrsg_constants import HrsgConstants
from cctwin.assets.train.train_request import TrainSimulationRequest
from cctwin.assets.hrsg.duct_burner_mode import DuctBurnerMode



class BlockConfig:
    def __init__(self, name: str,
                 trains: List[TrainSimulationRequest],
                 is_stg_online: bool):
        self.name = name
        self.trains = trains
        self.is_stg_online = is_stg_online

    def update_availability(self, block_bidding_request: BlockBiddingRequest):
        for train_bidding_request in block_bidding_request.trains:
            ctg_name = train_bidding_request.ctg
            train = next((train for train in self.trains if train.ctg == ctg_name), None)
            train.ctg_availability = train_bidding_request.ctg_availability
            train.inlet_conditioner_availability = train_bidding_request.inlet_conditioner_availability
            train.duct_burner_fuel = (train_bidding_request.duct_burner_availability * HrsgConstants.MAX_FUEL)/100
            train.wc_availability = train_bidding_request.wc_availability
            train.pag_availability = train_bidding_request.pag_availability
