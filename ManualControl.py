from Robot import Robot
from Condition import ManualControlCondition
from State import ManualControlState
from FiniteStateMachine import FiniteStateMachine
from Transition import ConditionalTransition



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
        
    
        