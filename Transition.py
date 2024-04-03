from abc import ABC, abstractmethod
from State import State

class Transition:
    """Représente une transition entre les états dans une machine à états.

    Cette classe abstraite définit le cadre pour une transition, incluant l'état suivant
    et si la transition est valide.

    Attributs :
        __next_state (State): L'état vers lequel cette transition mène.
    """

    def __init__(self, next_state: State = None) -> None:
        """Initialise une instance de Transition.

        Args :
            next_state (State, facultatif): L'état suivant de cette transition. Par défaut à None.
        """
        if not isinstance(next_state, State):
            raise TypeError("L'état suivant doit être une instance de State.")
        self.next_state = next_state

    @property
    def next_state(self) -> State:
        """Obtient l'état suivant de la transition.

        Retourne :
            State: L'état vers lequel la transition mène.
        """
        return self.__next_state
    
    @next_state.setter
    def next_state(self, next_state: State) -> None:
        """Définit l'état suivant de la transition.

        Args :
            next_state (State): L'état vers lequel la transition doit mener.
        """
        if not isinstance(next_state, State):
            raise TypeError("L'état suivant doit être une instance de State.")
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
