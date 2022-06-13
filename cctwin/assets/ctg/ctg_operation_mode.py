from enum import Enum


class CtgOperationMode(Enum):
    OFFLINE = 'Off'
    MINLOAD = 'Min'
    BASELOAD = 'Base'
    PARTLOAD = 'Part'
    AGCLOAD = 'Agc'
