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
        """
        return self.__next_state
    
    @next_state.setter
    def next_state(self, next_state: 'State') -> None:
        """Définit l'état suivant de la transition.

        Args :
            next_state (State): L'état vers lequel la transition doit mener.
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
    
    def __init__(self, next_state: 'State' = None, condition: 'Condition' = None) -> None:
        super().__init__(next_state)
        self.__condition : 'Condition' = condition

    @property
    def valid(self) -> bool:
        return (self.__condition is not None) and super().valid
    
    @property
    def condition(self) -> 'Condition':
        return self.__condition
    
    @condition.setter
    def condition(self, condition: 'Condition') -> None:
        self.__condition : 'Condition' = condition
    
    @property
    def transiting(self) -> bool:
        return bool(self.__condition)

class ActionTransition(ConditionalTransition):

    Action = Callable[[], None]

    def __init__(self, next_state: 'State' = None, condition: 'Condition' = None) -> None:
        """Initialise une instance de ActionTransition.

        Args :
            next_state (State, facultatif): L'état suivant de cette transition. Par défaut à None.
        """
        super().__init__(next_state, condition)
        self.__transiting_actions : List[self.Action] = []

    def _do_transiting_action(self) -> None:
        super()._do_transiting_action()
        for transiting_action in self.__transiting_actions:
            transiting_action()


    def add_transiting_action(self, action: Action) -> None:
        """Ajoute une action à exécuter au moment de transition.

        Args :
            action (Action) : L'action à exécuter.
        """
        if not isinstance(action, self.Action):
            raise TypeError("L'action doit être une instance de Action.")
        self.__transiting_actions.add(action)
        
class MonitoredTransition(ActionTransition):
    
    def __init__(self, next_state: 'State' = None, condition: 'Condition' = None) -> None:
        """Initialise une instance de MonitoredTransition.

        Args :
            next_state (State, facultatif): L'état suivant de cette transition. Par défaut à None.
        """
        super().__init__(next_state, condition)
        self.__transit_count : int = 0
        self.__last_transit_time : float = 0
        self.custom_value : any = None

    @property
    def transit_count(self) -> int:
        return self.__transit_count
    
    @transit_count.setter
    def transit_count(self) -> None:
        raise ValueError("transit_count is a read-only property")
    
    @property
    def last_transit_time(self) -> float:
        return self.__last_transit_time
    
    @last_transit_time.setter
    def last_transit_time(self) -> None:
        raise ValueError("last_transit_time is a read-only property")
    
    def reset_transit_count(self) -> None:
        self.__transit_count = 0

    def reset_last_transit_time(self) -> None:
        self.__last_transit_time = 0
        
    def _exec_transiting_action(self) -> None:
        self.__last_transit_time = time.perf_counter()
        self.__transit_count += 1
        super()._exec_transiting_action()
        
        