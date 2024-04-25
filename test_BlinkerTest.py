import unittest
from Blinker import Blinker
from State import MonitoredState
import time

class BlinkerTest(unittest.TestCase):
    def setUp(self) -> None:
        def off_state_generator() -> MonitoredState:
            off = MonitoredState()
            off.custom_value = "Off"
            return off
    
        def on_state_generator() -> MonitoredState:
            on = MonitoredState()
            on.custom_value = "On"
            return on
        
        self.blinker = Blinker(off_state_generator, on_state_generator)
        
    def test_blinker_is_off(self) -> None:
        self.assertEqual(True, self.blinker.is_off)

    def test_blinker_is_on(self) -> None:
        self.blinker.turn_on()
        self.assertEqual(True, self.blinker.is_on)

    def test_blinker_initial_state(self) -> None:
        self.assertEqual(True, self.blinker.is_off)

    def test_blinker_on(self) -> None:
        self.blinker.turn_on()
        self.assertEqual(True, self.blinker.is_on)

    def test_blinker_off(self) -> None:
        self.blinker.turn_on()
        self.blinker.turn_off()
        self.assertEqual("Off", self.blinker.current_applicative_state.custom_value)

    def test_blinker_blink(self) -> None:
        duration = 0.6
        self.blinker.blink(cycle_duration=1, percent_on=0.5, begin_on=True)
        t_start = time.perf_counter()
        self.blinker.track()
        self.assertEqual("On", self.blinker.current_applicative_state.custom_value)
        while time.perf_counter() - t_start < duration:
            self.blinker.track()    
        self.assertEqual("Off", self.blinker.current_applicative_state.custom_value)

    def test_blinker_blink_off(self) -> None:
        duration = 0.6
        self.blinker.blink(cycle_duration=1, percent_on=0.5, begin_on=False)
        t_start = time.perf_counter()
        self.blinker.track()
        self.assertEqual("Off", self.blinker.current_applicative_state.custom_value)
        while time.perf_counter() - t_start < duration:
            self.blinker.track()    
        self.assertEqual("On", self.blinker.current_applicative_state.custom_value)

    def test_blinker_total_duration(self) -> None:
        duration = 2
        t_start = time.perf_counter()
        self.blinker.blink(total_duration=duration, cycle_duration=1, percent_on=0.5, begin_on=True, end_off=True)
        self.blinker.track()
        self.assertEqual("On", self.blinker.current_applicative_state.custom_value)
        while time.perf_counter() - t_start < duration :
            self.blinker.track()
        self.assertAlmostEqual(duration, self.blinker.current_applicative_state.last_exit_time, delta=0.3)
        self.assertEqual("Off", self.blinker.current_applicative_state.custom_value)



if __name__ == '__main__':
    unittest.main()
