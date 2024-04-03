from ActionState import ActionState, Action, Parameters

class MonitoredState(ActionState):
    def __init__(self, parameters: Parameters = Parameters()) -> None:
        """Initialise une instance de State.

        Args :
            parameters (Parameters) : Les paramètres de comportement de l'état. Par défaut à une instance vide de Parameters.
        """
        super().__init__(parameters)
        self.__counter_last_entry : int = 0
        self.__counter_last_exit : int = 0