from enum import Enum, auto


class InletConditionerType(Enum):
    EVAPORATIVE_COOLERS = auto()
    FOGGERS = auto()
    CHILLERS = auto()
    NONE = auto()
