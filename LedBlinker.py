from Blinker import SideBlinker, Blinker
from State import MonitoredState
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Robot import Robot

class LedBlinker(SideBlinker):
    def __init__(self, robot: 'Robot'):
        self.robot = robot

        def off_right_state_generator() -> MonitoredState:
            off = MonitoredState()
            off.add_entering_action(self.robot.turn_off_right_led)
            return off
        
        def on_right_state_generator() -> MonitoredState:
            on = MonitoredState()
            on.add_entering_action(self.robot.turn_on_right_led)
            return on
        
        def off_left_state_generator() -> MonitoredState:
            off = MonitoredState()
            off.add_entering_action(self.robot.turn_off_left_led)
            return off
        
        def on_left_state_generator() -> MonitoredState:
            on = MonitoredState()
            on.add_entering_action(self.robot.turn_on_left_led)
            return on
        
        super().__init__(
            off_left_state_generator,
            on_left_state_generator,
            off_right_state_generator,
            on_right_state_generator
        )

