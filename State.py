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

    def __init__(self, parameters: Parameters = Parameters()) -> None:
        """Initialise une instance de State.

        Args :
            parameters (Parameters) : Les paramètres de comportement de l'état. Par défaut à une instance vide de Parameters.
        """
        self.parameters = parameters
        self.__transitions = set()

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
            list[bool] : Une liste indiquant si l'état est actuellement en transition à travers une quelconque transition.
        """
        return [transition.transiting for transition in self.__transitions.values() if transition.transiting == True]

    def add_transition(self, transition: Transition):
        """Ajoute une transition à l'état.

        Args :
            transition (Transition) : La transition à ajouter.
        """
        if not isinstance(transition, Transition):
            raise TypeError("La transition doit être une instance de Transition.")
        self.__transitions.add(transition)

    def _exec_entering_action(self) -> None:
        """Exécute l'action associée à l'entrée dans l'état."""
        self._do_entering_action()

    def _exec_in_state_action(self) -> None:
        """Exécute l'action associée à la présence dans l'état."""
        self._do_in_state_action()

    def _exec_exiting_action(self):
        """Exécute l'action associée à la sortie de l'état."""
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
