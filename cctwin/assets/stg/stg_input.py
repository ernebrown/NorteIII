from typing import List

from cctwin.assets.block.ambient_conditions import AmbientConditions
from cctwin.assets.train.train_output import TrainOutput


class StgInput:
    def __init__(self,
                 ambient_conditions: AmbientConditions,
                 train_outputs: List[TrainOutput],
                 site_config: str):
        self.ambient_conditions = ambient_conditions
        self.train_outputs = train_outputs
        self.site_config = site_config

