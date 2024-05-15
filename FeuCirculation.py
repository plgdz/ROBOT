from typing import Callable
from FiniteStateMachine import FiniteStateMachine
from State import MonitoredState, State
from Transition import MonitoredTransition
from Condition import StateEntryDurationCondition

class TrafficLight(FiniteStateMachine):
        
    StateGenerator = Callable[[], State]

    def __init__(self,  red_state_generator:      StateGenerator, 
                        yellow_state_generator:   StateGenerator, 
                        green_state_generator:    StateGenerator
                ) -> None:
        
        # defining states
        state_red = red_state_generator()
        state_green = green_state_generator()
        state_yellow = yellow_state_generator()

        # defining transitions and adding them to states
        transition_red_to_green = MonitoredTransition(next_state=state_green, condition=StateEntryDurationCondition(10, state_red))
        state_red.add_transition(transition_red_to_green)

        transition_green_to_yellow = MonitoredTransition(next_state=state_yellow, condition=StateEntryDurationCondition(10, state_green))
        state_green.add_transition(transition_green_to_yellow)

        transition_yellow_to_red = MonitoredTransition(next_state=state_red, condition=StateEntryDurationCondition(5, state_yellow))
        state_yellow.add_transition(transition_yellow_to_red)

        # defining layout
        layout = FiniteStateMachine.Layout()
        layout.add_states([state_red, state_yellow, state_green])
        layout.initial_state = state_red
        super().__init__(layout=layout)

def main():

    def red_state_generator() -> MonitoredState:
        red_state = MonitoredState()
        red_state.add_in_state_action(lambda : print(f"\r\033[91m******\033[0m", end=""))
        return red_state
    
    def green_state_generator() -> MonitoredState:
        green_state = MonitoredState()
        green_state.add_in_state_action(lambda : print(f"\r\033[92m******\033[0m", end=""))
        return green_state
    
    def yellow_state_generator() -> MonitoredState:
        yellow_state = MonitoredState()
        yellow_state.add_in_state_action(lambda : print(f"\r\033[93m******\033[0m", end=""))
        return yellow_state
    
    traffic = TrafficLight(red_state_generator, yellow_state_generator, green_state_generator)
    traffic.start()

if __name__ == "__main__":
    main()

    # ***\n*****\n ***