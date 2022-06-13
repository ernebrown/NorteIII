from typing import Dict, List, Union

import numpy as np
import pandas as pd
from marshmallow import Schema, fields

from cctwin.assets.block.block_config import BlockConfig
from cctwin.assets.block.block_constants import BlockConstants
from cctwin.assets.block.block_output import BlockBiddingOutput, BlockSimulationOutput
from cctwin.assets.block.block_request import BlockBiddingRequest, BlockSimulationRequest
from cctwin.assets.ctg.ctg_constants import CtgConstants
from cctwin.assets.ctg.ctg_input import CtgInput
from cctwin.assets.ctg.ctg_operation_mode import CtgOperationMode
from cctwin.assets.hrsg.duct_burner_mode import DuctBurnerMode
from cctwin.assets.hrsg.hrsg_constants import HrsgConstants
from cctwin.assets.hrsg.hrsg_input import HrsgInput
from cctwin.assets.inletconditioner.inlet_conditioner_input import InletConditionerInput
from cctwin.assets.inletconditioner.inlet_conditioner_input import InletConditionerConstants
from cctwin.assets.stg.stg import SteamTurbine
from cctwin.assets.stg.stg_input import StgInput
from cctwin.assets.stg.stg_output import StgOutput
from cctwin.assets.train.train import Train, TrainBiddingSchema, TrainSimulationSchema
from cctwin.assets.train.train_output import TrainOutput
from cctwin.assets.train.train_request import TrainSimulationRequest, TrainBiddingRequest
from cctwin.helper.asset_model_executor import ModelExecutor


class Block:
    def __init__(self,
                 name: str,
                 trains: List[Train],
                 stg: SteamTurbine,
                 aux_load_model_dict: dict,
                 config_mode: list,
                 config_type: list,
                 LSLMODE: bool,
                 LSL1x1: Union[int, float],
                 LSL2x1: Union[int, float]):
        self.name = name
        self.trains = trains
        self.stg = stg
        self.aux_load_model_executor = ModelExecutor(aux_load_model_dict)
        self.config_mode = config_mode
        self.config_type = config_type
        self.LSLMODE = LSLMODE
        self.LSL1x1 = LSL1x1
        self.LSL2x1 = LSL2x1


    def create_block_configs(self) -> Dict[str, BlockConfig]:
        config_1 = BlockConfig(name='1x1 A Min',
                               trains=[TrainSimulationRequest(ctg=self.trains[0].ctg.name,
                                                              ctg_mode=CtgOperationMode.MINLOAD,
                                                              ctg_availability=100,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv= CtgConstants.BASE_IGV),
                                       TrainSimulationRequest(ctg=self.trains[1].ctg.name,
                                                              ctg_mode=CtgOperationMode.OFFLINE,
                                                              ctg_availability=0,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              )],
                               is_stg_online=True)

        config_2 = BlockConfig(name='1x1 A Base',
                               trains=[TrainSimulationRequest(ctg=self.trains[0].ctg.name,
                                                              ctg_mode=CtgOperationMode.AGCLOAD,
                                                              ctg_availability=100,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              ),
                                       TrainSimulationRequest(ctg=self.trains[1].ctg.name,
                                                              ctg_mode=CtgOperationMode.OFFLINE,
                                                              ctg_availability=0,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              )],
                               is_stg_online=True)

        config_3 = BlockConfig(name='1x1 A Base + DB',
                               trains=[TrainSimulationRequest(ctg=self.trains[0].ctg.name,
                                                              ctg_mode=CtgOperationMode.BASELOAD,
                                                              ctg_availability=100,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=
                                                              InletConditionerConstants.TON_DEFAULT,
                                                              duct_burner_mode=DuctBurnerMode.FUEL,
                                                              duct_burner_fuel=HrsgConstants.MAX_FUEL,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              ),
                                       TrainSimulationRequest(ctg=self.trains[1].ctg.name,
                                                              ctg_mode=CtgOperationMode.OFFLINE,
                                                              ctg_availability=0,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              )],
                               is_stg_online=True)

        config_4 = BlockConfig(name='1x1 A Base + Chiller + DB',
                               trains=[TrainSimulationRequest(ctg=self.trains[0].ctg.name,
                                                              ctg_mode=CtgOperationMode.BASELOAD,
                                                              ctg_availability=100,
                                                              is_inlet_conditioner_on=True,
                                                              inlet_conditioner_availability=
                                                              InletConditionerConstants.TON_DEFAULT,
                                                              duct_burner_mode=DuctBurnerMode.FUEL,
                                                              duct_burner_fuel=HrsgConstants.MAX_FUEL,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv= CtgConstants.BASE_IGV),
                                       TrainSimulationRequest(ctg=self.trains[1].ctg.name,
                                                              ctg_mode=CtgOperationMode.OFFLINE,
                                                              ctg_availability=0,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              )],
                               is_stg_online=True)

        config_5 = BlockConfig(name='1x1 B Min',
                               trains=[TrainSimulationRequest(ctg=self.trains[0].ctg.name,
                                                              ctg_mode=CtgOperationMode.OFFLINE,
                                                              ctg_availability=0,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              ),
                                       TrainSimulationRequest(ctg=self.trains[1].ctg.name,
                                                              ctg_mode=CtgOperationMode.MINLOAD,
                                                              ctg_availability=100,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              )],
                               is_stg_online=True)

        config_6 = BlockConfig(name='1x1 B Base',
                               trains=[TrainSimulationRequest(ctg=self.trains[0].ctg.name,
                                                              ctg_mode=CtgOperationMode.OFFLINE,
                                                              ctg_availability=0,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv= CtgConstants.BASE_IGV),
                                       TrainSimulationRequest(ctg=self.trains[1].ctg.name,
                                                              ctg_mode=CtgOperationMode.AGCLOAD,
                                                              ctg_availability=100,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              )],
                               is_stg_online=True)

        config_7 = BlockConfig(name='1x1 B Base + DB',
                               trains=[TrainSimulationRequest(ctg=self.trains[0].ctg.name,
                                                              ctg_mode=CtgOperationMode.OFFLINE,
                                                              ctg_availability=0,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              ),
                                       TrainSimulationRequest(ctg=self.trains[1].ctg.name,
                                                              ctg_mode=CtgOperationMode.BASELOAD,
                                                              ctg_availability=100,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=
                                                              InletConditionerConstants.TON_DEFAULT,
                                                              duct_burner_mode=DuctBurnerMode.FUEL,
                                                              duct_burner_fuel=HrsgConstants.MAX_FUEL,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              )],
                               is_stg_online=True)

        config_8 = BlockConfig(name='1x1 B Base + Chiller + DB',
                               trains=[TrainSimulationRequest(ctg=self.trains[0].ctg.name,
                                                              ctg_mode=CtgOperationMode.OFFLINE,
                                                              ctg_availability=0,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              ),
                                       TrainSimulationRequest(ctg=self.trains[1].ctg.name,
                                                              ctg_mode=CtgOperationMode.BASELOAD,
                                                              ctg_availability=100,
                                                              is_inlet_conditioner_on=True,
                                                              inlet_conditioner_availability=
                                                              InletConditionerConstants.TON_DEFAULT,
                                                              duct_burner_mode=DuctBurnerMode.FUEL,
                                                              duct_burner_fuel=HrsgConstants.MAX_FUEL,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              )],
                               is_stg_online=True)

        config_9 = BlockConfig(name='2x1 Min',
                               trains=[TrainSimulationRequest(ctg=self.trains[0].ctg.name,
                                                              ctg_mode=CtgOperationMode.MINLOAD,
                                                              ctg_availability=100,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              ),
                                       TrainSimulationRequest(ctg=self.trains[1].ctg.name,
                                                              ctg_mode=CtgOperationMode.MINLOAD,
                                                              ctg_availability=100,
                                                              is_inlet_conditioner_on=False,
                                                              inlet_conditioner_availability=0,
                                                              duct_burner_mode=DuctBurnerMode.OFF,
                                                              duct_burner_fuel=0,
                                                              is_pag_on=False,
                                                              pag_availability=0,
                                                              is_peak_fire_on=False,
                                                              is_wc_on=False,
                                                              wc_availability=0,
                                                              igv_input=True,
                                                              igv=CtgConstants.BASE_IGV
                                                              )],
                               is_stg_online=True)

        config_10 = BlockConfig(name='2x1 Base',
                                trains=[TrainSimulationRequest(ctg=self.trains[0].ctg.name,
                                                               ctg_mode=CtgOperationMode.AGCLOAD,
                                                               ctg_availability=100,
                                                               is_inlet_conditioner_on=False,
                                                               inlet_conditioner_availability=0,
                                                               duct_burner_mode=DuctBurnerMode.OFF,
                                                               duct_burner_fuel=0,
                                                               is_pag_on=False,
                                                               pag_availability=0,
                                                               is_peak_fire_on=False,
                                                               is_wc_on=False,
                                                               wc_availability=0,
                                                               igv_input=True,
                                                               igv=CtgConstants.BASE_IGV
                                                               ),
                                        TrainSimulationRequest(ctg=self.trains[1].ctg.name,
                                                               ctg_mode=CtgOperationMode.AGCLOAD,
                                                               ctg_availability=100,
                                                               is_inlet_conditioner_on=False,
                                                               inlet_conditioner_availability=0,
                                                               duct_burner_mode=DuctBurnerMode.OFF,
                                                               duct_burner_fuel=0,
                                                               is_pag_on=False,
                                                               pag_availability=0,
                                                               is_peak_fire_on=False,
                                                               is_wc_on=False,
                                                               wc_availability=0,
                                                               igv_input=True,
                                                               igv=CtgConstants.BASE_IGV
                                                               )],
                                is_stg_online=True)

        config_11 = BlockConfig(name='2x1 Base + DB',
                                trains=[TrainSimulationRequest(ctg=self.trains[0].ctg.name,
                                                               ctg_mode=CtgOperationMode.BASELOAD,
                                                               ctg_availability=100,
                                                               is_inlet_conditioner_on=False,
                                                               inlet_conditioner_availability=0,
                                                               duct_burner_mode=DuctBurnerMode.FUEL,
                                                               duct_burner_fuel=HrsgConstants.MAX_FUEL,
                                                               is_pag_on=False,
                                                               pag_availability=0,
                                                               is_peak_fire_on=False,
                                                               is_wc_on=False,
                                                               wc_availability=0,
                                                               igv_input=True,
                                                               igv=CtgConstants.BASE_IGV
                                                               ),
                                        TrainSimulationRequest(ctg=self.trains[1].ctg.name,
                                                               ctg_mode=CtgOperationMode.BASELOAD,
                                                               ctg_availability=100,
                                                               is_inlet_conditioner_on=False,
                                                               inlet_conditioner_availability=
                                                               InletConditionerConstants.TON_DEFAULT,
                                                               duct_burner_mode=DuctBurnerMode.FUEL,
                                                               duct_burner_fuel=HrsgConstants.MAX_FUEL,
                                                               is_pag_on=False,
                                                               pag_availability=0,
                                                               is_peak_fire_on=False,
                                                               is_wc_on=False,
                                                               wc_availability=0,
                                                               igv_input=True,
                                                               igv=CtgConstants.BASE_IGV
                                                               )],
                                is_stg_online=True)

        config_12 = BlockConfig(name='2x1 Base + Chiller + DB',
                                trains=[TrainSimulationRequest(ctg=self.trains[0].ctg.name,
                                                               ctg_mode=CtgOperationMode.BASELOAD,
                                                               ctg_availability=100,
                                                               is_inlet_conditioner_on=True,
                                                               inlet_conditioner_availability=100,
                                                               duct_burner_mode=DuctBurnerMode.FUEL,
                                                               duct_burner_fuel=HrsgConstants.MAX_FUEL,
                                                               is_pag_on=False,
                                                               pag_availability=0,
                                                               is_peak_fire_on=False,
                                                               is_wc_on=False,
                                                               wc_availability=0,
                                                               igv_input=True,
                                                               igv=CtgConstants.BASE_IGV
                                                               ),
                                        TrainSimulationRequest(ctg=self.trains[1].ctg.name,
                                                               ctg_mode=CtgOperationMode.BASELOAD,
                                                               ctg_availability=100,
                                                               is_inlet_conditioner_on=True,
                                                               inlet_conditioner_availability=
                                                               InletConditionerConstants.TON_DEFAULT,
                                                               duct_burner_mode=DuctBurnerMode.FUEL,
                                                               duct_burner_fuel=HrsgConstants.MAX_FUEL,
                                                               is_pag_on=False,
                                                               pag_availability=0,
                                                               is_peak_fire_on=False,
                                                               is_wc_on=False,
                                                               wc_availability=0,
                                                               igv_input=True,
                                                               igv=CtgConstants.BASE_IGV
                                                               )],
                                is_stg_online=True)
        return {config_1.name: config_1,
                config_2.name: config_2,
                config_3.name: config_3,
                config_4.name: config_4,
                config_5.name: config_5,
                config_6.name: config_6,
                config_7.name: config_7,
                config_8.name: config_8,
                config_9.name: config_9,
                config_10.name: config_10,
                config_11.name: config_11,
                config_12.name: config_12,
                }

    def get_performance(self, block_simulation_request: BlockSimulationRequest):

        num_ctgs_online = sum(
            [1 if (train.ctg_mode != CtgOperationMode.OFFLINE.value and train.ctg_availability != 0.0)
             else 0 for train in block_simulation_request.trains])
        num_stgs_online = 1 if block_simulation_request.is_stg_online else 0
        site_config = f'{num_ctgs_online}X{num_stgs_online}'

        train_outputs = []
        ctg_outputs = []
        hrsg_inputs = []
        hrsg_outputs = []
        inlet_conditioner_outputs = []

        for train_request in block_simulation_request.trains:
            ctg_name = train_request.ctg
            train = next((train for train in self.trains if train.ctg.name == ctg_name), None)

            if train:
                ctg = train.ctg
                hrsg = train.hrsg

                # Update inlet_conditioner_availability, WC, pag and peak_fire based on ctg_mode and ctg_availability
                if train_request.ctg_mode == CtgOperationMode.BASELOAD.value:
                    train_request.igv_input = False

                    if not train_request.is_inlet_conditioner_on:
                        train_request.inlet_conditioner_availability = 0.0
                        train_request.igv = None

                    elif train_request.ctg_availability < CtgConstants.MIN_BASE_LOAD_THRESHOLD:
                        train_request.inlet_conditioner_availability = 0.0
                        train_request.is_pag_on = False
                        train_request.is_peak_fire_on = False
                        train_request.is_wc_on = False
                        train_request.igv = None

                elif train_request.ctg_mode == CtgOperationMode.PARTLOAD.value:
                    train_request.inlet_conditioner_availability = 0.0
                    train_request.igv_input = True
                    train_request.is_pag_on = False
                    train_request.is_wc_on = False
                    train_request.is_peak_fire_on = False

                else:
                    train_request.inlet_conditioner_availability = 0.0
                    train_request.is_pag_on = False
                    train_request.is_peak_fire_on = False
                    train_request.igv_input = False
                    train_request.is_wc_on = False
                    train_request.igv = None

                inlet_conditioner = ctg.inlet_conditioner
                inlet_conditioner_input = InletConditionerInput(avlblty=train_request.inlet_conditioner_availability,
                                                                db=block_simulation_request.ambient_conditions.db,
                                                                rh=block_simulation_request.ambient_conditions.rh,
                                                                baro=block_simulation_request.ambient_conditions.baro)
                inlet_conditioner_output = \
                    inlet_conditioner.get_performance(inlet_conditioner_input=inlet_conditioner_input)
                inlet_conditioner_outputs.append(inlet_conditioner_output)

                pag_availability = train_request.pag_availability if train_request.is_pag_on else 0.0
                wc_availability = train_request.wc_availability if train_request.is_wc_on else 0.0
                ctg_input = CtgInput(ctg_operation_mode=train_request.ctg_mode,
                                     site_config=site_config, ctg_avlblty=train_request.ctg_availability,
                                     pag_avlblty=pag_availability,
                                     wc_avlblty=wc_availability,
                                     is_peak_fire_on=train_request.is_peak_fire_on,
                                     cit=inlet_conditioner_output.cit,
                                     baro=block_simulation_request.ambient_conditions.baro,
                                     db=block_simulation_request.ambient_conditions.db,
                                     rh=block_simulation_request.ambient_conditions.rh,
                                     igv_input=train_request.igv_input,
                                     igv=train_request.igv)
                ctg_output = ctg.get_performance(ctg_input=ctg_input)
                ctg_outputs.append(ctg_output)

                # Turn off duct-burners if CTG is Offline
                if train_request.ctg_mode == CtgOperationMode.OFFLINE.value:
                    db_fuel = 0.0
                elif train_request.duct_burner_mode == DuctBurnerMode.FUEL.value:
                    db_fuel = train_request.duct_burner_fuel
                elif train_request.duct_burner_mode == DuctBurnerMode.MAX.value:
                    db_fuel = HrsgConstants.MAX_FUEL
                else:
                    db_fuel = 0.0

                db_fuel = [db_fuel for _ in ctg_output.mw]

                hrsg_input = HrsgInput(ctg_mode=train_request.ctg_mode,
                                       ctg_avail=train_request.ctg_availability,
                                       ctg_mw=ctg_output.mw,
                                       ctg_exh_temp=ctg_output.exh_temp,
                                       db_fuel=db_fuel)
                hrsg_inputs.append(hrsg_input)
                hrsg_output = hrsg.get_performance(hrsg_input=hrsg_input, stg_fdbk=None)
                hrsg_outputs.append(hrsg_output)

                train_output = TrainOutput(inlet_conditioner_output, ctg_output, hrsg_output)
                train_outputs.append(train_output)

        stg_input = StgInput(block_simulation_request.ambient_conditions, train_outputs, site_config=site_config)
        stg_output = self.stg.get_performance(stg_input)

        if stg_output.train_hp:
            for i, train_request in enumerate(ctg_outputs):
                hrsg_new_input = hrsg_inputs[i]
                hrsg_new_output = self.trains[i].hrsg.get_performance(hrsg_input=hrsg_new_input, stg_fdbk=stg_output)
                train_new_output = TrainOutput(inlet_conditioner_outputs[i], ctg_outputs[i], hrsg_new_output)
                train_outputs.append(train_new_output)
                train_outputs.pop(0)

        block_gross_mw = [0.0 for _ in block_simulation_request.ambient_conditions.db]
        block_fuel = [0.0 for _ in block_simulation_request.ambient_conditions.db]
        block_load = [0.0 for _ in block_simulation_request.ambient_conditions.db]

        df = pd.DataFrame()

        for train_output in train_outputs:
            ctg_mw = train_output.ctg_output.mw
            ctg_name = ''.join(c.lower() for c in train_output.ctg_output.name if c.isalnum())
            df.loc[:, f'{ctg_name}_mw'] = ctg_mw
            block_gross_mw = np.add(block_gross_mw, ctg_mw)
            block_fuel = np.add(block_fuel, train_output.ctg_output.fuel)
            block_fuel = np.add(block_fuel, train_output.hrsg_output.duct_burner_fuel)
            if train_output.inlet_conditioner_output.load == None:
                train_output.inlet_conditioner_output.load = 0.0
            block_load = np.add(block_load, train_output.inlet_conditioner_output.load)

        stg_name = ''.join(c.lower() for c in stg_output.name if c.isalnum())
        df.loc[:, f'{stg_name}_mw'] = stg_output.mw
        block_gross_mw = np.add(block_gross_mw, stg_output.mw)

        if '0x' in site_config.lower():
            aux_load = [0.0 for _ in block_simulation_request.ambient_conditions.db]

        else:

            aux_load_model_key = next((model_key for model_key in self.aux_load_model_executor.model_dict.keys() if
                                   model_key.lower().startswith(site_config.lower())), None)
            if aux_load_model_key is None:
                raise ValueError(f'Could not find a model of aux_load for {site_config} configuration')

            df = self.aux_load_model_executor.append_predictions(model_key=aux_load_model_key, df=df,
                                                             custom_output_names=None)
            aux_load = list(df.aux_load)



        block_load = np.add(block_load, aux_load)

        block_net_mw = block_gross_mw - block_load

        if '0x' in site_config.lower():
            block_heat_rate = block_fuel
        else:
            block_heat_rate = block_fuel / block_net_mw * 1000

        block_output = BlockSimulationOutput(ambient_conditions=block_simulation_request.ambient_conditions,
                                             net_mw=list(block_net_mw), net_fuel=list(block_fuel),
                                             net_heat_rate=list(block_heat_rate), aux_load=list(block_load),
                                             train_outputs=train_outputs, stg_output=stg_output)

        return block_output

    def get_data_for_bids(self,
                          block_configs: Dict[str, BlockConfig],
                          bidding_request: BlockBiddingRequest) -> List[BlockBiddingOutput]:
        dict_block_simulation_requests = {}
        for config_name, config in block_configs.items():
            config.update_availability(bidding_request)
            dict_block_simulation_requests[config_name] = BlockSimulationRequest(bidding_request.ambient_conditions,
                                                                                 config.trains,
                                                                                 config.is_stg_online)

        block_bidding_outputs = []
        for config_name, block_simulation_request in dict_block_simulation_requests.items():
            block_simulation_output = self.get_performance(block_simulation_request)
            block_bidding_output = block_simulation_output.convert_to_bidding_output(config_name)#, bidding_request.times)
            if (self.LSLMODE == True) & ('min' in config_name.lower()):
                block_bidding_output.net_mws = []
                for stgmw in block_bidding_output.stg_outputs.mw:
                    if int(stgmw) == 0:
                        block_bidding_output.net_mws.append(0)
                    elif '1x1' in config_name.lower():
                        block_bidding_output.net_mws.append(self.LSL1x1)
                    elif '2x1' in config_name.lower():
                        block_bidding_output.net_mws.append(self.LSL2x1)
                block_bidding_output.net_fuels = [0 if block_mw == 0 else block_hr * block_mw / 1000
                                                  for block_hr, block_mw in
                                                  zip(block_bidding_output.net_heat_rates,
                                                      block_bidding_output.net_mws)]


            # TODO figure out how to handle any number of operating modes, i.e. 3x1 or 4x1
            # TODO should seperate Config from Mode

            block_bidding_outputs.append(block_bidding_output)
        return block_bidding_outputs


class BlockSimulationConfigSchema(Schema):
    class Meta:
        ordered = True

    name = fields.String()
    min_db = fields.Number(default=BlockConstants.MIN_DB)
    max_db = fields.Number(default=BlockConstants.MAX_DB)
    min_rh = fields.Number(default=BlockConstants.MIN_RH * 100)
    max_rh = fields.Number(default=BlockConstants.MAX_RH * 100)
    min_baro = fields.Number(default=BlockConstants.MIN_BARO)
    max_baro = fields.Number(default=BlockConstants.MAX_BARO)
    trains = fields.Nested(TrainSimulationSchema(), many=True)
    stg = fields.Method('get_stg_name')

    @classmethod
    def get_stg_name(cls, obj: Block):
        return obj.stg.name


class BlockBiddingConfigSchema(Schema):
    class Meta:
        ordered = True

    name = fields.String()
    min_db = fields.Number(default=BlockConstants.MIN_DB)
    max_db = fields.Number(default=BlockConstants.MAX_DB)
    min_rh = fields.Number(default=BlockConstants.MIN_RH * 100)
    max_rh = fields.Number(default=BlockConstants.MAX_RH * 100)
    min_baro = fields.Number(default=BlockConstants.MIN_BARO)
    max_baro = fields.Number(default=BlockConstants.MAX_BARO)
    trains = fields.Nested(TrainBiddingSchema(), many=True)
    stg = fields.Method('get_stg_name')
    config_mode = fields.List(fields.String(), many=True)
    config_type = fields.List(fields.String(), many=True)
    @classmethod
    def get_stg_name(cls, obj: Block):
        return obj.stg.name
