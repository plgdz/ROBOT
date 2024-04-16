from State import State, MonitoredState
from abc import abstractmethod
from Transition import Transition
from typing import List
from time import perf_counter

class Condition:
    def __init__(self, inverse: bool = False) -> None:
        if not isinstance(inverse, bool):
            raise ValueError("The inverse parameter must be a boolean.")
        self.__inverse = inverse

    @abstractmethod
    def _compare(self) -> bool:
        pass

    def __bool__(self) -> bool:
        return self._compare() if not self.__inverse else not self._compare()

class ConditionList:
    def __init__(self) -> None:
        self._conditions : List[Condition] = []

    def __getitem__(self, key: int) -> Condition:
        return self._conditions[key]
    
    def __delitem__(self, key: int) -> None:
        del self._conditions[key]

    def __len__(self) -> int:
        return len(self._conditions)
    
    def append(self, condition: Condition) -> None:
        if not isinstance(condition, Condition):
            raise ValueError("The condition must be an instance of Condition.")
        self._conditions.append(condition)



class ManyConditions(Condition): 
    """
    Represents a collection of conditions.

    Args:
        inverse (bool, optional): Indicates whether the conditions should be inverted. Defaults to False.
    """

    def __init__(self, inverse: bool = False) -> None:
        super().__init__(inverse)
        self._conditions : ConditionList = ConditionList()

    def add_condition(self, condition: Condition) -> None:
        """
        Adds a single condition to the collection.

        Args:
            condition (Condition): The condition to add.
        """
        if not isinstance(condition, Condition):
            raise ValueError("The condition must be an instance of Condition.")
        self._conditions.append(condition)

    def add_conditions(self, conditions: List[Condition]) -> None:
        """
        Adds multiple conditions to the collection.

        Args:
            conditions (List[Condition]): The conditions to add.
        """
        for condition in conditions:
            self.add_condition(condition)

class AllConditions(ManyConditions):
    """
    A class representing a collection of conditions that must all be True.

    Inherits from the ManyConditions class.

    Args:
        inverse (bool, optional): If True, the result of the conditions will be inverted. Defaults to False.

    Methods:
        _compare(): Compares all conditions and returns True if all conditions are True, False otherwise.
    """

    def __init__(self, inverse: bool = False) -> None:
        super().__init__(inverse)

    def _compare(self) -> bool:
        """
        Compares all conditions and returns True if all conditions are True, False otherwise.
        """
        return all(condition for condition in self._conditions)
    
class AnyConditions(ManyConditions):
    """
    A class representing a collection of conditions that are evaluated using the 'any' operator.

    Args:
        inverse (bool, optional): If True, the result of the condition evaluation will be inverted. Defaults to False.

    Methods:
        _compare(): Evaluates the conditions using the 'any' operator and returns the result.

    """

    def __init__(self, inverse: bool = False) -> None:
        super().__init__(inverse)

    def _compare(self) -> bool:
        """
        Evaluates the conditions using the 'any' operator and returns the result.

        Returns:
            bool: True if any of the conditions evaluate to True, False otherwise.

        """
        return any(condition for condition in self._conditions)
    
class NoneConditions(ManyConditions):
    """
    Represents a set of conditions that evaluates to True if none of the conditions are True.
    Inherits from the ManyConditions class.
    """

    def __init__(self, inverse: bool = False) -> None:
        super().__init__(inverse)

    def _compare(self) -> bool:
        """
        Compares the conditions and returns True if none of the conditions are True.
        Returns:
            bool: True if none of the conditions are True, False otherwise.
        """
        return not any(condition for condition in self._conditions)

class MonitoredStateCondition(Condition):
    """
    Represents a condition based on a monitored state.

    Args:
        monitored_state (MonitoredState): The monitored state object.
        inverse (bool, optional): Whether the condition should be inverted. Defaults to False.
    """

    def __init__(self, monitored_state: MonitoredState, inverse: bool = False) -> None:
        super().__init__(inverse)
        self._monitored_state: MonitoredState = monitored_state

    @property
    def monitored_state(self) -> MonitoredState:
        """
        Get the monitored state object.

        Returns:
            MonitoredState: The monitored state object.
        """
        return self._monitored_state
    
    @monitored_state.setter
    def monitored_state(self, monitored_state: MonitoredState) -> None:
        """
        Set the monitored state object.

        Args:
            monitored_state (MonitoredState): The monitored state object.
        """
        self._monitored_state: MonitoredState = monitored_state

# TODO: Regarder si le _compare est correct
class StateEntryDurationCondition(MonitoredStateCondition):
    """
    A condition that checks if the duration of the monitored state's last entry
    is greater than or equal to a specified duration.

    Args:
        duration (float): The duration threshold to compare against.
        monitored_state (MonitoredState): The monitored state to check.
        inverse (bool, optional): If True, the condition will be inverted. Defaults to False.
    """

    def __init__(self, duration: float, monitored_state: MonitoredState, inverse: bool = False) -> None:
        super().__init__(monitored_state, inverse)
        self.__duration: float = duration

    @property
    def duration(self) -> float:
        """
        Get the duration threshold.

        Returns:
            float: The duration threshold.
        """
        return self.__duration
    
    @duration.setter
    def duration(self, duration: float) -> None:
        """
        Set the duration threshold.

        Args:
            duration (float): The new duration threshold.
        """
        if not isinstance(duration, (float)):
            raise ValueError("The duration must be a float.")
        self.__duration: float = duration

    def _compare(self) -> bool:
        """
        Compare the duration of the monitored state's last entry with the threshold.

        Returns:
            bool: True if the duration is greater than or equal to the threshold, False otherwise.
        """

        return perf_counter() - self.monitored_state.last_entry_time >= self.duration
        
    
class StateEntryCountCondition(MonitoredStateCondition):
    """
    Represents a condition based on the entry count of a monitored state.

    Args:
        expected_count (int): The expected entry count.
        monitored_state (MonitoredState): The monitored state object.
        auto_reset (bool): Flag indicating whether the count should be automatically reset.
        inverse (bool, optional): Flag indicating whether the condition should be inverted. Defaults to False.
    """

    def __init__(self, expected_count: int, monitored_state: MonitoredState, auto_reset: bool, inverse: bool = False) -> None:
        super().__init__(monitored_state, inverse)
        self.__ref_count: int = monitored_state.entry_count
        self.__expected_count: int = expected_count
        self.__auto_reset: bool = auto_reset

    @property
    def expected_count(self) -> int:
        """
        Get the expected entry count.

        Returns:
            int: The expected entry count.
        """
        return self.__expected_count
    
    @expected_count.setter
    def expected_count(self, expected_count: int) -> None:
        """
        Set the expected entry count.

        Args:
            expected_count (int): The expected entry count.
        """
        self.__expected_count : int = expected_count

    def _compare(self) -> bool:
        """
        Compare the entry count with the expected count.

        Returns:
            bool: True if the condition is met, False otherwise.
        """
        # return self._monitored_state.entry_count - self.__ref_count >= self.__expected_count
        return self.__ref_count >= self.__expected_count
    
    def reset_count(self) -> None:
        """
        Reset the reference count to the current entry count.

        This method is called to reset the count if `auto_reset` is True.
        """
        if self.__auto_reset:
            self.__ref_count : int = self._monitored_state.entry_count

class StateValueCondition(MonitoredStateCondition):
    """
    Represents a condition that checks if a monitored state's custom value matches an expected value.
    """

    def __init__(self, expected_value: any, monitored_state: MonitoredState, inverse: bool = False) -> None:
        super().__init__(monitored_state, inverse)
        self.__expected_value = expected_value

    @property
    def expected_value(self) -> any:
        """
        Get the expected value for the condition.
        """
        return self.__expected_value
    
    @expected_value.setter
    def expected_value(self, expected_value: any) -> None:
        """
        Set the expected value for the condition.
        """
        self.__expected_value = expected_value

    def _compare(self) -> bool:
        """
        Compare the monitored state's custom value with the expected value.
        Returns True if they match, False otherwise.
        """
        return self._monitored_state.custom_value == self.__expected_value
    
class AlwaysTrueCondition(Condition):
    """Représente une condition qui évalue toujours à True.

    Cette condition retourne True indépendamment du contexte, permettant une transition ou une action inconditionnelle.
    
    Attributs :
        Aucun attribut spécifique.
    """

    def __init__(self, inverse: bool = False) -> None:
        """Initialise une condition qui évalue toujours à True.

        Args :
            inverse (bool, facultatif): Inverse le résultat de la condition. Par défaut à False.
        """
        super().__init__(inverse)

    def _compare(self) -> bool:
        """Évalue la condition.

        Retourne :
            bool: Retourne toujours True, sauf si inversé.
        """
        return True


# TODO
class ValueCondition(Condition):
    """Compare une valeur donnée à une valeur attendue pour déterminer la validité de la condition.

    Cette classe permet de créer une condition basée sur l'égalité entre une valeur donnée et une valeur attendue.
    
    Attributs :
        __value (any): La valeur à comparer.
        __expected_value (any): La valeur attendue pour la comparaison.
    """

    def __init__(self, value: any, expected_value: any, inverse: bool = False) -> None:
        """Initialise la condition avec une valeur et une valeur attendue.

        Args :
            value (any): La valeur à comparer.
            expected_value (any): La valeur attendue.
            inverse (bool, facultatif): Inverse le résultat de la condition. Par défaut à False.
        """
        super().__init__(inverse)
        self.__value = value
        self.__expected_value = expected_value

    def _compare(self) -> bool:
        """Compare la valeur à la valeur attendue.

        Retourne :
            bool: True si les valeurs sont égales, False sinon.
        """
        return self.__value == self.__expected_value


class TimedCondition(Condition):
    """Une condition basée sur le temps, devenant True après une durée spécifiée.

    Cette classe permet de créer une condition qui évalue à True après que le temps spécifié se soit écoulé.
    
    Attributs :
        ___duration (float): La durée après laquelle la condition devient True.
        __counter_duration (float): Compteur utilisé pour mesurer le temps écoulé.
        __time_reference (float): Point de référence temporel pour le début du comptage.
    """

    def __init__(self, duration: float = 1., time_reference: float = None, inverse: bool = False) -> None:
        """Initialise la condition temporelle avec une durée et un point de référence temporel.

        Args :
            duration (float, facultatif): La durée après laquelle la condition doit devenir True. Par défaut à 1.
            time_reference (float, facultatif): Le point de référence temporel pour le début du comptage. Par défaut à None.
            inverse (bool, facultatif): Inverse le résultat de la condition. Par défaut à False.
        """
        super().__init__(inverse)
        self.__duration = duration
        self.__counter_duration = 0
        self.__time_reference = time_reference

    @property
    def duration(self) -> float:
        """Obtient la durée après laquelle la condition devient True.

        Retourne :
            float: La durée spécifiée pour la condition.
        """
        return self.__duration
    
    @duration.setter
    def duration(self, duration: float) -> None:
        """Définit la durée après laquelle la condition doit devenir True.

        Args :
            duration (float): La nouvelle durée.
        """
        self.__duration = duration

    def reset(self) -> None:
        """Réinitialise le compteur de temps de la condition."""
        self.__counter_duration = 0
        self.__time_reference = 0

    def _compare(self) -> bool:
        """Vérifie si la durée spécifiée s'est écoulée depuis le point de référence temporel.

        Retourne :
            bool: True si la durée s'est écoulée, False sinon.
        """
        self.__counter_duration = perf_counter() - self.__time_reference
        return self.__counter_duration >= self.__duration

