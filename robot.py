import wpilib
import configuration
import ema
from arm import Arm


class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.arm = Arm(configuration.Arm_Config)
        self.arm_controller = wpilib.Joystick(0)
        self._ema_x = ema.EMA(15, 2)
        self._ema_y = ema.EMA(15, 2)

        self.logger.info(f'Hello World!')

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        self.logger.info("Periodic")

        self._ema_y.add(self.arm_controller.getY())
        self._ema_x.add(self.arm_controller.getX())

        proximal_arm_pos = configuration.Input_Config.JOYSTICK_RANGE.normalize(self._ema_x.ema_value)
        distal_arm_pos = configuration.Input_Config.JOYSTICK_RANGE.normalize(self._ema_y.ema_value)

        self.arm.set_position(proximal_arm_pos,
                              1-distal_arm_pos)

        self.arm.do_periodic()




if __name__ == '__main__':
    wpilib.run(MyRobot)