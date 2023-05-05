from typing import NamedTuple
from dataclasses import dataclass
import rev
import math
from range import Range


class NEO_Config(NamedTuple):
    Channel: int
    Inverted: bool
    IdleMode: rev.CANSparkMax.IdleMode
    MotorType: rev.CANSparkMaxLowLevel.MotorType


class PID_Config(NamedTuple):
    proportional_gain: float
    integral_gain: float
    derivative_gain: float

class Range_Map_Config(NamedTuple):
    pot_range: Range
    encoder_raw_range_length: float

@dataclass(init=False, frozen=True)
class Input_Config():
    JOYSTICK_RANGE = Range(min_val = -1, max_val = 1)

@dataclass(init=False, frozen=True)
class Arm_Config():
    DISTAL_NEO_CAN = NEO_Config(6, Inverted=False, IdleMode=rev.CANSparkMax.IdleMode.kCoast,
                                MotorType=rev.CANSparkMaxLowLevel.MotorType.kBrushless)
    LEFT_PROXIMAL_NEO_CAN = NEO_Config(7, Inverted=False, IdleMode=rev.CANSparkMax.IdleMode.kCoast,
                                       MotorType=rev.CANSparkMaxLowLevel.MotorType.kBrushless)
    RIGHT_PROXIMAL_NEO_CAN = NEO_Config(8, Inverted=False, IdleMode=rev.CANSparkMax.IdleMode.kCoast,
                                        MotorType=rev.CANSparkMaxLowLevel.MotorType.kBrushless)

    DISTAL_PID = PID_Config(0.5, 0, 0.001)
    LEFT_PROXIMAL_PID = PID_Config(0.5, 0, 0.001)
    RIGHT_PROXIMAL_PID = PID_Config(0.5, 0, 0.001)

    DISTAL_POTENTIOMETER_ANALOG_CHANNEL = 1  # type: int
    PROXIMAL_POTENTIOMETER_ANALOG_CHANNEL = 0  # type: int

    DISTAL_RANGE_MAP = Range_Map_Config(pot_range=Range(min_val=0.13772, max_val=0.679), encoder_raw_range_length=159.5)
    PROXIMAL_RANGE_MAP = Range_Map_Config(pot_range= Range(min_val=0.152949, max_val=0.337427), encoder_raw_range_length=61.3)
