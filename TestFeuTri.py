import unittest
from State import State, ActionState, MonitoredState
from typing import Callable, List, Optional
from unittest.mock import Mock


class TestActionState(unittest.TestCase):

    def test_add_entering_action(self):
        state = ActionState()
        action = Mock()
        state.add_entering_action(action)
        state._do_entering_action()
        action.assert_called_once()

    def test_add_in_state_action(self):
        state = ActionState()
        action = Mock()
        state.add_in_state_action(action)
        state._do_in_state_action()
        action.assert_called_once()

    def test_add_exiting_action(self):
        state = ActionState()
        action = Mock()
        state.add_exiting_action(action)
        state._do_exiting_action()
        action.assert_called_once()

    def test_add_entering_action_raises_type_error(self):
        state = ActionState()
        with self.assertRaises(TypeError):
            state.add_entering_action("not a callable")

    def test_add_in_state_action_raises_type_error(self):
        state = ActionState()
        with self.assertRaises(TypeError):
            state.add_in_state_action("not a callable")

    def test_add_exiting_action_raises_type_error(self):
        state = ActionState()
        with self.assertRaises(TypeError):
            state.add_exiting_action("not a callable")

class TestMonitoredState(unittest.TestCase):
    def setUp(self):
        # Initialisation standard pour chaque test
        self.monitored_state = MonitoredState()

    def test_entry_count_increment(self):
        # Vérifie que le compteur d'entrées est bien incrémenté
        initial_count = self.monitored_state.entry_count
        self.monitored_state._exec_entering_action()
        self.assertEqual(self.monitored_state.entry_count, initial_count + 1)

    def test_last_entry_time_update(self):
        # Vérifie que le compteur de dernière entrée est mis à jour
        self.monitored_state._exec_entering_action()
        self.assertNotEqual(self.monitored_state.last_entry_time, 0)

    def test_last_exit_time_update(self):
        # Vérifie que le compteur de dernière sortie est mis à jour
        self.monitored_state._exec_exiting_action()
        self.assertNotEqual(self.monitored_state.last_exit_time, 0)

    def test_reset_entry_count(self):
        # Teste la réinitialisation du compteur d'entrées
        self.monitored_state._exec_entering_action()
        self.monitored_state.reset_entry_count()
        self.assertEqual(self.monitored_state.entry_count, 0)

    def test_reset_last_times(self):
        # Teste la réinitialisation des compteurs de temps
        self.monitored_state._exec_entering_action()
        self.monitored_state._exec_exiting_action()
        self.monitored_state.reset_last_times()
        self.assertEqual(self.monitored_state.last_entry_time, 0)
        self.assertEqual(self.monitored_state.last_exit_time, 0)

if __name__ == "__main__":
    unittest.main()
