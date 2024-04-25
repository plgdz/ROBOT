from typing import Callable
from enum import Enum, auto
from FiniteStateMachine import FiniteStateMachine
from State import State, ActionState, MonitoredState
from Transition import ConditionalTransition, Transition, MonitoredTransition, ActionTransition
from Condition import StateEntryDurationCondition, StateValueCondition, AlwaysTrueCondition
from time import time

class Blinker(FiniteStateMachine):
    
    StateGenerator = Callable[[], MonitoredState]

    def __init__(self, off_state_generator: StateGenerator, on_state_generator: StateGenerator) -> None:
        
        default_value = 0

        # Implicite Monitored State
        # Off State
        self.__off = off_state_generator()      
        self.__off_duration = off_state_generator()
        self.__blink_off = off_state_generator()
        self.__blink_stop_off = off_state_generator()
        self.__blink_stop_off.custom_value = "off STOP"
        
        # On State
        self.__on = on_state_generator()
        self.__on_duration = on_state_generator()
        self.__blink_on = on_state_generator()
        self.__blink_stop_on = on_state_generator()
        self.__blink_stop_on.custom_value = "on STOP"
        
        # Explicite Monitored State
        self.__blink_begin = MonitoredState()
        self.__blink_stop_begin = MonitoredState()
        self.__blink_stop_end = MonitoredState()

        self.__off.add_transition(ConditionalTransition(next_state=self.__off, condition=AlwaysTrueCondition()))
        self.__on.add_transition(ConditionalTransition(next_state=self.__on, condition=AlwaysTrueCondition()))
        
        # first transition : from off duration to on
        self.sedc_off_duration = StateEntryDurationCondition(default_value, self.__off_duration)
        self.__off_duration.add_transition(ConditionalTransition(next_state=self.__on, condition=self.sedc_off_duration))

        # second transition : from on duration to off
        self.sedc_on_duration = StateEntryDurationCondition(default_value, self.__on_duration)
        self.__on_duration.add_transition(ConditionalTransition(next_state=self.__off, condition=self.sedc_on_duration))

        # third transition : from blink_off to blink_on
        self.sedc_blink_off = StateEntryDurationCondition(default_value, self.__blink_off)
        self.__blink_off.add_transition(ConditionalTransition(next_state=self.__blink_on, condition=self.sedc_blink_off))

        # fourth transition : from blink_on to blink_off
        self.sedc_blink_on = StateEntryDurationCondition(default_value, self.__blink_on)
        self.__blink_on.add_transition(ConditionalTransition(next_state=self.__blink_off, condition=self.sedc_blink_on))

        # fifth transition : from blink_begin to blink_off & from blink_begin to blink_on
        self.__blink_begin.add_transition(ConditionalTransition(next_state=self.__blink_off, condition=StateValueCondition(False, self.__blink_begin)))
        self.__blink_begin.add_transition(ConditionalTransition(next_state=self.__blink_on, condition=StateValueCondition(True, self.__blink_begin)))

        # State entry condition sur le blink_stop_begin
        self.__blink_stop_begin.add_transition(ConditionalTransition(next_state=self.__blink_stop_off, condition=StateValueCondition(False, self.__blink_stop_begin)))
        self.__blink_stop_begin.add_transition(ConditionalTransition(next_state=self.__blink_stop_on, condition=StateValueCondition(True, self.__blink_stop_begin)))

        #from blink_stop_off to blink_stop_on
        self.sedc_blink_stop_off = StateEntryDurationCondition(default_value, self.__blink_stop_off)
        self.__blink_stop_off.add_transition(ConditionalTransition(next_state=self.__blink_stop_on, condition= self.sedc_blink_stop_off))
        
        #from blink_stop_on to blink_stop_off
        self.sedc_blink_stop_on = StateEntryDurationCondition(default_value, self.__blink_stop_on)
        self.__blink_stop_on.add_transition(ConditionalTransition(next_state=self.__blink_stop_off, condition= self.sedc_blink_stop_on))

        #from blink_stop_on to blink_stop_end & from blink_stop_off to blink_stop_end
        self.sedc_blink_stop_begin = StateEntryDurationCondition(default_value, self.__blink_stop_begin)
        self.__blink_stop_off.add_transition(ConditionalTransition(next_state=self.__blink_stop_end, condition=self.sedc_blink_stop_begin))
        self.__blink_stop_on.add_transition(ConditionalTransition(next_state=self.__blink_stop_end, condition=self.sedc_blink_stop_begin))

        #from blink_stop_end to off & from blink_stop_end to on
        self.__blink_stop_end.add_transition(ConditionalTransition(next_state=self.__on, condition=StateValueCondition(True, self.__blink_stop_end)))
        self.__blink_stop_end.add_transition(ConditionalTransition(next_state=self.__off, condition=StateValueCondition(False, self.__blink_stop_end)))

        #  init layout
        layout = FiniteStateMachine.Layout()
        layout.add_states([
            self.__off, self.__on,                                                                          # off and on states
            self.__off_duration, self.__on_duration,                                                        # off and on duration states
            self.__blink_begin, self.__blink_off, self.__blink_on,                                          # off and on blink states
            self.__blink_stop_begin, self.__blink_stop_off, self.__blink_stop_on, self.__blink_stop_end])   # off and on blink stop states
        
        layout.initial_state = self.__off

        super().__init__(layout)

        
    @property
    def is_off(self) -> bool:
        return True if self.current_operational_state == self.__off else False
    
    @is_off.setter
    def is_off(self) -> None:
        raise ValueError("is_off is a read-only property")
    
    @property
    def is_on(self) -> bool:
        return True if self.current_operational_state == self.__on else False
    
    @is_on.setter
    def is_on(self) -> None:
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
        

    def blink(self, **kwargs) -> None:
        """
        Fait clignoter le clignotant selon les paramètres spécifiés.

        Args:
            - Configuration 1:
                * 'cycle_duration' (int): Durée totale d'un cycle de clignotement, en secondes.
                * 'percent_on' (float): Pourcentage du cycle pendant lequel le clignotant est allumé.
                * 'begin_on' (bool): Indique si le clignotant démarre en étant allumé.
            - Configuration 2:
                * 'total_duration' (int): Durée totale du clignotement, en secondes.
                * 'cycle_duration' (int): Durée totale d'un cycle de clignotement, en secondes.
                * 'percent_on' (float): Pourcentage du cycle pendant lequel le clignotant est allumé.
                * 'begin_on' (bool): Indique si le clignotant démarre en étant allumé.
                * 'end_off' (bool): Indique si le clignotant termine en étant éteint.
            - Configuration 3:
                * 'total_duration' (int): Durée totale du clignotement, en secondes.
                * 'n_cycles' (int): Nombre de cycles de clignotement.
                * 'percent_on' (float): Pourcentage du cycle pendant lequel le clignotant est allumé.
                * 'begin_on' (bool): Indique si le clignotant démarre en étant allumé.
                * 'end_off' (bool): Indique si le clignotant termine en étant éteint.
            - Configuration 4:
                * 'n_cycles' (int): Nombre de cycles de clignotement.
                * 'cycle_duration' (int): Durée totale d'un cycle de clignotement, en secondes.
                * 'percent_on' (float): Pourcentage du cycle pendant lequel le clignotant est allumé.
                * 'begin_on' (bool): Indique si le clignotant démarre en étant allumé.
                * 'end_off' (bool): Indique si le clignotant termine en étant éteint.

        Raises:
            ValueError: Si les arguments spécifiés sont invalides.
        """

        default_kwargs = {'cycle_duration': 1, 'percent_on': 0.5, 'begin_on': True, 'end_off': True}

        first_case = {'cycle_duration', 'percent_on', 'begin_on'}
        second_case = {'total_duration', 'cycle_duration', 'percent_on', 'begin_on', 'end_off'}
        third_case = {'total_duration', 'n_cycles', 'percent_on', 'begin_on', 'end_off'}
        fourth_case = {'n_cycles', 'cycle_duration', 'percent_on', 'begin_on', 'end_off'}

        if first_case == set(kwargs.keys()):
            # set the duration of the blink_off and blink_on states
            self.sedc_blink_on.duration = kwargs['cycle_duration'] * kwargs['percent_on']
            self.sedc_blink_off.duration = kwargs['cycle_duration'] - self.sedc_blink_on.duration
            # set the starting state of the blink
            self.__blink_begin.custom_value = kwargs['begin_on']
            # transit to the blink_begin state
            self.transit_to(self.__blink_begin)
        elif second_case == set(kwargs.keys()):
            # set the starting state of the blink
            self.__blink_stop_begin.custom_value = kwargs['begin_on']
            # set the duration of the blink_stop_begin state
            self.sedc_blink_stop_begin.duration = kwargs['total_duration']
            # set the duration of the blink_off and blink_on states
            self.sedc_blink_stop_on.duration = kwargs['cycle_duration'] * kwargs['percent_on']
            self.sedc_blink_stop_off.duration = kwargs['cycle_duration'] - self.sedc_blink_stop_on.duration
            # set the status of the blink_stop_end state
            self.__blink_stop_end.custom_value = kwargs['end_off']
            # transit to the blink_stop_begin state
            self.transit_to(self.__blink_stop_begin)
        elif third_case == set(kwargs.keys()):
            # set the starting state of the blink
            self.__blink_stop_begin.custom_value = kwargs['begin_on']
            # set the duration of the blink_stop_begin state
            self.sedc_blink_stop_begin.duration = kwargs['total_duration']
            # set the duration of the blink_off and blink_on states

            cycle_duration = kwargs['total_duration'] / kwargs['n_cycles']

            self.sedc_blink_stop_on.duration = cycle_duration * kwargs['percent_on']
            self.sedc_blink_stop_off.duration = cycle_duration - self.sedc_blink_stop_on.duration
            # set the status of the blink_stop_end state
            self.__blink_stop_end.custom_value = kwargs['end_off']
            # transit to the blink_stop_begin state
            self.transit_to(self.__blink_stop_begin)
        elif fourth_case == set(kwargs.keys()):
            # set the starting state of the blink
            self.__blink_stop_begin.custom_value = kwargs['begin_on']
            total_duration = kwargs['cycle_duration'] * kwargs['n_cycles']
            # set the duration of the blink_stop_begin state
            self.sedc_blink_stop_begin.duration = total_duration
            # set the duration of the blink_off and blink_on states
            self.sedc_blink_stop_on.duration = kwargs['cycle_duration'] * kwargs['percent_on']
            self.sedc_blink_stop_off.duration = kwargs['cycle_duration'] - self.sedc_blink_stop_on.duration
            # set the status of the blink_stop_end state
            self.__blink_stop_end.custom_value = kwargs['end_off']
            # transit to the blink_stop_begin state
            self.transit_to(self.__blink_stop_begin)
        else:
            raise ValueError(f"Invalid arguments, kwargs must be \n\t - {first_case}, \n\t - {second_case}, \n\t - {third_case}, \n\t - {fourth_case}")


class SideBlinker():

    class Side(Enum):
        LEFT = auto()
        RIGHT = auto()
        BOTH = auto()
        LEFT_RECIPROCAL = auto()
        RIGHT_RECIPROCAL = auto()

    def __init__(
            self,
            left_off_state_generator : Blinker.StateGenerator,
            left_on_state_generator : Blinker.StateGenerator,
            right_off_state_generator : Blinker.StateGenerator,
            right_on_state_generator : Blinker.StateGenerator
            ) -> None:
        self.__left_blinker = Blinker(left_off_state_generator, left_on_state_generator)
        self.__right_blinker = Blinker(right_off_state_generator, right_on_state_generator)

    def turn_off(self, side: Side) -> None:
        if side == side.LEFT:
            self.__left_blinker.turn_off()
        elif side == side.RIGHT:
            self.__right_blinker.turn_off()
        elif side == side.BOTH:
            self.__left_blinker.turn_off()
            self.__right_blinker.turn_off()
        elif side == side.LEFT_RECIPROCAL:
            self.__left_blinker.turn_off()
            self.__right_blinker.turn_on()
        elif side == side.RIGHT_RECIPROCAL:
            self.__right_blinker.turn_off()
            self.__left_blinker.turn_on()
        else:
            raise ValueError("Invalid side value")
        
    def turn_on(self, side: Side) -> None:
        if side == side.LEFT:
            self.__left_blinker.turn_on()
        elif side == side.RIGHT:
            self.__right_blinker.turn_on()
        elif side == side.BOTH:
            self.__left_blinker.turn_on()
            self.__right_blinker.turn_on()
        elif side == side.LEFT_RECIPROCAL:
            self.__left_blinker.turn_on()
            self.__right_blinker.turn_off()
        elif side == side.RIGHT_RECIPROCAL:
            self.__right_blinker.turn_on()
            self.__left_blinker.turn_off()
        else:
            raise ValueError("Invalid side value")
        
    def blink(self, side: Side, **kwargs) -> None:
        if side == side.LEFT:
            self.__left_blinker.blink(**kwargs)
        elif side == side.RIGHT:
            self.__right_blinker.blink(**kwargs)
        elif side == side.BOTH:
            self.__left_blinker.blink(**kwargs)
            self.__right_blinker.blink(**kwargs)
        elif side == side.LEFT_RECIPROCAL:
            self.__left_blinker.blink(**kwargs)
            self.__right_blinker.turn_off()
        elif side == side.RIGHT_RECIPROCAL:
            self.__right_blinker.blink(**kwargs)
            self.__left_blinker.turn_off()
        else:
            raise ValueError("Invalid side value")
        

if __name__ == "__main__":
    def off_state_generator() -> MonitoredState:
        off = MonitoredState()
        # off.add_entering_action(lambda: print("Entering Off"))
        off.add_in_state_action(lambda: print("Off"))
        # off.add_exiting_action(lambda: print("Exiting Off"))
        return off
    
    def on_state_generator() -> MonitoredState:
        on = MonitoredState()
        # on.add_entering_action(lambda: print("Entering On"))
        on.add_in_state_action(lambda: print("On"))
        # on.add_exiting_action(lambda: print("Exiting On"))
        return on
    
    blinker = Blinker(off_state_generator=off_state_generator, on_state_generator=on_state_generator)
    
    # blinker.track()
    blinker.blink(cycle_duration=4, n_cycles=5, percent_on=0.5, begin_on=True, end_off=True)
    # blinker.blink(cycle_duration=10, percent_on=0.5, begin_on=True)
    # blinker.track()
    blinker.start(reset=False, time_budget=10000)
  
    

