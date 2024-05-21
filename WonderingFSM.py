from Robot import Robot
from Condition import DistanceSensorCondition, ManualControlCondition, StateEntryDurationCondition, StateValueCondition
from State import ManualControlState, RotateState, WonderState
from FiniteStateMachine import FiniteStateMachine
from Transition import ConditionalTransition
from typing import TYPE_CHECKING
from Robot import Robot
import random
import time
from Blinker import SideBlinker
if TYPE_CHECKING:
    from Robot import Robot



class WonderingFSM(FiniteStateMachine):
    def __init__(self, robot):
        self.__robot = robot
        
        self.state_wonder = WonderState(robot=self.__robot, side = self.__robot.eye_blinker.Side.BOTH, cycle_duration=.0, percent_on=.0, begin_on=False, off=True)

        self.state_rotate = RotateState(robot=self.__robot, side=self.__robot.eye_blinker.Side.BOTH, cycle_duration= .0, percent_on = .0, begin_on =False, off=True)
        def entering_rotate():
            self.__robot.set_left_eye_color("red")
        
        def exiting_rotate():
            self.__robot.set_left_eye_color("blue")

        self.state_rotate.add_entering_action(entering_rotate)
        self.state_rotate.add_exiting_action(exiting_rotate)

        self.state_stop = self.__create_state(Robot.MoveDirection.STOP, side=self.__robot.eye_blinker.Side.BOTH, cycle_duration= .0, percent_on = .0, begin_on =False, off=True)        

        state_forward = self.__create_state(Robot.MoveDirection.FORWARD, side=self.__robot.eye_blinker.Side.BOTH, cycle_duration= 1.0, percent_on = .25, begin_on =True)
        state_backward = self.__create_state(Robot.MoveDirection.BACKWARD, side=self.__robot.eye_blinker.Side.BOTH, cycle_duration= 1.0, percent_on = .75, begin_on =True)
        state_left = self.__create_state(Robot.MoveDirection.LEFT, side=self.__robot.eye_blinker.Side.LEFT, cycle_duration= 1.0, percent_on = .5, begin_on =True)
        state_right = self.__create_state(Robot.MoveDirection.RIGHT, side=self.__robot.eye_blinker.Side.RIGHT, cycle_duration= 1.0, percent_on = .5, begin_on =True)

        self.__connect(state_forward, Robot.KeyCodes.UP)
        self.__connect(state_backward, Robot.KeyCodes.DOWN)
        self.__connect(state_left, Robot.KeyCodes.LEFT)
        self.__connect(state_right, Robot.KeyCodes.RIGHT)

        self.state_wonder.add_transition(ConditionalTransition(next_state=self.state_wonder, condition=StateEntryDurationCondition(duration=2.0, monitored_state=self.state_wonder)))
        self.state_wonder.add_transition(ConditionalTransition(next_state=self.state_rotate, condition=DistanceSensorCondition(self.__robot)))
        self.state_stop.add_transition(ConditionalTransition(next_state=self.state_wonder, condition=StateEntryDurationCondition(duration=2.0, monitored_state=self.state_stop)))
        self.state_rotate.add_transition(ConditionalTransition(next_state=self.state_wonder, condition=StateValueCondition(expected_value="found", monitored_state=self.state_rotate)))

        layout = FiniteStateMachine.Layout()
        layout.add_states([
            self.state_wonder,
            self.state_rotate,
            self.state_stop,
            state_forward,
            state_backward,
            state_left,
            state_right])
        
        layout.initial_state = self.state_stop

        super().__init__(layout)
    
    def __create_state(self, direction, side = None, cycle_duration = 1.0, percent_on = .5, begin_on = True, off = False):
        return ManualControlState(robot=self.__robot, move_configuration=direction, side = side, cycle_duration  = cycle_duration, percent_on = percent_on, begin_on = begin_on, off = off)
    
    def __connect(self, state, key):
        self.state_stop.add_transition(ConditionalTransition(next_state=state, condition=ManualControlCondition(self.__robot, key)))
        self.state_wonder.add_transition(ConditionalTransition(next_state=state, condition=ManualControlCondition(self.__robot, key)))
        state.add_transition(ConditionalTransition(next_state=self.state_stop, condition=ManualControlCondition(self.__robot, key, inverse=True)))
        state.add_transition(ConditionalTransition(next_state=self.state_rotate, condition=DistanceSensorCondition(self.__robot)))

