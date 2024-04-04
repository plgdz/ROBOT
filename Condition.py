from State import State, MonitoredState
from abc import abstractmethod
from Transition import Transition
from typing import List
from time import perf_counter

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
        self.__condition : Condition = condition

    #
    @property
    def is_valid(self) -> bool:
        return self.__condition is None or bool(self.__condition)
    
    @property
    def condition(self) -> Condition:
        return self.__condition
    
    @condition.setter
    def condition(self, condition: Condition) -> None:
        self.__condition : Condition = condition
    
    #
    def is_transiting(self) -> bool:
        return self.__condition is not None and self.__condition._compare()

class ManyConditions(Condition): 
    def __init__(self, inverse: bool = False) -> None:
        super().__init__(inverse)
        self._conditions : List[Condition] = []

    def add_condition(self, condition: Condition) -> None:
        self._conditions.append(condition)

    def add_conditions(self, conditions: List[Condition]) -> None:
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
        self._monitored_state : MonitoredState = monitored_state

    @property
    def monitored_state(self) -> MonitoredState:
        return self._monitored_state
    
    @monitored_state.setter
    def monitored_state(self, monitored_state: MonitoredState) -> None:
        self._monitored_state : MonitoredState = monitored_state

class StateEntryDurationCondition(MonitoredStateCondition):
    def __init__(self, duration : float, monitored_state: MonitoredState, inverse: bool = False) -> None:
        super().__init__(monitored_state, inverse)
        self._duration : float = duration

    @property
    def duration(self) -> float:
        return self._duration
    
    @duration.setter
    def duration(self, duration: float) -> None:
        self._duration : float = duration

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
        __duration (float): La durée après laquelle la condition devient True.
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

