from enum import Enum, auto

class State:
    def __init__(self):
        pass

    def valid(self) -> bool:
        return True
    
class Transition:
    def __init__(self) -> None:
        pass

class FiniteStateMachine:
    class Layout:
        def __init__(self) -> None:
            self.__states = {State(), State()}
            self.initial_state = self.__states[0]
           
        @property
        def initial_state(self) -> State:
            return self.__initial_state
       
        @initial_state.setter
        def initial_state(self, state) -> None:
            if(isinstance(state, State)):
                raise ValueError("initial_state must be of type State")
            if state not in self.__states:
                raise ValueError("initial_state must be in states which must contain at least one state")
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
       
        self.__current_applicative_state = None
        self.__current_operational_state = self.OperationalState.UNINITIALIZED
        self.__layout = layout
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
        pass

    def transit_to(self, state : State) -> None:
        pass
        
    def track(self) -> bool:
        return self.current_applicative_state.transiting()
    
    def start(self, reset: bool = True, time_budget: float = None):
        self.__current_operational_state = self.OperationalState.RUNNING
        run = True
        while run and time_budget:
            run = self.track()
       
    def stop(self):
        self.__current_operational_state = self.OperationalState.IDLE
       
    

def main():
    pass
if __name__ == "__main__":
    main()