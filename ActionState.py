from State import State, Parameters

class ActionState(State):

    class Action:
        def __init__(self) -> None:
            self.action = callable[[], None]

    def __init__(self, parameters: Parameters = Parameters()) -> None:
        """Initialise une instance de State.

        Args :
            parameters (Parameters) : Les paramètres de comportement de l'état. Par défaut à une instance vide de Parameters.
        """
        super().__init__(parameters)
        self.__entering_actions  : self.Action = set()
        self.__in_state_actions : self.Action = set()
        self.__exiting_actions : self.Action = set()

    def _do_entering_action(self) -> None:
        super()._do_entering_action()

    def _do_in_state_action(self) -> None:
        super()._do_in_state_action()

    def _do_exiting_action(self) -> None:
        super()._do_exiting_action()

    def add_entering_action(self, action: Action) -> None:
        """Ajoute une action à exécuter à l'entrée de l'état.

        Args :
            action (Action) : L'action à exécuter.
        """
        if not isinstance(action, self.Action):
            raise TypeError("L'action doit être une instance de Action.")
        self.__entering_actions.add(action)

    def add_in_state_action(self, action: Action) -> None:
        """Ajoute une action à exécuter pendant l'état.

        Args :
            action (Action) : L'action à exécuter.
        """
        if not isinstance(action, self.Action):
            raise TypeError("L'action doit être une instance de Action.")
        self.__in_state_actions.add(action)

    def add_exiting_action(self, action: Action) -> None:
        """Ajoute une action à exécuter à la sortie de l'état.

        Args :
            action (Action) : L'action à exécuter.
        """
        if not isinstance(action, self.Action):
            raise TypeError("L'action doit être une instance de Action.")
        self.__exiting_actions.add(action) 