from typing import Callable
from FiniteStateMachine import FiniteStateMachine
from State import State, ActionState, MonitoredState
from Transition import ConditionalTransition, Transition, MonitoredTransition, ActionTransition
from Condition import StateEntryDurationCondition, StateValueCondition
from time import time

# create state generator with no argumnents that return new state
# class StateGenerator:
#     def __init__(self) -> None:
#         self.__state = ActionState()
#         self.__state.add_in_state_action("Test")

#     def __call__(self) -> State:
#         return self.__state

class Blinker(FiniteStateMachine):
    
    StateGenerator = Callable[[], MonitoredState]

    def __init__(self, off_state_generator: StateGenerator, on_state_generator: StateGenerator) -> None:
        
        # Implicite Monitored State
        # Off State
        self.__off = off_state_generator()      
        self.__off_duration = off_state_generator()
        self.__blink_off = off_state_generator()
        self.__blink_stop_off = off_state_generator()
        
        # On State
        self.__on = on_state_generator()
        self.__on_duration = on_state_generator()
        self.__blink_on = on_state_generator()
        self.__blink_stop_on = on_state_generator()
        
        # Explicite Monitored State
        self.__blink_begin = MonitoredState()
        self.__blink_stop_begin = MonitoredState()
        self.__blink_stop_end = MonitoredState()
        
        
        # first transition : from off duration to on
        self.sedc_off_duration = StateEntryDurationCondition(0, self.__off_duration)
        from_off_duration_to_on = ConditionalTransition(self.sedc_off_duration)
        from_off_duration_to_on.next_state(self.__on)
        self.__off_duration.add_transition(from_off_duration_to_on)
        
        # second transition : from on duration to off
        self.sedc_on_duration = StateEntryDurationCondition(0, self.__on_duration)
        from_on_duration_to_off = ConditionalTransition(self.sedc_on_duration)
        from_on_duration_to_off.next_state(self.__off)
        self.__on_duration.add_transition(from_on_duration_to_off)
        
        
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
    

    
    def turn_off(self, *args) -> None:
        if len(args) == 1:
            self.transit_to(self.__off)
        elif len(args) == 2:
            self.sedc_off_duration.duration = args[2]
            self.transit_to(self.__off_duration)
        else:
            raise ValueError("turn_off takes at most 1 argument")
        
    def turn_on(self, *args) -> None:
        if len(args) == 1:
            self.transit_to(self.__on)
        elif len(args) == 2:
            self.sedc_on_duration.duration = args[2]
            self.transit_to(self.__on_duration)
        else:
            raise ValueError("turn_on takes at most 1 argument")
