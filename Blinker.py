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
        from_off_duration_to_on = ConditionalTransition(next_state=self.__on, condition=self.sedc_off_duration)
        # from_off_duration_to_on.next_state(self.__on)
        self.__off_duration.add_transition(from_off_duration_to_on)
        
        # second transition : from on duration to off
        self.sedc_on_duration = StateEntryDurationCondition(0, self.__on_duration)
        from_on_duration_to_off = ConditionalTransition(next_state=self.__off, condition=self.sedc_on_duration)
        # from_on_duration_to_off.next_state(self.__off)
        self.__on_duration.add_transition(from_on_duration_to_off)

        
        # third transition : from blink_off to blink_on
        self.sedc_blink_off = StateEntryDurationCondition(0, self.__blink_off)
        from_blink_off_to_blink_on = ConditionalTransition(next_state=self.__blink_on, condition=self.sedc_blink_off)
        self.__blink_off.add_transition(from_blink_off_to_blink_on)
        
        # fourth transition : from blink_on to blink_off
        self.sedc_blink_on = StateEntryDurationCondition(0, self.__blink_on)
        from_blink_on_to_blink_off = ConditionalTransition(next_state=self.__blink_off, condition=self.sedc_blink_on)
        self.__blink_on.add_transition(from_blink_on_to_blink_off)
        
        # fifth transition : from blink_begin to blink_off & from blink_begin to blink_on
        self.svc_blink_begin = StateValueCondition(0, self.__blink_begin)
        from_blink_begin_to_blink_off = ConditionalTransition(next_state=self.__blink_off, condition=self.svc_blink_begin)
        from_blink_begin_to_blink_on = ConditionalTransition(next_state=self.__blink_on, condition=self.svc_blink_begin)
        self.__blink_begin.add_transition(from_blink_begin_to_blink_off)
        self.__blink_begin.add_transition(from_blink_begin_to_blink_on)
        
        # State entry condition sur le blink_stop_begin
        self.sedc_blink_stop_begin = StateEntryDurationCondition(0, self.__blink_stop_begin)
        from_blink_stop_begin_to_blink_stop_end = ConditionalTransition(next_state=self.__blink_stop_end, condition=self.sedc_blink_stop_begin)
        
        
        # sixth transition : from blink_stop_off to blink_stop_on
        self.sedc_blink_stop_off = StateEntryDurationCondition(0, self.__blink_stop_off)
        from_blink_stop_off_to_blink_stop_on = ConditionalTransition(next_state=self.__blink_stop_on, condition=self.sedc_blink_stop_off)
        self.__blink_stop_off.add_transition(from_blink_stop_begin_to_blink_stop_end)
        self.__blink_stop_off.add_transition(from_blink_stop_off_to_blink_stop_on)
        
        # seventh transition : from blink_stop_on to blink_stop_off
        self.sedc_blink_stop_on = StateEntryDurationCondition(0, self.__blink_stop_on)
        from_blink_stop_on_to_blink_stop_off = ConditionalTransition(next_state=self.__blink_stop_off, condition=self.sedc_blink_stop_on)
        self.__blink_stop_on.add_transition(from_blink_stop_begin_to_blink_stop_end)
        self.__blink_stop_on.add_transition(from_blink_stop_on_to_blink_stop_off)
        
        # eight transition : from blink_stop_begin to blink_stop_off & from blink_stop_begin to blink_stop_on
        self.svc_blink_stop_begin = StateValueCondition(0, self.__blink_stop_begin)
        from_blink_stop_begin_to_blink_stop_off = ConditionalTransition(next_state=self.__blink_stop_off, condition=self.svc_blink_stop_begin)
        from_blink_stop_begin_to_blink_stop_on = ConditionalTransition(next_state=self.__blink_stop_on, condition=self.svc_blink_stop_begin)
        self.__blink_stop_begin.add_transition(from_blink_stop_begin_to_blink_stop_off)
        self.__blink_stop_begin.add_transition(from_blink_stop_begin_to_blink_stop_on)
        
    
         #  init layout
        layout = FiniteStateMachine.Layout()
        layout.add_states([
            self.__off, self.__on, self.__off_duration, self.__on_duration,
            self.__blink_off, self.__blink_on, self.__blink_begin, self.__blink_stop_begin,
            self.__blink_stop_off, self.__blink_stop_on, self.__blink_stop_end])
        layout.initial_state = self.__off

        super().__init__(layout)

        
    @property
    def is_off(self) -> bool:
        return True if self.current_operational_state == self.__off else False
    
    @is_off.setter
    def is_off(self, value) -> None:
        raise ValueError("is_off is a read-only property")
    
    @property
    def is_on(self) -> bool:
        return True if self.current_operational_state == self.__on else False
    
    @is_on.setter
    def is_on(self, value) -> None:
        raise ValueError("is_on is a read-only property")
    
    def turn_off(self, **kwargs) -> None:
        if kwargs == {}:
            self.transit_to(self.__off)
        elif 'duration' in kwargs:
            self.sedc_off_duration.duration = kwargs['duration']
            self.transit_to(self.__off_duration)
        else:
            raise ValueError("turn_off takes at most 1 argument")
        
    def turn_on(self, **kwargs) -> None:
        if kwargs == {}:
            self.transit_to(self.__on)
        elif 'duration' in kwargs:
            self.sedc_on_duration.duration = kwargs["duration"]
            self.transit_to(self.__on_duration)
        else:
            raise ValueError("turn_on takes at most 1 argument")
        





# if __name__ == "__main__":
#     def off_state_generator() -> MonitoredState:
#         off = MonitoredState()
#         off.add_entering_action(lambda: print("Entering Off"))
#         off.add_in_state_action(lambda: print("Off"))
#         off.add_exiting_action(lambda: print("Exiting Off"))
#         return off
    
#     def on_state_generator() -> MonitoredState:
#         on = MonitoredState()
#         on.add_entering_action(lambda: print("Entering On"))
#         on.add_in_state_action(lambda: print("On"))
#         on.add_exiting_action(lambda: print("Exiting On"))
#         return on
    
#     blinker = Blinker(off_state_generator=off_state_generator, on_state_generator=on_state_generator)
    
#     blinker.track()
#     blinker.turn_on(duration=10.0)
#     blinker.start(reset=False, time_budget=1000)
  
    

