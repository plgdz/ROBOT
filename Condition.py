from State import State, MonitoredState
from abc import abstractmethod
from Transition import Transition
from typing import List, TYPE_CHECKING
from time import perf_counter
if TYPE_CHECKING:
    from Robot import Robot

class Condition:
    """
    Représente une condition abstraite dans un contexte de transitions d'état ou de logique de contrôle.
    Cette classe doit être étendue avec une implémentation concrète de la méthode `_compare`, qui définit
    la logique spécifique de la condition.

    Attributs:
        __inverse (bool): Si True, le résultat de la condition est inversé.
    
    Méthodes:
        _compare(): Méthode abstraite qui doit être implémentée pour comparer la condition.
        __bool__(): Permet à l'objet Condition de se comporter comme un booléen en fonction du résultat de _compare().
    """
    def __init__(self, inverse: bool = False) -> None:
        """
        Initialise la condition.
        
        Args:
            inverse (bool, optionnel): Si True, le résultat de la condition est inversé. Par défaut, False.
        
        Raises:
            TypeError: Si inverse n'est pas de type bool.

        Utilisation:
            >>> condition = Condition(inverse=True)
        """
        if not isinstance(inverse, bool):
            raise TypeError("inverse must be of type bool")
        self.__inverse: bool = inverse

    @abstractmethod
    def _compare(self) -> bool:
        """
        Méthode abstraite qui doit être implémentée pour évaluer la condition.
        
        Renvoie:
            bool: Résultat de l'évaluation de la condition.
        """
        pass

    def __bool__(self) -> bool:
        """
        Évalue la condition en utilisant la méthode _compare et inverse le résultat si nécessaire.

        Renvoie:
            bool: Le résultat final de la condition, potentiellement inversé.

        Utilisation:
            >>> bool(condition)
        """
        return self._compare() if not self.__inverse else not self._compare()

class ConditionalTransition(Transition):
    """
    Représente une transition conditionnelle entre deux états.

    Attributs:
        __condition (Condition): La condition associée à la transition.

    Propriétés:
        valid: Détermine si la transition est valide en fonction de la condition et de la transition de base.
        condition: Obtient la condition actuelle de la transition.

    Méthodes:
        is_transiting(): Évalue la condition pour déterminer si la transition doit avoir lieu.
    """
    def __init__(self, next_state: State, condition: Condition = None) -> None:
        """
        Initialise la transition conditionnelle.

        Args:
            next_state (State): L'état suivant de la transition.
            condition (Condition, optionnel): La condition associée à la transition. Par défaut, None.

        Raises:
            TypeError: Si la condition n'est pas de type Condition.

        Utilisation:
            >>> transition = ConditionalTransition(next_state=next_state, condition=condition)
        """
        super().__init__(next_state)
        if condition is not None and not isinstance(condition, Condition):
            raise TypeError("condition must be of type Condition")
        self.__condition : Condition = condition

    @property
    def valid(self) -> bool:
        """
        Détermine si la transition est valide en fonction de la condition et de la transition de base.

        Renvoie:
            bool: True si la condition est remplie et la transition de base est valide, False sinon.

        Utilisation:
            >>> transition.valid
        """
        return (self.__condition is not None) and super().valid
    
    @property
    def condition(self) -> Condition:
        """
        Obtient la condition associée à cette transition.

        Renvoie:
            Condition: La condition actuelle associée à cette transition.

        Utilisation:
            >>> transition.condition
        """
        return self.__condition
    
    @condition.setter
    def condition(self, condition: Condition) -> None:
        """
        Définit la condition associée à cette transition.

        Args:
            condition (Condition): La nouvelle condition à associer à cette transition.

        Renvoie:
            None

        Raises:
            TypeError: Si la condition n'est pas de type Condition.
        """
        if not isinstance(condition, Condition):
            raise TypeError("condition must be of type Condition")
        self.__condition : Condition = condition
    
    @property
    def transiting(self) -> bool:
        """
        Évalue la condition pour déterminer si la transition doit avoir lieu.

        Renvoie:
            bool: True si la condition est remplie, False sinon.

        Raises:
            ValueError: Si la condition est None.

        Utilisation:
            >>> transition.is_transiting()
        """
        return bool(self.__condition)

class ManyConditions(Condition): 
    """
    Une classe abstraite représentant une collection de conditions.

    Hérite de la classe Condition.

    Attributs:
        __conditions (List[Condition]): La liste des conditions à évaluer.

    Méthodes:
        add_condition(): Ajoute une seule condition à la collection.
        add_conditions(): Ajoute plusieurs conditions à la collection.
    """

    def __init__(self, inverse: bool = False) -> None:
        """
        Initialise la collection de conditions.

        Args:
            inverse (bool, optionnel): Si True, l'ensemble de conditions sera inversé. Par défaut, False.

        Utilisation:
            >>> many_conditions = ManyConditions()
        """
        super().__init__(inverse)
        self._conditions : List[Condition] = []

    def add_condition(self, condition: Condition) -> None:
        """
        Ajoute une seule condition à la collection.

        Args:
            condition (Condition): La condition à ajouter.

        Raises:
            TypeError: Si la condition n'est pas de type Condition.

        Utilisation:
            >>> many_conditions.add_condition(condition)
        """
        if not isinstance(condition, Condition):
            raise TypeError("condition must be of type Condition")
        self._conditions.append(condition)

    def add_conditions(self, conditions: List[Condition]) -> None:
        """
        Ajoute plusieurs conditions à la collection.

        Args:
            conditions (List[Condition]): La liste des conditions à ajouter.

        Raises:
            TypeError: Si une condition n'est pas de type Condition.

        Utilisation:
            >>> many_conditions.add_conditions([condition1, condition2])
        """
        for condition in conditions:
            if not isinstance(condition, Condition):
                raise TypeError("condition must be of type Condition")
            self.add_condition(condition)

class AllConditions(ManyConditions):
    """
    Représente un ensemble de conditions qui s'évalue à True si toutes les conditions sont vraies.

    Hérite de la classe ManyConditions.

    Méthodes:
        _compare(): Compare toutes les conditions et renvoie True si toutes les conditions sont vraies, False sinon.
    """

    def __init__(self, inverse: bool = False) -> None:
        """
        Initialise l'ensemble de conditions.

        Args:
            inverse (bool, optionnel): Si True, l'ensemble de conditions sera inversé. Par défaut, False.

        Utilisation:
            >>> all_conditions = AllConditions()
        """
        super().__init__(inverse)

    def _compare(self) -> bool:
        """
        Compare toutes les conditions et renvoie True si toutes les conditions sont vraies, False sinon.

        Renvoie:
            bool: True si toutes les conditions sont vraies, False sinon.

        Utilisation:
            >>> all_conditions._compare()
        """
        return all(condition for condition in self._conditions)
    
class AnyConditions(ManyConditions):
    """
    Représente un ensemble de conditions qui s'évalue à True si l'une des conditions est vraie.

    Hérite de la classe ManyConditions.

    Méthodes:
        _compare(): Évalue les conditions en utilisant l'opérateur 'any' et renvoie le résultat.
    """

    def __init__(self, inverse: bool = False) -> None:
        """
        Initialise l'ensemble de conditions.

        Args:
            inverse (bool, optionnel): Si True, l'ensemble de conditions sera inversé. Par défaut, False.

        Utilisation:
            >>> any_conditions = AnyConditions()
        """
        super().__init__(inverse)

    def _compare(self) -> bool:
        """
        Évalue les conditions en utilisant l'opérateur 'any' et renvoie le résultat.

        Renvoie:
            bool: True si l'une des conditions est vraie, False sinon.

        Utilisation:
            >>> any_conditions._compare()
        """
        return any(condition for condition in self._conditions)
    
class NoneConditions(ManyConditions):
    """
    Représente un ensemble de conditions qui s'évalue à True si aucune des conditions n'est vraie.

    Hérite de la classe ManyConditions.

    Méthodes:
        _compare(): Compare les conditions et renvoie True si aucune des conditions n'est vraie.
    """

    def __init__(self, inverse: bool = False) -> None:
        """
        Initialise l'ensemble de conditions.

        Args:
            inverse (bool, optionnel): Si True, l'ensemble de conditions sera inversé. Par défaut, False.

        Utilisation:
            >>> none_conditions = NoneConditions()
        """
        super().__init__(inverse)

    def _compare(self) -> bool:
        """
        Compare les conditions et renvoie True si aucune des conditions n'est vraie.

        Renvoie:
            bool: True si aucune des conditions n'est vraie, False sinon.

        Utilisation:
            >>> none_conditions._compare()
        """
        return not any(condition for condition in self._conditions)

class MonitoredStateCondition(Condition):
    """
    Une condition basée sur l'état surveillé.

    Cette classe abstraite fournit une base pour les conditions qui dépendent de l'état d'un objet MonitoredState.

    Attributs:
        _monitored_state (MonitoredState): L'objet d'état surveillé.

    Propriétés:
        monitored_state: Obtient l'objet d'état surveillé.

    Méthodes:
        _compare(): Méthode abstraite qui doit être implémentée pour comparer la condition.
    """

    def __init__(self, monitored_state: MonitoredState, inverse: bool = False) -> None:
        """
        Initialise la condition basée sur l'état surveillé.

        Args:
            monitored_state (MonitoredState): L'objet d'état surveillé.
            inverse (bool, optionnel): Si True, le résultat de la condition est inversé. Par défaut, False.

        Raises:
            TypeError: Si l'objet n'est pas de type MonitoredState.

        Utilisation:
            >>> condition = MonitoredStateCondition(monitored_state)
        """
        super().__init__(inverse)
        if not isinstance(monitored_state, MonitoredState):
            raise TypeError("monitored_state must be of type MonitoredState")
        self._monitored_state: MonitoredState = monitored_state

    @property
    def monitored_state(self) -> MonitoredState:
        """
        Obtenez l'objet d'état surveillé.

        Renvoie:
            MonitoredState: L'objet d'état surveillé.

        Utilisation:
            >>> monitored_state = condition.monitored_state
        """
        return self._monitored_state
    
    @monitored_state.setter
    def monitored_state(self, monitored_state: MonitoredState) -> None:
        """
        Définir l'objet d'état surveillé.

        Args:
            monitored_state (MonitoredState): Le nouvel objet d'état surveillé.

        Renvoie:
            None

        Raises:
            TypeError: Si l'objet n'est pas de type MonitoredState.

        Utilisation:
            >>> condition.monitored_state = monitored_state
        """
        if not isinstance(monitored_state, MonitoredState):
            raise TypeError("monitored_state must be of type MonitoredState")
        self._monitored_state: MonitoredState = monitored_state

class StateEntryDurationCondition(MonitoredStateCondition):
    """
    Représente une condition basée sur la durée de la dernière entrée d'un état surveillé.

    Propriétés:
        duration: Obtient le seuil de durée.

    Méthodes:
        _compare(): Compare la durée de la dernière entrée de l'état surveillé avec le seuil.
    """

    def __init__(self, duration: float, monitored_state: MonitoredState, inverse: bool = False) -> None:
        """
        Initialise la condition basée sur la durée de la dernière entrée de l'état surveillé.

        Args:
            duration (float): Le seuil de durée.
            monitored_state (MonitoredState): L'objet d'état surveillé.
            inverse (bool, optionnel): Si True, le résultat de la condition est inversé. Par défaut, False.

        Raises:
            ValueError: Si la durée est négative.

        Utilisation:
            >>> condition = StateEntryDurationCondition(duration=1.0, monitored_state=monitored_state)
        """
        super().__init__(monitored_state, inverse)
        if duration < 0:
            raise ValueError("duration must be positive")
        self._duration: float = duration

    @property
    def duration(self) -> float:
        """
        Obtenez le seuil de durée.

        Renvoie:
            float: Le seuil de durée.

        Utilisation:
            >>> duration = condition.duration
        """
        return self._duration
    
    @duration.setter
    def duration(self, duration: float) -> None:
        """
        Définir le seuil de durée.

        Args:
            duration (float): Le seuil de durée.

        Raises:
            ValueError: Si la durée est négative.

        Utilisation:
            >>> condition.duration = 1.0
        """
        if duration < 0:
            raise ValueError("duration must be positive")
        self._duration: float = duration

    def _compare(self) -> bool:
        """
        Compare la durée de la dernière entrée de l'état surveillé avec le seuil.

        Renvoie:
            bool: True si la durée de la dernière entrée est supérieure ou égale au seuil, False sinon.

        Utilisation:
            >>> condition._compare()
        """

        return perf_counter() - self.monitored_state.last_entry_time >= self.duration
        
    
class StateEntryCountCondition(MonitoredStateCondition):
    """
    Représente une condition basée sur le nombre d'entrées d'un état surveillé.

    Propriétés:
        expected_count: Obtient le nombre d'entrées attendu.

    Méthodes:
        _compare(): Compare le nombre d'entrées avec le nombre d'entrées attendu.
        reset_count(): Réinitialise le nombre de référence au nombre d'entrées actuel.
    """

    def __init__(self, expected_count: int, monitored_state: MonitoredState, auto_reset: bool, inverse: bool = False) -> None:
        """
        Initialise la condition basée sur le nombre d'entrées d'un état surveillé.
        
        Args:
            expected_count (int): Le nombre d'entrées attendu.
            monitored_state (MonitoredState): L'objet d'état surveillé.
            auto_reset (bool): Si True, le nombre de référence est réinitialisé après chaque comparaison.
            inverse (bool, optionnel): Si True, le résultat de la condition est inversé. Par défaut, False.
            
        Raises:
            ValueError: Si le nombre d'entrées attendu est négatif.

        Utilisation:
            >>> condition = StateEntryCountCondition(expected_count=3, monitored_state=monitored_state, auto_reset=True)
        """
        super().__init__(monitored_state, inverse)
        if expected_count < 0:
            raise ValueError("expected_count must be positive")
        self.__ref_count: int = monitored_state.entry_count
        self.__expected_count: int = expected_count
        self.__auto_reset: bool = auto_reset

    @property
    def expected_count(self) -> int:
        """
        Obtient le nombre d'entrées attendu.

        Return:
            int: Le nombre d'entrées attendu.

        Utilisation:
            >>> expected_count = condition.expected_count
        """
        return self.__expected_count
    
    @expected_count.setter
    def expected_count(self, expected_count: int) -> None:
        """
        Définir le nombre d'entrées attendu.

        Args:
            expected_count (int): Le nombre d'entrées attendu.

        Raises:
            ValueError: Si le nombre d'entrées attendu est négatif.

        Utilisation:
            >>> condition.expected_count = 3
        """
        if expected_count < 0:
            raise ValueError("expected_count must be positive")
        self.__expected_count : int = expected_count

    def _compare(self) -> bool:
        """
        Compare le nombre d'entrées avec le nombre d'entrées attendu.

        Renvoie:
            bool: True si le nombre d'entrées est supérieur ou égal au nombre d'entrées attendu, False sinon.

        Utilisation:
            >>> condition._compare()
        """
        return self._monitored_state.entry_count - self.__ref_count >= self.__expected_count
    
    def reset_count(self) -> None:
        """
        Réinitialise le nombre de référence au nombre d'entrées actuel.

        Utilisation:
            >>> condition.reset_count()
        """
        if self.__auto_reset:
            self.__ref_count : int = self._monitored_state.entry_count

class StateValueCondition(MonitoredStateCondition):
    """
    Représente une condition basée sur la valeur personnalisée d'un état surveillé.

    Propriétés:
        expected_value: Obtient la valeur attendue pour la condition.

    Méthodes:
        _compare(): Compare la valeur personnalisée de l'état surveillé avec la valeur attendue.
    """

    def __init__(self, expected_value: any, monitored_state: MonitoredState, inverse: bool = False) -> None:
        """
        Initialise la condition basée sur la valeur personnalisée de l'état surveillé.

        Args:
            expected_value (any): La valeur attendue pour la condition.
            monitored_state (MonitoredState): L'objet d'état surveillé.
            inverse (bool, optionnel): Si True, le résultat de la condition est inversé. Par défaut, False.

        Utilisation:
            >>> condition = StateValueCondition(expected_value="On", monitored_state=monitored_state)
        """
        super().__init__(monitored_state, inverse)
        self.__expected_value = expected_value

    @property
    def expected_value(self) -> any:
        """
        Obtient la valeur attendue pour la condition.

        Return:
            any: La valeur attendue pour la condition.

        Utilisation:
            >>> expected_value = condition.expected_value
        """
        return self.__expected_value
    
    @expected_value.setter
    def expected_value(self, expected_value: any) -> None:
        """
        Définit la valeur attendue pour la condition.

        Args:
            expected_value (any): La valeur attendue pour la condition.

        Utilisation:
            >>> condition.expected_value = "Off"
        """
        self.__expected_value: any = expected_value

    def _compare(self) -> bool:
        """
        Compare la valeur personnalisée de l'état surveillé avec la valeur attendue.

        Renvoie:
            bool: True si les valeurs sont égales, False sinon.

        Utilisation:    
            >>> condition._compare()
        """
        return self._monitored_state.custom_value == self.__expected_value
    
class AlwaysTrueCondition(Condition):
    """
    Une condition qui évalue toujours à True.

    Méthodes:
        _compare(): Évalue la condition.
    """

    def __init__(self, inverse: bool = False) -> None:
        """
        Initialise la condition qui évalue toujours à True.

        Args :
            inverse (bool, facultatif): Inverse le résultat de la condition. Par défaut à False.

        Utilisation :
            >>> condition = AlwaysTrueCondition()
        """
        super().__init__(inverse)

    def _compare(self) -> bool:
        """
        Évalue la condition.

        Renvoie :
            bool: True

        Utilisation :
            >>> condition._compare()
        """
        return True

class ValueCondition(Condition):
    """
    Une condition basée sur une valeur.

    Cette classe permet de créer une condition qui évalue à True si une valeur est égale à une valeur attendue.

    Attributs :
        __value (any): La valeur à comparer.
        __expected_value (any): La valeur attendue.

    Méthodes :
        _compare(): Compare la valeur à la valeur attendue.
    """

    def __init__(self, value: any, expected_value: any, inverse: bool = False) -> None:
        """
        Initialise la condition basée sur une valeur.

        Args :
            value (any): La valeur à comparer.
            expected_value (any): La valeur attendue.
            inverse (bool, facultatif): Inverse le résultat de la condition. Par défaut à False.

        Utilisation :
            >>> condition = ValueCondition(value=1, expected_value=1)
        """
        super().__init__(inverse)
        self.__value: any = value
        self.__expected_value: any = expected_value

    def _compare(self) -> bool:
        """
        Compare la valeur à la valeur attendue.

        Return :
            bool: True si la valeur est égale à la valeur attendue, False sinon.

        Utilisation :
            >>> condition._compare()
        """
        return self.__value == self.__expected_value


class TimedCondition(Condition):
    """
    Une condition temporelle qui évalue à True après une durée spécifiée.

    Attributs :
        __duration (float): La durée après laquelle la condition devient True.
        __counter_duration (float): Le compteur de temps pour la condition.
        __time_reference (float): Le point de référence temporel pour le début du comptage.

    Méthodes :
        reset(): Réinitialise le compteur de temps de la condition.
        _compare(): Vérifie si la durée spécifiée s'est écoulée depuis le point de référence temporel.

    Propriétés :
        duration (float): La durée après laquelle la condition devient True.
    """

    def __init__(self, duration: float = 1., time_reference: float = None, inverse: bool = False) -> None:
        """
        Initialise la condition temporelle.

        Args :
            duration (float, facultatif): La durée après laquelle la condition devient True. Par défaut à 1.
            time_reference (float, facultatif): Le point de référence temporel pour le début du comptage. Par défaut à None.
            inverse (bool, facultatif): Inverse le résultat de la condition. Par défaut à False.

        Raises :
            ValueError: Si la durée est négative.   

        Utilisation :
            >>> condition = TimedCondition(duration=1)
        """
        if duration < 0:
            raise ValueError("duration must be positive")
        super().__init__(inverse)
        self.__duration: float = duration
        self.__counter_duration: float = 0
        self.__time_reference: float = time_reference

    @property
    def duration(self) -> float:
        """
        Obtient la durée après laquelle la condition doit devenir True.

        Return :
            float: La durée.

        Utilisation :   
            >>> duration = condition.duration
        """
        return self.__duration
    
    @duration.setter
    def duration(self, duration: float) -> None:
        """
        Définit la durée après laquelle la condition doit devenir True.

        Args :
            duration (float): La durée.

        Raises :
            ValueError: Si la durée est négative.

        Utilisation :
            >>> condition.duration = 1
        """
        if duration < 0:
            raise ValueError("duration must be positive")
        self.__duration: float = duration

    def reset(self) -> None:
        """
        Réinitialise le compteur de temps de la condition.

        Utilisation :
            >>> condition.reset()
        """
        self.__counter_duration: float = 0
        self.__time_reference: float = 0

    def _compare(self) -> bool:
        """
        Vérifie si la durée spécifiée s'est écoulée depuis le point de référence temporel.

        Return :
            bool: True si la durée s'est écoulée, False sinon.

        Utilisation :
            >>> condition._compare()
        """
        self.__counter_duration = perf_counter() - self.__time_reference
        return self.__counter_duration >= self.__duration
    
class RobotCondition(Condition):
    def __init__(self, robot : 'Robot', inverse: bool = False) -> None:
        from Robot import Robot
        super().__init__(inverse)
        if not isinstance(robot, Robot):
            raise TypeError("robot must be of type Robot")
        self._robot: Robot = robot

class DistanceSensorCondition(RobotCondition):
    def __init__(self, robot : 'Robot', inverse: bool = False) -> None:
        super().__init__(robot, inverse)
        self.__expected_value = True
        
    def _compare(self) -> bool:
        return self._robot.reached_max_distance() == self.__expected_value

class ManualControlCondition(RobotCondition):
    def __init__(self, robot : 'Robot', expected_value : 'Robot.KeyCodes', read_once: bool= False, inverse: bool = False) -> None:
        super().__init__(robot, inverse)
        self.__expected_value = expected_value
        self.__read_once = read_once
        
    def _compare(self) -> bool:
        return self._robot.read_input(read_once=self.__read_once) == self.__expected_value