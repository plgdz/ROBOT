from Robot import Robot
from Condition import RobotCondition, ManualControlCondition

class RobotState(State):
    def __init__(self, robot: Robot, parameters: Optional[State.Parameters] = None):
        if not isinstance(robot, Robot):
            raise TypeError("robot must be of type Robot")
        super().__init__(parameters)  
        self._robot: Robot = robot

class ManualControlState(RobotState):
    def __init__(self, robot: Robot, move_configuration: Robot.MoveDirection, parameters: Optional[State.Parameters] = None):
        self.__move_config = move_configuration
        super().__init__(robot, parameters)
        
    def _do_entering_action(self) -> None:
        super()._do_entering_action()
        self._robot.move(self.__move_config)
            
    def _do_in_state_action(self) -> None:
        super()._do_in_state_action()
        
    def _do_exiting_action(self) -> None:
        super()._do_exiting_action()
        self._robot.move(Robot.MoveDirection.STOP)

class ManualControlFSM(FiniteStateMachine):
    def __init__(self, robot):
        self.__robot = robot
        self.state_stop = self.__create_state(Robot.MoveDirection.STOP)
        state_forward = self.__create_state(Robot.MoveDirection.FORWARD)
        state_backward = self.__create_state(Robot.MoveDirection.BACKWARD)
        state_left = self.__create_state(Robot.MoveDirection.LEFT)
        state_right = self.__create_state(Robot.MoveDirection.RIGHT)
        
        self.__connect(state_forward, Robot.KeyCodes.UP)
        self.__connect(state_backward, Robot.KeyCodes.DOWN)
        self.__connect(state_left, Robot.KeyCodes.LEFT)
        self.__connect(state_right, Robot.KeyCodes.RIGHT)
        
        layout = FiniteStateMachine.Layout()
        layout.add_states([
            self.state_stop,
            state_forward,
            state_backward,
            state_left,
            state_right])
        
        layout.initial_state = self.state_stop

        super().__init__(layout)
        
        # del self.state_stop
        
        
    def __create_state(self, direction):
        return ManualControlState(robot=self.__robot, move_configuration=direction)
    
    def __connect(self, state, key):
        self.state_stop.add_transition(ConditionalTransition(next_state=state, condition=ManualControlCondition(self.__robot, key)))
        state.add_transition(ConditionalTransition(next_state=self.state_stop, condition=ManualControlCondition(self.__robot, key, inverse=True)))
        
    
        