from State import State, MonitoredState
from abc import abstractmethod
from Transition import Transition
from typing import List
from time import perf_counter

class Condition:
    # TODO: Vérifier si le __inverse est correct
    def __init__(self, inverse: bool = False) -> None:
        self.__inverse = inverse

    @abstractmethod
    def _compare(self) -> bool:
        pass

    def __bool__(self) -> bool:
        return self._compare() if not self.__inverse else not self._compare()

class ConditionalTransition(Transition):
    #
    def __init__(self, next_state: State, condition: Condition = None) -> None:
        super().__init__(next_state)
        self.__condition : Condition = condition

    #
    @property
    def valid(self) -> bool:
        # if self.__condition:
        #     return True
        # return False
        return (self.__condition is not None) and super().valid
    
    @property
    def condition(self) -> Condition:
        return self.__condition
    
    @condition.setter
    def condition(self, condition: Condition) -> None:
        self.__condition : Condition = condition
    
    #
    def is_transiting(self) -> bool:
        return bool(self.__condition)

class ManyConditions(Condition): 
    """
    Représente une collection de conditions.

    Args:
        inverse (bool, optionnel): Indique si les conditions doivent être inversées. Par défaut, False.
    """

    def __init__(self, inverse: bool = False) -> None:
        super().__init__(inverse)
        self._conditions : List[Condition] = []

    def add_condition(self, condition: Condition) -> None:
        """
        Ajoute une seule condition à la collection.

        Args:
            condition (Condition): La condition à ajouter.
        """
        if not isinstance(condition, Condition):
            raise TypeError("condition must be of type Condition")
        self._conditions.append(condition)

    def add_conditions(self, conditions: List[Condition]) -> None:
        """
        Ajoute plusieurs conditions à la collection.

        Args:
            conditions (List[Condition]): Les conditions à ajouter.
        """
        for condition in conditions:
            self.add_condition(condition)

class AllConditions(ManyConditions):
    """
    Une classe représentant une collection de conditions qui doivent toutes être vraies.

    Hérite de la classe ManyConditions.

    Args:
        inverse (bool, optionnel): Si True, le résultat des conditions sera inversé. Par défaut, False.

    Méthodes:
        _compare(): Compare toutes les conditions et renvoie True si toutes les conditions sont vraies, False sinon.
    """

    def __init__(self, inverse: bool = False) -> None:
        super().__init__(inverse)

    def _compare(self) -> bool:
        """
        Compare toutes les conditions et renvoie True si toutes les conditions sont vraies, False sinon.
        """
        return all(condition for condition in self._conditions)
    
class AnyConditions(ManyConditions):
    """
    Une classe représentant une collection de conditions qui sont évaluées en utilisant l'opérateur 'any'.

    Args:
        inverse (bool, optionnel): Si True, le résultat de l'évaluation de la condition sera inversé. Par défaut, False.

    Méthodes:
        _compare(): Évalue les conditions en utilisant l'opérateur 'any' et renvoie le résultat.
    """

    def __init__(self, inverse: bool = False) -> None:
        super().__init__(inverse)

    def _compare(self) -> bool:
        """
        Évalue les conditions en utilisant l'opérateur 'any' et renvoie le résultat.

        Renvoie:
            bool: True si l'une des conditions est évaluée à True, False sinon.
        """
        return any(condition for condition in self._conditions)
    
class NoneConditions(ManyConditions):
    """
    Représente un ensemble de conditions qui s'évalue à True si aucune des conditions n'est vraie.
    Hérite de la classe ManyConditions.
    """

    def __init__(self, inverse: bool = False) -> None:
        super().__init__(inverse)

    def _compare(self) -> bool:
        """
        Compare les conditions et renvoie True si aucune des conditions n'est vraie.
        Renvoie:
            bool: True si aucune des conditions n'est vraie, False sinon.
        """
        return not any(condition for condition in self._conditions)

class MonitoredStateCondition(Condition):
    """
    Représente une condition basée sur un état surveillé.

    Args:
        monitored_state (MonitoredState): L'objet d'état surveillé.
        inverse (bool, optionnel): Indique si la condition doit être inversée. Par défaut, False.
    """

    def __init__(self, monitored_state: MonitoredState, inverse: bool = False) -> None:
        super().__init__(inverse)
        self._monitored_state: MonitoredState = monitored_state

    @property
    def monitored_state(self) -> MonitoredState:
        """
        Obtenez l'objet d'état surveillé.

        Renvoie:
            MonitoredState: L'objet d'état surveillé.
        """
        return self._monitored_state
    
    @monitored_state.setter
    def monitored_state(self, monitored_state: MonitoredState) -> None:
        """
        Définir l'objet d'état surveillé.

        Args:
            monitored_state (MonitoredState): L'objet d'état surveillé.
        """
        self._monitored_state: MonitoredState = monitored_state

    # TODO: Regarder si le _compare est correct
class StateEntryDurationCondition(MonitoredStateCondition):
    """
    Une condition qui vérifie si la durée de la dernière entrée de l'état surveillé
    est supérieure ou égale à une durée spécifiée.

    Args:
        duration (float): Le seuil de durée à comparer.
        monitored_state (MonitoredState): L'état surveillé à vérifier.
        inverse (bool, optionnel): Si True, la condition sera inversée. Par défaut, False.
    """

    def __init__(self, duration: float, monitored_state: MonitoredState, inverse: bool = False) -> None:
        super().__init__(monitored_state, inverse)
        self._duration: float = duration

    @property
    def duration(self) -> float:
        """
        Obtenez le seuil de durée.

        Renvoie:
            float: Le seuil de durée.
        """
        return self._duration
    
    @duration.setter
    def duration(self, duration: float) -> None:
        """
        Définir le seuil de durée.

        Args:
            duration (float): Le nouveau seuil de durée.
        """
        self._duration: float = duration

    def _compare(self) -> bool:
        """
        Compare la durée de la dernière entrée de l'état surveillé avec le seuil.

        Renvoie:
            bool: True si la durée est supérieure ou égale au seuil, False sinon.
        """

        return perf_counter() - self.monitored_state.last_entry_time >= self.duration
        
    
class StateEntryCountCondition(MonitoredStateCondition):
    """
    Représente une condition basée sur le nombre d'entrées d'un état surveillé.

    Args:
        expected_count (int): Le nombre d'entrées attendu.
        monitored_state (MonitoredState): L'objet d'état surveillé.
        auto_reset (bool): Indicateur indiquant si le compteur doit être réinitialisé automatiquement.
        inverse (bool, optionnel): Indicateur indiquant si la condition doit être inversée. Par défaut, False.
    """

    def __init__(self, expected_count: int, monitored_state: MonitoredState, auto_reset: bool, inverse: bool = False) -> None:
        super().__init__(monitored_state, inverse)
        self.__ref_count = monitored_state.entry_count
        self.__expected_count = expected_count
        self.__auto_reset = auto_reset

    @property
    def expected_count(self) -> int:
        """
        Obtenez le nombre d'entrées attendu.

        Renvoie:
            int: Le nombre d'entrées attendu.
        """
        return self.__expected_count
    
    @expected_count.setter
    def expected_count(self, expected_count: int) -> None:
        """
        Définir le nombre d'entrées attendu.

        Args:
            expected_count (int): Le nombre d'entrées attendu.
        """
        self.__expected_count : int = expected_count

    def _compare(self) -> bool:
        """
        Compare le nombre d'entrées avec le nombre d'entrées attendu.

        Renvoie:
            bool: True si la condition est remplie, False sinon.
        """
        return self._monitored_state.entry_count - self.__ref_count >= self.__expected_count
    
    def reset_count(self) -> None:
        """
        Réinitialise le nombre de référence au nombre d'entrées actuel.

        Cette méthode est appelée pour réinitialiser le compteur si `auto_reset` est True.
        """
        if self.__auto_reset:
            self.__ref_count : int = self._monitored_state.entry_count

class StateValueCondition(MonitoredStateCondition):
    """
    Représente une condition qui vérifie si la valeur personnalisée de l'état surveillé correspond à une valeur attendue.
    """

    def __init__(self, expected_value: any, monitored_state: MonitoredState, inverse: bool = False) -> None:
        super().__init__(monitored_state, inverse)
        self.__expected_value = expected_value

    @property
    def expected_value(self) -> any:
        """
        Obtenez la valeur attendue pour la condition.
        """
        return self.__expected_value
    
    @expected_value.setter
    def expected_value(self, expected_value: any) -> None:
        """
        Définir la valeur attendue pour la condition.
        """
        self.__expected_value = expected_value

    def _compare(self) -> bool:
        """
        Compare la valeur personnalisée de l'état surveillé avec la valeur attendue.
        Renvoie True si elles correspondent, False sinon.
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

        Renvoie :
            bool: Renvoie toujours True, sauf si inversé.
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

        Renvoie :
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

        Renvoie :
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

        Renvoie :
            bool: True si la durée s'est écoulée, False sinon.
        """
        self.__counter_duration = perf_counter() - self.__time_reference
        return self.__counter_duration >= self.__duration
