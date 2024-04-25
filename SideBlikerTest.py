import unittest
from Blinker import SideBlinker
from State import MonitoredState
import time

class SideBlinkerTest(unittest.TestCase):
    def setUp(self) -> None:
        def off_state_generator() -> MonitoredState:
            off = MonitoredState()
            off.custom_value = "Off"
            return off
    
        def on_state_generator() -> MonitoredState:
            on = MonitoredState()
            on.custom_value = "On"
            return on
        
        self.side_blinker = SideBlinker(
            off_state_generator,
            on_state_generator,
            off_state_generator,
            on_state_generator
        )

    def test_blinker_initial_state(self) -> None:
        self.assertEqual("Off", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
        self.assertEqual("Off", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)

    def test_turn_off(self):
        for side in SideBlinker.Side:
            self.side_blinker.turn_off(side)
            if side == SideBlinker.Side.LEFT:
                self.assertEqual("Off", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
            elif side == SideBlinker.Side.RIGHT:
                self.assertEqual("Off", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)
            elif side == SideBlinker.Side.BOTH:
                self.assertEqual("Off", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
                self.assertEqual("Off", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)
            elif side == SideBlinker.Side.LEFT_RECIPROCAL:
                self.assertEqual("Off", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
                self.assertEqual("On", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)
            elif side == SideBlinker.Side.RIGHT_RECIPROCAL:
                self.assertEqual("On", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
                self.assertEqual("Off", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)

    def test_turn_on(self):
        for side in SideBlinker.Side:
            self.side_blinker.turn_on(side)
            if side == SideBlinker.Side.LEFT:
                self.assertEqual("On", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
            elif side == SideBlinker.Side.RIGHT:
                self.assertEqual("On", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)
            elif side == SideBlinker.Side.BOTH:
                self.assertEqual("On", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
                self.assertEqual("On", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)
            elif side == SideBlinker.Side.LEFT_RECIPROCAL:
                self.assertEqual("On", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
                self.assertEqual("Off", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)
            elif side == SideBlinker.Side.RIGHT_RECIPROCAL:
                self.assertEqual("Off", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
                self.assertEqual("On", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)

    def test_blink_case_one(self):
        for side in SideBlinker.Side:
            self.side_blinker.turn_off(SideBlinker.Side.BOTH)
            self.side_blinker.blink(side, cycle_duration=1, percent_on=0.5, begin_on=True)
            t_start = time.perf_counter()
            self.side_blinker._SideBlinker__left_blinker.track()
            self.side_blinker._SideBlinker__right_blinker.track()
            if side == SideBlinker.Side.LEFT:
                self.assertEqual("On", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
                self.assertEqual("Off", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)
            elif side == SideBlinker.Side.RIGHT:
                self.assertEqual("Off", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
                self.assertEqual("On", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)
            elif side == SideBlinker.Side.BOTH:
                self.assertEqual("On", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
                self.assertEqual("On", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)
            elif side == SideBlinker.Side.LEFT_RECIPROCAL:
                self.assertEqual("On", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
                self.assertEqual("Off", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)
            elif side == SideBlinker.Side.RIGHT_RECIPROCAL:
                self.assertEqual("Off", self.side_blinker._SideBlinker__left_blinker.current_applicative_state.custom_value)
                self.assertEqual("On", self.side_blinker._SideBlinker__right_blinker.current_applicative_state.custom_value)

    

if __name__ == '__main__':
    unittest.main()
    