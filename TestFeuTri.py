import unittest

from FiniteStateMachine import FiniteStateMachine
from State import MonitoredState, ActionState
from Transition import ConditionalTransition, MonitoredTransition, ActionTransition
from Condition import StateEntryDurationCondition, StateValueCondition

class TestFeuTriValue(unittest.TestCase):
    def setUp(self) -> None:
        self.green = MonitoredState()
        self.green.custom_value = "Green"
        self.green.add_in_state_action(lambda : print(f"Green", end="                  \r"))

        self.yellow = MonitoredState()
        self.yellow.custom_value = "Yellow"
        self.yellow.add_in_state_action(lambda : print(f"Yellow", end="                  \r"))

        self.red = MonitoredState()
        self.red.custom_value = "Red"
        self.red.add_in_state_action(lambda : print(f"Red", end="                  \r"))

        self.green_to_yellow = ConditionalTransition(next_state=self.yellow, condition=StateValueCondition(expected_value='Green', monitored_state=self.green))
        self.green.add_transition(self.green_to_yellow)

        self.yellow_to_red = ConditionalTransition(next_state=self.red, condition=StateValueCondition(expected_value='Yellow', monitored_state=self.yellow))
        self.yellow.add_transition(self.yellow_to_red)

        self.red_to_green = ConditionalTransition(next_state=self.green, condition=StateValueCondition(expected_value='Red', monitored_state=self.red))
        self.red.add_transition(self.red_to_green)

        
        self.layout = FiniteStateMachine.Layout()
        self.layout.add_states([self.green, self.yellow, self.red])
        self.layout.initial_state = self.green
        self.feu = FiniteStateMachine(layout=self.layout)

    def test_green_to_yellow(self):
        self.feu.track()
        self.assertEqual(self.feu.current_applicative_state, self.yellow)

    def test_yellow_to_red(self):
        self.feu.track()
        self.feu.track()
        self.assertEqual(self.feu.current_applicative_state, self.red)

    def test_red_to_green(self):
        self.feu.track()
        self.feu.track()
        self.feu.track()
        self.assertEqual(self.feu.current_applicative_state, self.green)

    def test_red_to_green_to_yellow(self):
        self.feu.track()
        self.feu.track()
        self.feu.track()
        self.feu.track()
        self.assertEqual(self.feu.current_applicative_state, self.yellow)

if __name__ == "__main__":
    unittest.main()
