# Version: 1.0
import random
from typing import Callable, List, Optional, TYPE_CHECKING
import time
from Robot import Robot
if TYPE_CHECKING:
    from Transition import Transition
    from Robot import Robot
    from FiniteStateMachine import FiniteStateMachine

class State:
    """Représente un état dans une machine à états.

    Cette classe contient des informations sur un état au sein d'une machine à états, incluant ses paramètres
    et ses transitions vers d'autres états.

    Attributs :
        parameters (Parameters) : Les paramètres définissant le comportement de l'état.
        __transitions (set) : Un ensemble de transitions de cet état vers d'autres états.

    Méthodes :
        valid : Vérifie si l'état a des transitions valides.
        terminal : Indique si l'état est terminal.
        transiting : Liste les statuts de transition.
        add_transition : Ajoute une transition à l'état.
        _exec_entering_action : Exécute l'action associée à l'entrée dans l'état.
        _exec_in_state_action : Exécute l'action associée à la présence dans l'état.
        _exec_exiting_action : Exécute l'action associée à la sortie de l'état.
        _do_entering_action : Définit l'action à exécuter à l'entrée de l'état.
        _do_in_state_action : Définit l'action à exécuter pendant la présence dans l'état.
        _do_exiting_action : Définit l'action à exécuter à la sortie de l'état.
    """

    class Parameters:
        """Paramètres définissant le comportement d'un état dans une machine à états.

        Attributs :
            terminal (bool) : Indicateur si l'état est terminal.
            do_in_state_action_when_entering (bool) : Indicateur si une action doit être exécutée en entrant dans l'état.
            do_in_state_action_when_exiting (bool) : Indicateur si une action doit être exécutée en sortant de l'état.

        Méthodes :
            __init__ : Initialise les paramètres pour un état.
        """

        def __init__(self, terminal: bool = False, do_in_state_action_when_entering: bool = False, do_in_state_action_when_exiting: bool = False):
            """Initialise les paramètres pour un état.

            Args :
                terminal (bool) : Si l'état est terminal. Par défaut à False.
                do_in_state_action_when_entering (bool) : Si une action doit être exécutée à l'entrée. Par défaut à False.
                do_in_state_action_when_exiting (bool) : Si une action doit être exécutée à la sortie. Par défaut à False.

            Raises :
                TypeError : Si les paramètres ne sont pas des booléens.

            Utilisation :
                >>> State.Parameters(terminal=True, do_in_state_action_when_entering=True, do_in_state_action_when_exiting=True)
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

        Utilisation :
            >>> State()
            >>> State(State.Parameters())

        """
        
        self.parameters : State.Parameters = parameters if parameters is not None else self.Parameters()
        self.__transitions = []

    @property
    def valid(self) -> bool:
        """Vérifie si l'état a des transitions valides.

        Retourne :
            bool : True si toutes les transitions sont valides, False autrement.

        Utilisation :
            >>> state.valid
        """
        if not self.__transitions or not all(transition.valid for transition in self.__transitions):
            if self.terminal:
                return True
            return False
        return True

    @property
    def terminal(self) -> bool:
        """Indique si l'état est terminal.

        Retourne :
            bool : True si l'état est terminal, False autrement.

        Utilisation :
            >>> state.terminal
        """
        return self.parameters.terminal

    @property
    def transiting(self) -> bool:
        """Liste les statuts de transition.

        Retourne :
            bool : La transition en cours, None autrement.

        Utilisation :
            >>> state.transiting
        """
        for transition in self.__transitions:
            if transition.transiting:
                return transition
        return None

    def add_transition(self, transition: 'Transition'):
        """Ajoute une transition à l'état.

        Args :
            transition (Transition) : La transition à ajouter.

        Raises :
            TypeError : Si la transition n'est pas une instance de Transition.
            ValueError : Si la transition est déjà ajoutée.

        Utilisation :
            >>> state.add_transition(transition)
        """
        from Transition import Transition
        if not isinstance(transition, Transition):
            raise TypeError("La transition doit être une instance de Transition.")
        if transition in self.__transitions:
            raise ValueError("La transition est déjà ajoutée.")
        self.__transitions.append(transition)

    def _exec_entering_action(self) -> None:
        """
        Exécute l'action associée à l'entrée dans l'état.

        Utilisation :
            >>> state._exec_entering_action()
        """
        self._do_entering_action()
        if self.parameters.do_in_state_action_when_entering:
            self._exec_in_state_action()

    def _exec_in_state_action(self) -> None:
        """
        Exécute l'action associée à la présence dans l'état.
        
        Utilisation :
            >>> state._exec_in_state_action()
        """
        self._do_in_state_action()

    def _exec_exiting_action(self) -> None:
        """
        Exécute l'action associée à la sortie de l'état.
        
        Utilisation :
            >>> state._exec_exiting_action()
        """
        if self.parameters.do_in_state_action_when_exiting:
            self._exec_in_state_action()
        self._do_exiting_action()
        

    def _do_entering_action(self) -> None:
        """
        Définit l'action à exécuter à l'entrée de l'état.
        
        Utilisation :
            >>> state._do_entering_action()
        """
        pass

    def _do_in_state_action(self) -> None:
        """
        Définit l'action à exécuter pendant la présence dans l'état.
        
        Utilisation :
            >>> state._do_in_state_action()
        """
        pass

    def _do_exiting_action(self) -> None:
        """
        Définit l'action à exécuter à la sortie de l'état.
        
        Utilisation :
            >>> state._do_exiting_action()
        """
        pass

class ActionState(State):
    """
    ActionState est une classe dérivée de State qui permet d'ajouter des actions à exécuter à l'entrée, pendant et à la sortie de l'état.

    Attributs :
        __entering_actions (List[Callable[[], None]]) : La liste des actions à exécuter à l'entrée de l'état.
        __in_state_actions (List[Callable[[], None]]) : La liste des actions à exécuter pendant la présence dans l'état.
        __exiting_actions (List[Callable[[], None]]) : La liste des actions à exécuter à la sortie de l'état.  

    Méthodes :
        add_entering_action : Ajoute une action à exécuter à l'entrée de l'état.
        add_in_state_action : Ajoute une action à exécuter pendant la présence dans l'état.
        add_exiting_action : Ajoute une action à exécuter à la sortie de l'état.
        _do_entering_action : Exécute l'action associée à l'entrée dans l'état.
        _do_in_state_action : Exécute l'action associée à la présence dans l'état.
        _do_exiting_action : Exécute l'action associée à la sortie de l'état.
    """

    Action = Callable[[], None]

    def __init__(self, parameters: Optional[State.Parameters] = None) -> None:
        """
        Initialise une instance de State.

        Args :
            parameters (Parameters) : Les paramètres de comportement de l'état. Par défaut à une instance vide de Parameters.

        Utilisation :
            >>> ActionState()
            >>> ActionState(State.Parameters())
        """
        super().__init__(parameters)
        self.__entering_actions : List[self.Action] = []
        self.__in_state_actions : List[self.Action] = []
        self.__exiting_actions : List[self.Action] = []

    def _do_entering_action(self) -> None:
        """
        Exécute l'action associée à l'entrée dans l'état.

        Utilisation :
            >>> state._do_entering_action()
        """
        super()._do_entering_action()
        for action in self.__entering_actions:
            action()

    def _do_in_state_action(self) -> None:
        """
        Exécute l'action associée à la présence dans l'état.

        Utilisation :
            >>> state._do_in_state_action()
        """
        super()._do_in_state_action()
        for action in self.__in_state_actions:
            action()

    def _do_exiting_action(self) -> None:
        """
        Exécute l'action associée à la sortie de l'état.

        Utilisation :
            >>> state._do_exiting_action()
        """
        super()._do_exiting_action()
        for action in self.__exiting_actions:
            action()

    def add_entering_action(self, action: Action) -> None:
        """Ajoute une action à exécuter à l'entrée de l'état.

        Args :
            action (Action) : L'action à exécuter.

        Raises :
            TypeError : Si l'action n'est pas une instance de Action.

        Utilisation :
            >>> state.add_entering_action(action)
        """
        if not callable(action):
            raise TypeError("L'action doit être une instance de Action.")
        self.__entering_actions.append(action)

    def add_in_state_action(self, action: Action) -> None:
        """Ajoute une action à exécuter pendant l'état.

        Args :
            action (Action) : L'action à exécuter.

        Raises :
            TypeError : Si l'action n'est pas une instance de Action.

        Utilisation :
            >>> state.add_in_state_action(action)
        """
        if not callable(action):
            raise TypeError("L'action doit être une instance de Action.")
        self.__in_state_actions.append(action)

    def add_exiting_action(self, action: Action) -> None:
        """Ajoute une action à exécuter à la sortie de l'état.

        Args :
            action (Action) : L'action à exécuter.

        Raises :
            TypeError : Si l'action n'est pas une instance de Action.

        Utilisation :
            >>> state.add_exiting_action(action)
        """
        if not callable(action):
            raise TypeError("L'action doit être une instance de Action.")
        self.__exiting_actions.append(action) 

class MonitoredState(ActionState):

    """
    MonitoredState est une classe dérivée de ActionState qui permet de suivre les entrées et sorties de l'état.

    Attributs :
        __counter_last_entry (float) : Le compteur de la dernière entrée dans l'état.
        __counter_last_exit (float) : Le compteur de la dernière sortie de l'état.
        __entry_count (int) : Le nombre d'entrées dans l'état.
        custom_value (any) : Une valeur personnalisée pour l'état.

    Méthodes :
        entry_count : Obtient le nombre d'entrées dans l'état.
        last_entry_time : Obtient le compteur de la dernière entrée dans l'état.
        last_exit_time : Obtient le compteur de la dernière sortie de l'état.
        reset_entry_count : Réinitialise le compteur d'entrées.
        reset_last_times : Réinitialise les compteurs de temps.
        _exec_entering_action : Exécute l'action associée à l'entrée dans l'état.
        _exec_exiting_action : Exécute l'action associée à la sortie de l'état. 
    """

    def __init__(self, parameters: Optional[State.Parameters] = None) -> None:
        """Initialise une instance de State.

        Args :
            parameters (Parameters) : Les paramètres de comportement de l'état. Par défaut à une instance vide de Parameters.

        Utilisation :
            >>> MonitoredState()
            >>> MonitoredState(State.Parameters())
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

        Utilisation :
            >>> state.entry_count
        """
        return self.__entry_count
    
    @property
    def last_entry_time(self) -> float:
        """Obtient le compteur de la dernière entrée dans l'état.

        Retourne :
            float : Le compteur de la dernière entrée dans l'état.

        Utilisation :
            >>> state.last_entry_time
        """
        return self.__counter_last_entry
    
    
    @property
    def last_exit_time(self) -> float:
        """Obtient le compteur de la dernière sortie de l'état.

        Retourne :
            float : Le compteur de la dernière sortie de l'état.

        Utilisation :
            >>> state.last_exit_time
        """
        return self.__counter_last_exit
    
    def reset_entry_count(self) -> None:
        """
        Réinitialise le compteur d'entrées.
        
        Utilisation :
            >>> state.reset_entry_count()
        """
        self.__entry_count = 0

    def reset_last_times(self) -> None:
        """
        Réinitialise les compteurs de temps.
        
        Utilisation :
            >>> state.reset_last_times()
        """
        self.__counter_last_entry = 0
        self.__counter_last_exit = 0

    def _exec_entering_action(self) -> None:
        """
        Exécute l'action associée à l'entrée dans l'état.
        
        Utilisation :
            >>> state._exec_entering_action()
        """
        self.__counter_last_entry = time.perf_counter()
        self.__entry_count += 1
        super()._exec_entering_action()

    def _exec_exiting_action(self) -> None:
        """
        Exécute l'action associée à la sortie de l'état.
        
        Utilisation :
            >>> state._exec_exiting_action()
        """
        super()._exec_exiting_action()
        self.__counter_last_exit = time.perf_counter()
        
class TaskState(MonitoredState):
    def __init__(self, parameters: Optional[State.Parameters] = None) -> None:
        """Initialise une instance de State.

        Args :
            parameters (Parameters) : Les paramètres de comportement de l'état. Par défaut à une instance vide de Parameters.

        Utilisation :
            >>> TaskState()
            >>> TaskState(State.Parameters())
        """
        super().__init__(parameters)
        self.__task_value : 'FiniteStateMachine' = None

    @property
    def task_value(self) -> 'FiniteStateMachine':
        return self.__task_value
    
    @task_value.setter
    def task_value(self, value: 'FiniteStateMachine') -> None:
        from FiniteStateMachine import FiniteStateMachine
        if not isinstance(value, FiniteStateMachine):
            raise TypeError("task_value must be of type FiniteStateMachine")
        self.__task_value = value

class RobotState(State):
    def __init__(self, robot: 'Robot', parameters: Optional[State.Parameters] = None):
        from Robot import Robot
        if not isinstance(robot, Robot):
            raise TypeError("robot must be of type Robot")
        super().__init__(parameters)  
        self._robot: Robot = robot

class ManualControlState(RobotState):
    from Robot import Robot
    def __init__(self, robot: 'Robot', move_configuration, parameters: Optional[State.Parameters] = None, side : 'Robot.Side' = None, cycle_duration : float = 1.0, percent_on: float = .5, begin_on : bool = True, off=False):
        self.off = off
        self.__move_config = move_configuration
        self.side = side
        self.cycle_duration = cycle_duration
        self.percent_on = percent_on
        self.begin_on = begin_on
        super().__init__(robot, parameters)
        
    def _do_entering_action(self) -> None:
        super()._do_entering_action()
        if self.off:
            self._robot.turn_off_left_led()
            self._robot.turn_off_right_led()
        else:
            print(self.side, self.cycle_duration, self.percent_on, self.begin_on)
            self._robot.led_blinker.blink(self.side, cycle_duration = self.cycle_duration, percent_on=self.percent_on, begin_on=self.begin_on)
        self._robot.move(self.__move_config)
            
    def _do_in_state_action(self) -> None:
        if self.off:
            self._robot.turn_off_left_led()
            self._robot.turn_off_right_led()
        self._robot.led_blinker.track()
        self._robot.eye_blinker.track()
        super()._do_in_state_action()
        
    def _do_exiting_action(self) -> None:
        super()._do_exiting_action()
        self._robot.led_blinker.track()
        self._robot.move(Robot.MoveDirection.STOP)

class WonderState(MonitoredState):
    from Robot import Robot
    def __init__(self, robot: 'Robot', parameters: Optional[State.Parameters] = None, side : 'Robot.Side' = None, cycle_duration : float = 1.0, percent_on: float = .5, begin_on : bool = True, off=False):
        self.off = off
        self.side = side
        self.cycle_duration = cycle_duration
        self.percent_on = percent_on
        self.begin_on = begin_on
        super().__init__(robot)
        
    def __random_move(self):
        return random.choice([Robot.MoveDirection.FORWARD, Robot.MoveDirection.LEFT, Robot.MoveDirection.RIGHT])
    
    def _do_entering_action(self) -> None:
        super()._do_entering_action()
        if self.off:
            self._robot.turn_off_left_led()
            self._robot.turn_off_right_led()
        else:
            print(self.side, self.cycle_duration, self.percent_on, self.begin_on)
            self._robot.led_blinker.blink(self.side, cycle_duration = self.cycle_duration, percent_on=self.percent_on, begin_on=self.begin_on)
        self._robot.move(self.__random_move())
            
    def _do_in_state_action(self) -> None:
        if self.off:
            self._robot.turn_off_left_led()
            self._robot.turn_off_right_led()
        self._robot.led_blinker.track()
        self._robot.eye_blinker.track()
        super()._do_in_state_action()
        
    def _do_exiting_action(self) -> None:
        super()._do_exiting_action()
        self._robot.led_blinker.track()
        self._robot.move(Robot.MoveDirection.STOP)