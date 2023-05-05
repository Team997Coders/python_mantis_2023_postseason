import rev
import wpilib
from wpilib import SmartDashboard
import logging

import configuration
from configuration import NEO_Config
import range
from range import Range


class Arm():
    _distal_encoder_range: Range
    _proximal_encoder_range: Range
    def do_periodic(self):
        SmartDashboard.putString("Arm Info",
                                        f'Distal Pot: {self._distal_pot.get():4f} Proximal Pot: {self._proximal_pot.get():4f}')
        SmartDashboard.putNumber("Distal Encoder Pos", self._distal_encoder.getPosition())
        SmartDashboard.putNumber("Distal Encoder Norm", self._distal_encoder_range.normalize(self._distal_encoder.getPosition()))

        SmartDashboard.putNumber("Proximal Encoder Pos", self._proximal_encoder.getPosition())
        SmartDashboard.putNumber("Proximal Encoder Norm", self._proximal_encoder_range.normalize(self._proximal_encoder.getPosition()))
        self._logger.info(f'Distal Pot: {self._distal_pot.get():4f} Proximal Pot: {self._proximal_pot.get():4f}')


    def set_position(self, proximal_scalar: float, distal_scalar: float):
        '''
        :param proximal_scalar: A value from 0 to 1 indicating where the proximal arm should be in its range
        :param distal_scalar:  A value from 0 to 1 indicating where the distal arm should be in its range
        :return:
        '''

        distal_pos = self._distal_encoder_range.interpolate(distal_scalar)
        self._distal_pid.setReference(distal_pos,
                                     rev.CANSparkMaxLowLevel.ControlType.kPosition)

        proximal_pos = self._proximal_encoder_range.interpolate(proximal_scalar)
        self._right_proximal_pid.setReference(proximal_pos,
                                     rev.CANSparkMaxLowLevel.ControlType.kPosition)

        SmartDashboard.putNumber("Distal Encoder Goal",
                                 distal_pos)
        SmartDashboard.putNumber("Proximal Encoder Goal",
                                 proximal_pos)

        SmartDashboard.putNumber("Proximal Encoder Goal For Real",
                                 self._proximal_encoder_range.max_val - proximal_pos)
        return

    def __init__(self, config: configuration.Arm_Config):
        self._config = config

        self._distal_neo = self.init_neo(config.DISTAL_NEO_CAN)
        self._left_proximal_neo = self.init_neo(config.LEFT_PROXIMAL_NEO_CAN)
        self._right_proximal_neo = self.init_neo(config.RIGHT_PROXIMAL_NEO_CAN)

        self._left_proximal_neo.follow(self._right_proximal_neo, invert=True) #config.LEFT_PROXIMAL_NEO_CAN.Inverted)

        self._distal_pid = self.init_pid(self._distal_neo, config.DISTAL_PID)
        self._left_proximal_pid = self.init_pid(self._left_proximal_neo, config.LEFT_PROXIMAL_PID)
        self._right_proximal_pid = self.init_pid(self._right_proximal_neo, config.RIGHT_PROXIMAL_PID)

        self._distal_pot = wpilib.AnalogPotentiometer(config.DISTAL_POTENTIOMETER_ANALOG_CHANNEL)
        self._proximal_pot = wpilib.AnalogPotentiometer(config.PROXIMAL_POTENTIOMETER_ANALOG_CHANNEL)

        self._logger = logging.getLogger(self.__class__.__name__)

        self._distal_encoder, self._distal_encoder_range = self.init_encoder(self._distal_neo, self._distal_pot, config.DISTAL_RANGE_MAP)
        self._proximal_encoder, self._proximal_encoder_range = self.init_encoder(self._right_proximal_neo,
                                                                                 self._proximal_pot,config.PROXIMAL_RANGE_MAP)



    @staticmethod
    def init_neo(config: NEO_Config) -> rev.CANSparkMax:
        neo = rev.CANSparkMax(config.Channel, config.MotorType)
        neo.setInverted(config.Inverted)
        neo.setIdleMode(config.IdleMode)
        return neo

    @staticmethod
    def init_pid(neo: rev.CANSparkMax, config: configuration.PID_Config) -> rev.SparkMaxPIDController:
        pid = neo.getPIDController()
        pid.setP(config.proportional_gain)
        pid.setI(config.integral_gain)
        pid.setD(config.derivative_gain)
        return pid

    def init_encoder(self,neo: rev.CANSparkMax, pot: wpilib.AnalogPotentiometer, config: configuration.Range_Map_Config)\
            -> tuple[rev.SparkMaxRelativeEncoder, Range]:
        '''
        Get the NEO encoder, and initialize the relative encoder position based on potentiometer position
        :param neo:
        :param config:
        :return:
        '''

        encoder = neo.getEncoder()
        scalar = config.pot_range.normalize(pot.get())
        encoder_min = -(scalar * config.encoder_raw_range_length)
        encoder_max = config.encoder_raw_range_length + encoder_min
        encoder.setPosition(0)

        return encoder, Range(encoder_min, encoder_max)