from FiniteStateMachine import FiniteStateMachine
from State import ActionState, State
from time import time

# create state generator with no argumnents that return new state
class StateGenerator:
    def __init__(self) -> None:
        self.__state = ActionState()
        self.__state.add_in_state_action("Test")

    def __call__(self) -> State:
        return self.__state

class Blinker(FiniteStateMachine):

    def __init__(self, off_state_generator: StateGenerator, on_state_generator: StateGenerator) -> None:
        layout = FiniteStateMachine.Layout()
        layout.add_states([off_state_generator(), on_state_generator()])
        layout.initial_state = off_state_generator()
        super().__init__(layout)

    @property
    def is_off(self) -> bool:
        return self.current_operational_state != self.OperationalState.RUNNING
    
    @is_off.setter
    def is_off(self, value) -> None:
        raise ValueError("is_off is a read-only property")
    
    @property
    def is_on(self) -> bool:
        return self.current_operational_state == self.OperationalState.RUNNING
    
    @is_on.setter
    def is_on(self, value) -> None:
        raise ValueError("is_on is a read-only property")
    
    def __turn_off_immediately(self) -> None:
        self.stop()

    # TODO: A CHECKER
    def __turn_off_with_delay(self, duration: int) -> None:
        time.sleep(duration)
        self.stop()
    
    def turn_off(self, *args) -> None:
        if len(args) == 1:
            self.__turn_off_immediately()
        elif len(args) == 2:
            self.__turn_off_with_delay(args[1])
        else:
            raise ValueError("turn_off takes at most 1 argument")
        
    def __turn_on_immediately(self) -> None:
        self.start()

    # TODO: A CHECKER
    def __turn_on_with_delay(self, duration: int) -> None:
        time.sleep(duration)
        self.start()
    
    def turn_on(self, *args) -> None:
        if len(args) == 1:
            self.__turn_on_immediately()
        elif len(args) == 2:
            self.__turn_on_with_delay(args[1])
        else:
            raise ValueError("turn_on takes at most 1 argument")




    def turn_on(self) -> None:
        self.start()