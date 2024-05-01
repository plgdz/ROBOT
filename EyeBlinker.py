from Blinker import SideBlinker
from State import MonitoredState
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Robot import Robot

class EyeBlinker(SideBlinker):
    def __init__(self, robot: 'Robot'):
        self.robot = robot

        def off_right_state_generator() -> MonitoredState:
            off = MonitoredState()
            off.add_entering_action(self.robot.turn_off_right_eye)
            return off
        
        def on_right_state_generator() -> MonitoredState:
            on = MonitoredState()
            on.add_entering_action(self.robot.turn_on_right_eye)
            return on
        
        def off_left_state_generator() -> MonitoredState:
            off = MonitoredState()
            off.add_entering_action(self.robot.turn_off_left_eye)
            return off
        
        def on_left_state_generator() -> MonitoredState:
            on = MonitoredState()
            on.add_entering_action(self.robot.turn_on_left_eye)
            return on
        
        super().__init__(
            off_left_state_generator,
            on_left_state_generator,
            off_right_state_generator,
            on_right_state_generator
        )
    
    # def set_right_eye_color(self, color: tuple) -> None:
    #     self.robot.__gpg.set_right_eye_color(color)

    # def set_left_eye_color(self, color: tuple) -> None:
    #     self.robot.__gpg.set_left_eye_color(color)

    # def set_both_eye_color(self, color: tuple) -> None:
    #     self.robot.__gpg.set_eyes_color(color)
