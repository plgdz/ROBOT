from enum import Enum, auto
from Transition import Transition
from State import State, MonitoredState
from time import perf_counter
from typing import List

class FiniteStateMachine:
    """
    Représente une machine à états finis (FSM) capable de passer d'un état à un autre en fonction de transitions prédéfinies.

    Attributs:
        __layout (Layout): La disposition de la machine à états finis contenant ses états et son état initial.
        __current_operational_state (OperationalState): L'état opérationnel actuel du FSM.
        __current_applicative_state (State): L'état applicatif actuel du FSM.

    Méthodes:
        __init__(layout: Layout, uninitialized: bool = True) -> None:
            Initialise la machine à états finis avec la disposition fournie.
        
        reset() -> None:
            Réinitialise la machine à états finis à son état initial.
        
        _transit_by(transition: Transition) -> None:
            Effectue une transition en fonction de la transition fournie.
        
        transit_to(state: State) -> None:
            Effectue une transition de la machine à états finis vers l'état spécifié.
        
        track() -> bool:
            Suit l'état actuel de la machine à états finis et effectue les actions nécessaires en fonction des transitions.
        
        start(reset: bool = True, time_budget: float = None) -> None:
            Démarre la machine à états finis, en la réinitialisant éventuellement et en la faisant fonctionner pendant un budget de temps spécifié.
        
        stop() -> None:
            Arrête la machine à états finis, en définissant son état opérationnel sur IDLE.

    Classes:
        Layout:
            Représente la disposition de la machine à états finis, contenant ses états et son état initial.
        
        OperationalState (Enum):
            Représente les états opérationnels de la machine à états finis.
    """

    class Layout:
        """
        Représente le layout de la machine à états finis, contenant ses états et son état initial.

        Attributs:
            __states (List[State]): La liste des états de la machine à états finis.
            initial_state (State): L'état initial de la machine à états finis.

        Méthodes:
            __init__() -> None:
                Initialise la disposition de la machine à états finis.
            
            add_state(state: State) -> None:
                Ajoute un état à la liste des états de la machine à états finis.
            
            add_states(states: List[State]) -> None:
                Ajoute une liste d'états à la liste des états de la machine à états finis.
        """

        def __init__(self) -> None:
            """
            Initialise la disposition de la machine à états finis.
            """
            self.__states: List[State] = []
            self.initial_state = None

        @property
        def initial_state(self) -> State:
            """
            Getter de l'état initial de la machine à états finis.
            """
            return self.__initial_state

        @initial_state.setter
        def initial_state(self, state) -> None:
            """
            Setter de l'état initial de la machine à états finis.

            Args:
                state (State): L'état initial de la machine à états finis.

            Raises:
                ValueError: L'état initial doit être de type State.
                ValueError: L'état initial doit être dans la liste des états ajoutés.
            """
            if state is not None and not isinstance(state, State):
                raise ValueError("initial_state must be of type State")
            if state is not None and state not in self.__states:
                raise ValueError("initial_state must be in the added list of states")
            self.__initial_state = state
        
        @property
        def valid(self) -> bool:
            """
            Verifie la validité du layout en verifiant la validite de chaque etat.

            Returns:
                bool: La validité de la disposition de la machine à états finis.
            """
            for state in self.__states:
                if not state.valid:
                    return False
            return self.__initial_state is not None
        
        @valid.setter
        def valid(self) -> None:
            raise ValueError("valid is a read-only property")
        
        def add_state(self, state) -> None:
            """
            Ajoute un état à la liste des états de la machine à états finis.

            Args:
                state (State): L'état à ajouter à la liste des états de la machine à états finis.

            Raises:
                ValueError: L'état doit être de type State.
                ValueError: L'état doit être unique.
            """
            if(not isinstance(state, State)):
                raise ValueError("state must be of type State. Actual type is " + str(type(state)) + ".")
            if state in self.__states:
                raise ValueError("state must be unique")
            self.__states.append(state)

        def add_states(self, states) -> None:
            """
            Ajoute une liste d'états à la liste des états de la machine à états finis.

            Args:
                states (List[State]): La liste des états à ajouter à la liste des états de la machine à états finis.

            Raises:
                ValueError: La liste des états doit être une liste.
            """
            for state in states:
                self.add_state(state)

    class OperationalState(Enum):
        """
        Représente les états opérationnels de la machine à états finis.
        """
        UNINITIALIZED = auto()
        IDLE = auto()
        RUNNING = auto()
        TERMINAL_REACHED = auto()

    def __init__(self, layout: Layout, uninitialized: bool = True):
        """
        Initialise la machine à états finis avec la disposition fournie.

        Args:
            layout (Layout): La disposition de la machine à états finis.
            uninitialized (bool): Indique si la machine à états finis doit être initialisée ou non.

        Raises:
            ValueError: Le layout n'est pas valide.
        """

        if not layout.valid:
            raise ValueError("layout is not valid")

        self.__layout = layout
        self.__current_applicative_state = layout.initial_state
        self.__current_operational_state = self.OperationalState.UNINITIALIZED

        if not uninitialized:
            self.reset()

    @property
    def current_operational_state(self) -> int:
        """
        Getter de l'état opérationnel actuel de la machine à états finis.

        Returns:
            int: L'état opérationnel actuel de la machine à états finis.
        """
        return self.__current_operational_state

    @current_operational_state.setter
    def current_operational_state(self) -> None:
        """
        Setter de l'état opérationnel actuel de la machine à états finis.

        Raises:
            ValueError: L'état opérationnel actuel est une propriété en lecture seule.
        """
        raise ValueError("current_operational_state is a read-only property")

    @property
    def current_applicative_state(self) -> State:
        """
        Getter de l'état applicatif actuel de la machine à états finis.

        Returns:
            State: L'état applicatif actuel de la machine à états finis.
        """
        return self.__current_applicative_state

    @current_applicative_state.setter
    def current_applicative_state(self) -> None:
        """
        Setter de l'état applicatif actuel de la machine à états finis.

        Raises:
            ValueError: L'état applicatif actuel est une propriété en lecture seule.
        """
        raise ValueError("current_applicative_state is a read-only property")

    def reset(self):
        """
        Réinitialise la machine à états finis à son état initial.
        """
        self.__current_operational_state = self.OperationalState.IDLE
        self.__current_applicative_state = self.__layout.initial_state

    def _transit_by(self, transition : Transition) -> None:
        """
        Effectue une transition en fonction de la transition fournie.
        
        Args:
            transition (Transition): La transition à effectuer.
        """
        self.current_applicative_state._exec_exiting_action()
        transition._exec_transiting_action()
        self.__current_applicative_state = transition.next_state
        self.current_applicative_state._exec_entering_action()

    def transit_to(self, state : State) -> None:
        """
        Effectue une transition de la machine à états finis vers l'état spécifié.

        Args:
            state (State): L'état vers lequel effectuer la transition.
        """
        self.current_applicative_state._exec_exiting_action()
        self.__current_applicative_state = state
        self.current_applicative_state._exec_entering_action()
        
    def track(self) -> bool:
        """
        Suit l'état actuel de la machine à états finis et effectue les actions nécessaires en fonction des transitions.

        Returns:
            bool: Indique si la machine à états finis est toujours en cours d'exécution.

        Raises:
            ValueError: current_applicative_state est None.
        """
        if self.current_applicative_state is None:
            raise ValueError("current_applicative_state is None")
        
        transition = self.current_applicative_state.transiting
            
        if transition:
            self._transit_by(transition)
        else:
            self.current_applicative_state._exec_in_state_action()

        if self.current_applicative_state.terminal:
            self.__current_operational_state = self.OperationalState.TERMINAL_REACHED
            return False
        return True
            
    
    def start(self, reset: bool = True, time_budget: float = None):
        """
        Démarre la machine à états finis, en la réinitialisant éventuellement et en la faisant fonctionner pendant un budget de temps spécifié.

        Args:
            reset (bool): Indique si la machine à états finis doit être réinitialisée.
            time_budget (float): Le budget de temps pour lequel la machine à états finis doit fonctionner.
        """
        if reset:
            self.reset()
        self.__current_operational_state = self.OperationalState.RUNNING
        self.current_applicative_state._exec_entering_action()
        run = True
        init_time = perf_counter()

        while ((time_budget is None) or (time_budget > perf_counter() - init_time)) and run:
            run = self.track()
            if not run:
                self.stop()

    def stop(self):
        """
        Arrête la machine à états finis, en définissant son état opérationnel sur IDLE.
        """
        self.__current_operational_state = self.OperationalState.IDLE
    

def main():
    pass
if __name__ == "__main__":
    main()