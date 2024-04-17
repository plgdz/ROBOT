# Version: 1.0
from typing import Callable, List, Optional, TYPE_CHECKING
import time
if TYPE_CHECKING:
    from Transition import Transition

class State:
    """Représente un état dans une machine à états.

    Cette classe contient des informations sur un état au sein d'une machine à états, incluant ses paramètres
    et ses transitions vers d'autres états.

    Attributs :
        parameters (Parameters) : Les paramètres définissant le comportement de l'état.
        __transitions (set) : Un ensemble de transitions de cet état vers d'autres états.
    """

    class Parameters:
        """Paramètres définissant le comportement d'un état dans une machine à états.

        Attributs :
            terminal (bool) : Indicateur si l'état est terminal.
            do_in_state_action_when_entering (bool) : Indicateur si une action doit être exécutée en entrant dans l'état.
            do_in_state_action_when_exiting (bool) : Indicateur si une action doit être exécutée en sortant de l'état.
        """

        def __init__(self, terminal: bool = False, do_in_state_action_when_entering: bool = False, do_in_state_action_when_exiting: bool = False):
            """Initialise les paramètres pour un état.

            Args :
                terminal (bool) : Si l'état est terminal. Par défaut à False.
                do_in_state_action_when_entering (bool) : Si une action doit être exécutée à l'entrée. Par défaut à False.
                do_in_state_action_when_exiting (bool) : Si une action doit être exécutée à la sortie. Par défaut à False.
            """

            if not isinstance(terminal, bool) or not isinstance(do_in_state_action_when_entering, bool) or not isinstance(do_in_state_action_when_exiting, bool):
                raise TypeError("Les paramètres doivent être des booléens.")
            self.terminal = terminal
            self.do_in_state_action_when_entering = do_in_state_action_when_entering
            self.do_in_state_action_when_exiting = do_in_state_action_when_exiting

    def __init__(self, parameters: Optional[Parameters] = None) -> None:
        """Initialise une instance de State.

        Args :
            parameters (Parameters) : Les paramètres de comportement de l'état. Par défaut à une instance vide de Parameters.
        """
        
        self.parameters : State.Parameters = parameters if parameters is not None else self.Parameters()
        self.__transitions = []

    @property
    def valid(self) -> bool:
        """Vérifie si l'état a des transitions valides.

        Retourne :
            bool : True si toutes les transitions sont valides, False autrement.
        """
        if not self.__transitions or not all(transition.valid for transition in self.__transitions):
            return False
        return True

    @property
    def terminal(self) -> bool:
        """Indique si l'état est terminal.

        Retourne :
            bool : True si l'état est terminal, False autrement.
        """
        return self.parameters.terminal

    @property
    def transiting(self) -> bool:
        """Liste les statuts de transition.

        Retourne :
            bool : La transition en cours, None autrement.
        """
        for transition in self.__transitions:
            if transition.transiting:
                return transition
        return None

    def add_transition(self, transition: 'Transition'):
        """Ajoute une transition à l'état.

        Args :
            transition (Transition) : La transition à ajouter.
        """
        from Transition import Transition
        if not isinstance(transition, Transition):
            raise TypeError("La transition doit être une instance de Transition.")
        if transition in self.__transitions:
            raise ValueError("La transition est déjà ajoutée.")
        self.__transitions.append(transition)

    def _exec_entering_action(self) -> None:
        """Exécute l'action associée à l'entrée dans l'état."""
        self._do_entering_action()
        if self.parameters.do_in_state_action_when_entering:
            self._exec_in_state_action()

    def _exec_in_state_action(self) -> None:
        """Exécute l'action associée à la présence dans l'état."""
        self._do_in_state_action()

    def _exec_exiting_action(self) -> None:
        """Exécute l'action associée à la sortie de l'état."""
        if self.parameters.do_in_state_action_when_exiting:
            self._exec_in_state_action()
        self._do_exiting_action()
        

    def _do_entering_action(self) -> None:
        """Définit l'action à exécuter à l'entrée de l'état."""
        pass

    def _do_in_state_action(self) -> None:
        """Définit l'action à exécuter pendant la présence dans l'état."""
        pass

    def _do_exiting_action(self) -> None:
        """Définit l'action à exécuter à la sortie de l'état."""
        pass

class ActionState(State):

    Action = Callable[[], None]

    def __init__(self, parameters: Optional[State.Parameters] = None) -> None:
        """Initialise une instance de State.

        Args :
            parameters (Parameters) : Les paramètres de comportement de l'état. Par défaut à une instance vide de Parameters.
        """
        super().__init__(parameters)
        self.__entering_actions : List[self.Action] = []
        self.__in_state_actions : List[self.Action] = []
        self.__exiting_actions : List[self.Action] = []

    def _do_entering_action(self) -> None:
        super()._do_entering_action()
        for action in self.__entering_actions:
            action()

    def _do_in_state_action(self) -> None:
        super()._do_in_state_action()
        for action in self.__in_state_actions:
            action()

    def _do_exiting_action(self) -> None:
        super()._do_exiting_action()
        for action in self.__exiting_actions:
            action()

    def add_entering_action(self, action: Action) -> None:
        """Ajoute une action à exécuter à l'entrée de l'état.

        Args :
            action (Action) : L'action à exécuter.
        """
        if not callable(action):
            raise TypeError("L'action doit être une instance de Action.")
        self.__entering_actions.append(action)

    def add_in_state_action(self, action: Action) -> None:
        """Ajoute une action à exécuter pendant l'état.

        Args :
            action (Action) : L'action à exécuter.
        """
        if not callable(action):
            raise TypeError("L'action doit être une instance de Action.")
        self.__in_state_actions.append(action)

    def add_exiting_action(self, action: Action) -> None:
        """Ajoute une action à exécuter à la sortie de l'état.

        Args :
            action (Action) : L'action à exécuter.
        """
        if not callable(action):
            raise TypeError("L'action doit être une instance de Action.")
        self.__exiting_actions.append(action) 

class MonitoredState(ActionState):
    def __init__(self, parameters: Optional[State.Parameters] = None) -> None:
        """Initialise une instance de State.

        Args :
            parameters (Parameters) : Les paramètres de comportement de l'état. Par défaut à une instance vide de Parameters.
        """
        super().__init__(parameters)
        self.__counter_last_entry : complex = 0
        self.__counter_last_exit : complex = 0
        self.__entry_count : int = 0
        self.custom_value : any = None

    @property
    def entry_count(self) -> int:
        """Obtient le nombre d'entrées dans l'état.

        Retourne :
            int : Le nombre d'entrées dans l'état.
        """
        return self.__entry_count
    
    @property
    def last_entry_time(self) -> float:
        """Obtient le compteur de la dernière entrée dans l'état.

        Retourne :
            float : Le compteur de la dernière entrée dans l'état.
        """
        return self.__counter_last_entry
    
    
    @property
    def last_exit_time(self) -> float:
        """Obtient le compteur de la dernière sortie de l'état.

        Retourne :
            float : Le compteur de la dernière sortie de l'état.
        """
        return self.__counter_last_exit
    
    def reset_entry_count(self) -> None:
        """Réinitialise le compteur d'entrées."""
        self.__entry_count = 0

    def reset_last_times(self) -> None:
        """Réinitialise les compteurs de temps."""
        self.__counter_last_entry = 0
        self.__counter_last_exit = 0

    def _exec_entering_action(self) -> None:
        """Exécute l'action associée à l'entrée dans l'état."""
        self.__counter_last_entry = time.perf_counter()
        self.__entry_count += 1
        super()._exec_entering_action()

    def _exec_exiting_action(self) -> None:
        """Exécute l'action associée à la sortie de l'état."""
        super()._exec_exiting_action()
        self.__counter_last_exit = time.perf_counter()
        
