from abc import ABC, abstractmethod
from typing import Callable, List, TYPE_CHECKING
import time
if TYPE_CHECKING:
    from State import State
    from Condition import Condition

class Transition:
    """Représente une transition entre les états dans une machine à états.

    Cette classe abstraite définit le cadre pour une transition, incluant l'état suivant
    et si la transition est valide.

    Attributs :
        __next_state (State): L'état vers lequel cette transition mène.

    Propriétés :
        next_state (State): L'état vers lequel cette transition mène.
        valid (bool): Indique si la transition est valide.
        transiting (bool): Indique si la transition est en cours.

    Méthodes :
        _do_transiting_action(): Définit l'action à exécuter pendant la transition
        _exec_transiting_action(): Exécute l'action de transition
    """

    def __init__(self, next_state: 'State' = None) -> None:
        """Initialise une instance de Transition.

        Args :
            next_state (State, facultatif): L'état suivant de cette transition. Par défaut à None.
        """
        self.next_state = next_state

    @property
    def next_state(self) -> 'State':
        """Obtient l'état suivant de la transition.

        Retourne :
            State: L'état vers lequel la transition mène.

        Utilisation :
            >>> next_state = transition.next_state
        """
        return self.__next_state
    
    @next_state.setter
    def next_state(self, next_state: 'State') -> None:
        """Définit l'état suivant de la transition.

        Args :
            next_state (State): L'état vers lequel la transition doit mener.

        Raises :
            TypeError: Si next_state n'est pas une instance de State.

        Utilisation :
            >>> transition.next_state = next_state
        """
        from State import State
        if not isinstance(next_state, State):
            raise TypeError(f"next_state doit être une instance de State. Type actuel : {type(next_state)}")
        self.__next_state = next_state

    @property
    def valid(self) -> bool:
        """Vérifie si la transition est valide.

        Une transition est considérée comme valide si elle a un état suivant défini.

        Retourne :
            bool: True si la transition est valide, False autrement.

        Utilisation :
            >>> transition.valid
        """
        return True if self.__next_state is not None else False
    
    @property
    @abstractmethod
    def transiting(self) -> bool:
        """Indique si la transition est en cours.

        Cette méthode abstraite doit être implémentée par les sous-classes pour déterminer
        si la transition est actuellement en cours.

        Retourne :
            bool: True si la transition est en cours, False autrement.
        """
        pass

    def _exec_transiting_action(self) -> None:
        """Exécute l'action de transition.

        Cette méthode appelle `_do_transiting_action` pour effectuer l'action spécifique de transition.
        """
        self._do_transiting_action()

    def _do_transiting_action(self) -> None:
        """Définit l'action à exécuter pendant la transition.

        Cette méthode doit être surchargée par les sous-classes pour implémenter l'action spécifique
        de la transition.
        """
        pass


class ConditionalTransition(Transition):
    """Représente une transition conditionnelle entre les états dans une machine à états.

    Cette classe étend la classe Transition pour inclure une condition qui doit être satisfaite
    pour que la transition soit valide.

    Attributs :
        __condition (Condition): La condition qui doit être satisfaite pour que la transition soit valide.

    Propriétés :
        condition (Condition): La condition à satisfaire pour que la transition soit valide.
        valid (bool): Indique si la transition est valide.
        transiting (bool): Indique si la transition est en cours.
    """
    
    def __init__(self, next_state: 'State' = None, condition: 'Condition' = None) -> None:
        """Initialise une instance de ConditionalTransition.

        Args :
            next_state (State, facultatif): L'état suivant de cette transition. Par défaut à None.
            condition (Condition, facultatif): La condition qui doit être satisfaite pour que la transition soit valide. Par défaut à None.
        """
        super().__init__(next_state)
        self.__condition : 'Condition' = condition

    @property
    def valid(self) -> bool:
        """Vérifie si la transition est valide.

        Une transition est considérée comme valide si elle a un état suivant défini et que la condition est satisfaite.

        Retourne :
            bool: True si la transition est valide, False autrement.

        Utilisation :
            >>> transition.valid
        """
        return (self.__condition is not None) and super().valid
    
    @property
    def condition(self) -> 'Condition':
        """Obtient la condition de la transition.

        Retourne :
            Condition: La condition à satisfaire pour que la transition soit valide.

        Utilisation :
            >>> condition = transition.condition
        """
        return self.__condition
    
    @condition.setter
    def condition(self, condition: 'Condition') -> None:
        """
        Définit la condition de la transition.
        Args :
            condition (Condition): La condition à satisfaire pour que la transition soit valide.

        Raises :
            TypeError: Si condition n'est pas une instance de Condition.

        Utilisation :
            >>> transition.condition = condition
        """
        from Condition import Condition
        if not isinstance(condition, Condition):
            raise TypeError("condition doit être une instance de Condition.")
        self.__condition : 'Condition' = condition
    
    @property
    def transiting(self) -> bool:
        """Indique si la transition est en cours.

        Retourne :
            bool: True si la transition est en cours, False autrement.

        Utilisation :
            >>> transition.transiting
        """
        return bool(self.__condition)

class ActionTransition(ConditionalTransition):
    """Représente une transition avec une action à exécuter pendant la transition.

    Cette classe étend la classe ConditionalTransition pour inclure une action à exécuter
    pendant la transition.

    Attributs :
        __transiting_actions (List[Callable[[], None]]): La liste des actions à exécuter pendant la transition.

    Méthodes :
        add_transiting_action(action: Callable[[], None]): Ajoute une action à exécuter pendant la transition.
    """

    Action = Callable[[], None]

    def __init__(self, next_state: 'State' = None, condition: 'Condition' = None) -> None:
        """Initialise une instance de ActionTransition.

        Args :
            next_state (State, facultatif): L'état suivant de cette transition. Par défaut à None.

        Utilisation :
            >>> transition = ActionTransition(next_state)
        """
        super().__init__(next_state, condition)
        self.__transiting_actions : List[self.Action] = []

    def _do_transiting_action(self) -> None:
        """Exécute l'action de transition.

        Cette méthode exécute toutes les actions de transition enregistrées.

        Utilisation :
            >>> transition._do_transiting_action()
        """
        super()._do_transiting_action()
        for transiting_action in self.__transiting_actions:
            transiting_action()


    def add_transiting_action(self, action: Action) -> None:
        """Ajoute une action à exécuter au moment de transition.

        Args :
            action (Action) : L'action à exécuter.

        Raises :
            TypeError: Si l'action n'est pas une instance de Action.

        Utilisation :
            >>> transition.add_transiting_action(action)
        """
        if not isinstance(action, self.Action):
            raise TypeError("L'action doit être une instance de Action.")
        self.__transiting_actions.add(action)
        
class MonitoredTransition(ActionTransition):
    """Représente une transition avec un suivi de statistiques.

    Cette classe étend la classe ActionTransition pour inclure un suivi des statistiques
    de la transition.

    Attributs :
        __transit_count (int): Le nombre de fois que la transition a été effectuée.
        __last_transit_time (float): Le temps de la dernière transition.
        custom_value (any): Une valeur personnalisée pour la transition.

    Propriétés :
        transit_count (int): Le nombre de fois que la transition a été effectuée.
        last_transit_time (float): Le temps de la dernière transition.

    Méthodes :
        reset_transit_count(): Réinitialise le nombre de fois que la transition a été effectuée.
        reset_last_transit_time(): Réinitialise le temps de la dernière transition.
    """
    
    def __init__(self, next_state: 'State' = None, condition: 'Condition' = None) -> None:
        """Initialise une instance de MonitoredTransition.

        Args :
            next_state (State, facultatif): L'état suivant de cette transition. Par défaut à None.
            condition (Condition, facultatif): La condition qui doit être satisfaite pour que la transition soit valide. Par défaut à None.

        Utilisation :
            >>> transition = MonitoredTransition(next_state=next_state, condition=condition)
        """
        super().__init__(next_state, condition)
        self.__transit_count : int = 0
        self.__last_transit_time : float = 0
        self.custom_value : any = None

    @property
    def transit_count(self) -> int:
        """Obtient le nombre de fois que la transition a été effectuée.

        Retourne :
            int: Le nombre de fois que la transition a été effectuée.


        Utilisation :
            >>> transit_count = transition.transit_count
        """
        return self.__transit_count
    
    @transit_count.setter
    def transit_count(self) -> None:
        """Définit le nombre de fois que la transition a été effectuée.
        
        Cette propriété est en lecture seule.
        
        Raises :
            ValueError: Si la propriété est modifiée.
        """
        raise ValueError("transit_count is a read-only property")
    
    @property
    def last_transit_time(self) -> float:
        """Obtient le temps de la dernière transition.

        Retourne :
            float: Le temps de la dernière transition.

        Utilisation :
            >>> last_transit_time = transition.last_transit_time
        """
        return self.__last_transit_time
    
    @last_transit_time.setter
    def last_transit_time(self) -> None:
        """Définit le temps de la dernière transition.

        Cette propriété est en lecture seule.

        Raises :
            ValueError: Si la propriété est modifiée.
        """
        raise ValueError("last_transit_time is a read-only property")
    
    def reset_transit_count(self) -> None:
        """Réinitialise le nombre de fois que la transition a été effectuée."""
        self.__transit_count = 0

    def reset_last_transit_time(self) -> None:
        """Réinitialise le temps de la dernière transition."""
        self.__last_transit_time = 0
        
    def _exec_transiting_action(self) -> None:
        """Exécute l'action de transition.

        Cette méthode met à jour le moment de la derniere entrée et incrémente le compteur de l'état.

        Utilisation :
            >>> transition._exec_transiting_action()
        """
        self.__last_transit_time = time.perf_counter()
        self.__transit_count += 1
        super()._exec_transiting_action()
        
        