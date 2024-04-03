from State import State
from MonitoredState import MonitoredState
from abc import abstractmethod
from Transition import Transition

class Condition:
    def __init__(self, inverse: bool = False) -> None:
        self.__inverse = inverse

    @abstractmethod
    def _compare(self) -> bool:
        pass

    def __bool__(self) -> bool:
        pass

class ConditionalTransition(Transition):
    #
    def __init__(self, next_state: State, condition: Condition = None) -> None:
        super().__init__(next_state)
        self.__condition = condition

    #
    @property
    def is_valid(self) -> bool:
        return self.__condition is None or bool(self.__condition)
    
    @property
    def condition(self) -> Condition:
        return self.__condition
    
    @condition.setter
    def condition(self, condition: Condition) -> None:
        self.__condition = condition
    
    #
    def is_transiting(self) -> bool:
        return self.__condition is not None and self.__condition._compare()

class ManyConditions(Condition): 
    def __init__(self, inverse: bool = False) -> None:
        super().__init__(inverse)
        self._conditions = []

    def add_condition(self, condition: Condition) -> None:
        self._conditions.append(condition)

    def add_conditions(self, conditions: list[Condition]) -> None:
        self._conditions.extend(conditions)

class AllConditions(ManyConditions):
    def __init__(self, inverse: bool = False) -> None:
        super().__init__(inverse)

    def _compare(self) -> bool:
        return all(condition for condition in self._conditions)
    
class AnyConditions(ManyConditions):
    def __init__(self, inverse: bool = False) -> None:
        super().__init__(inverse)

    def _compare(self) -> bool:
        return any(condition for condition in self._conditions)
    
class NoneConditions(ManyConditions):
    def __init__(self, inverse: bool = False) -> None:
        super().__init__(inverse)

    def _compare(self) -> bool:
        return not any(condition for condition in self._conditions)

class MonitoredStateCondition(Condition):
    def __init__(self, monitored_state: MonitoredState, inverse: bool = False) -> None:
        super().__init__(inverse)
        self._monitored_state = monitored_state

    @property
    def monitored_state(self) -> MonitoredState:
        return self._monitored_state
    
    @monitored_state.setter
    def monitored_state(self, monitored_state: MonitoredState) -> None:
        self._monitored_state = monitored_state

class StateEntryDurationCondition(MonitoredStateCondition):
    def __init__(self, duration : float, monitored_state: MonitoredState, inverse: bool = False) -> None:
        super().__init__(monitored_state, inverse)
        self._duration = duration

    @property
    def duration(self) -> float:
        return self._duration
    
    @duration.setter
    def duration(self, duration: float) -> None:
        self._duration = duration

    def _compare(self) -> bool:
        return self._monitored_state.counter_last_entry >= self._duration
    
class StateEntryCountCondition(MonitoredStateCondition):
    def __init__(self, expected_count : int, monitored_state: MonitoredState, auto_reset : bool, inverse: bool = False) -> None:
        super().__init__(monitored_state, inverse)
        self.__expected_count = expected_count
        self.__ref_count = monitored_state.entry_count
        self.__expected_count = expected_count

    @property
    def expected_count(self) -> int:
        return self.__expected_count
    
    @expected_count.setter
    def expected_count(self, expected_count: int) -> None:
        self.__expected_count = expected_count

    def _compare(self) -> bool:
        return self._monitored_state.entry_count - self.__ref_count >= self.__expected_count
    
    def reset_count(self) -> None:
        self.__ref_count = self._monitored_state.entry_count

class StateValueCondition(MonitoredStateCondition):
    def __init__(self, expected_value : any, monitored_state: MonitoredState, inverse: bool = False) -> None:
        super().__init__(monitored_state, inverse)
        self.__expected_value = expected_value

    @property
    def expected_value(self) -> any:
        return self.__expected_value
    
    @expected_value.setter
    def expected_value(self, expected_value: any) -> None:
        self.__expected_value = expected_value

    def _compare(self) -> bool:
        return self._monitored_state.custom_value == self.__expected_value
    

