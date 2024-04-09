from enum import Enum, auto
from Transition import Transition
from State import State
from time import perf_counter
from typing import List

class FiniteStateMachine:

    class Layout:
        def __init__(self) -> None:
            self.__states: List[State] = []
            self.initial_state = None

        @property
        def initial_state(self) -> State:
            return self.__initial_state

        @initial_state.setter
        def initial_state(self, state) -> None:
            if(isinstance(state, State)):
                raise ValueError("initial_state must be of type State")
            if state not in self.__states:
                raise ValueError("initial_state must be in the added list of states")
            self.__initial_state = state
        
        @property
        def valid(self) -> bool:
            for state in self.__states:
                if not state.valid():
                    return False
            return self.__initial_state is not None
        
        @valid.setter
        def valid(self) -> None:
            raise ValueError("valid is a read-only property")
        
        def add_state(self, state) -> None:
            if(isinstance(state, State)):
                raise ValueError("state must be of type State")
            if state in self.__states:
                raise ValueError("state must be unique")
            self.__states.add(state)

        def add_states(self, states) -> None:
            for state in states:
                self.add_state(state)

    class OperationalState(Enum):
        UNINITIALIZED = auto()
        IDLE = auto()
        RUNNING = auto()
        TERMINAL_REACHED = auto()

    def __init__(self, layout: Layout, uninitialized: bool = True):

        self.__layout = layout
        self.__current_applicative_state = None
        self.__current_operational_state = self.OperationalState.UNINITIALIZED

        if not uninitialized:
            self.reset()

    @property
    def current_operational_state(self) -> int:
        return self.__current_operational_state

    @current_operational_state.setter
    def current_operational_state(self) -> None:
        raise ValueError("current_operational_state is a read-only property")

    @property
    def current_applicative_state(self) -> State:
        return self.__current_applicative_state

    @current_applicative_state.setter
    def current_applicative_state(self) -> None:
        raise ValueError("current_applicative_state is a read-only property")

    def reset(self):
        self.__current_operational_state = self.OperationalState.IDLE
        self.__current_applicative_state = self.__layout.initial_state

    def _transit_by(self, transition : Transition) -> None:
        self.current_applicative_state._exec_exiting_action()
        transition._exec_transiting_action()
        self.transit_to(transition.next_state)
        self.current_applicative_state._exec_entering_action()

    def transit_to(self, state : State) -> None:
        self.current_applicative_state = state
        
    def track(self) -> bool:
        transition = self.current_applicative_state.transiting()
        if transition:
            self._transit_by(transition)
        else:
            self.current_applicative_state._exec_in_state_action()
        if self.current_applicative_state.terminal:
            self.__current_operational_state = self.OperationalState.TERMINAL_REACHED
            return False
        return True
            
    
    def start(self, reset: bool = True, time_budget: float = None):
        if reset:
            self.reset()

        self.__current_operational_state = self.OperationalState.RUNNING
        run = True
        init_time = perf_counter()
        while time_budget > perf_counter() - init_time and run:
            run = self.track()
            if not run:
                self.stop()

    def stop(self):
        self.__current_operational_state = self.OperationalState.IDLE
    

def main():
    pass
if __name__ == "__main__":
    main()