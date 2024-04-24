from enum import Enum
from typing import TypeAlias
from FiniteStateMachine import FiniteStateMachine
from State import MonitoredState
from Transition import MonitoredTransition
from Condition import AllConditions, Condition, StateEntryDurationCondition, StateValueCondition

def set_road_status(*args):
    pass
def get_day_period():
    pass
class RoadType(Enum):
    pass
class LightColor(Enum):
    pass
class LightStatus(Enum):
    pass
class DayPeriod(Enum):
    pass

class MainSecRoadsIntersectionController(FiniteStateMachine):

	State: TypeAlias = MonitoredState
	Transition: TypeAlias = MonitoredTransition

	def __init__(self):

		#creation des actions
		def set_primary_red_off():
			set_road_status(RoadType.MAIN, LightColor.RED, LightStatus.OFF)

		def set_primary_green_off():
			set_road_status(RoadType.MAIN, LightColor.GREEN, LightStatus.OFF)

		def set_primary_yellow_off():
			set_road_status(RoadType.MAIN, LightColor.YELLOW, LightStatus.OFF)

		def set_primary_red_on():
			set_road_status(RoadType.MAIN, LightColor.RED, LightStatus.ON)

		def set_primary_green_on():
			set_road_status(RoadType.MAIN, LightColor.GREEN, LightStatus.ON)

		def set_primary_yellow_on():
			set_road_status(RoadType.MAIN, LightColor.YELLOW, LightStatus.ON)

		def set_secondary_red_off():
			set_road_status(RoadType.SECONDARY , LightColor.RED, LightStatus.OFF)

		def set_secondary_green_off():
			set_road_status(RoadType.SECONDARY , LightColor.GREEN, LightStatus.OFF)

		def set_secondary_yellow_off():
			set_road_status(RoadType.SECONDARY , LightColor.YELLOW, LightStatus.OFF)

		def set_secondary_red_on():
			set_road_status(RoadType.SECONDARY , LightColor.RED, LightStatus.ON)

		def set_secondary_green_on():
			set_road_status(RoadType.SECONDARY , LightColor.GREEN, LightStatus.ON)

		def set_secondary_yellow_on():
			set_road_status(RoadType.SECONDARY , LightColor.YELLOW, LightStatus.ON)


		#creation de states

		# initial state # PLUSIEUR TRANSITIONS
		self.initialization: MainSecRoadsIntersectionController.State = MonitoredState()
		self.initialization.add_entering_action(set_primary_red_on)
		self.initialization.add_entering_action(set_secondary_red_on)
		self.initialization.add_exiting_action(set_primary_red_off)
		self.initialization.add_exiting_action(set_secondary_red_off)
		self.initialization.custom_value = get_day_period()

		# main_red state
		self.main_red: MainSecRoadsIntersectionController.State = MonitoredState()
		self.main_red.add_entering_action(set_primary_red_on)
		self.main_red.add_entering_action(set_secondary_red_on)
		self.main_red.add_exiting_action(set_primary_red_off)
		self.main_red.add_exiting_action(set_secondary_red_off)

		# main_green state
		self.main_green: MainSecRoadsIntersectionController.State = MonitoredState()
		self.main_green.add_entering_action(set_primary_green_on)
		self.main_green.add_entering_action(set_secondary_red_on)
		self.main_green.add_exiting_action(set_primary_green_off)
		self.main_green.add_exiting_action(set_secondary_red_off)

		# main_yellow state
		self.main_yellow: MainSecRoadsIntersectionController.State = MonitoredState()
		self.main_yellow.add_entering_action(set_primary_yellow_on)
		self.main_yellow.add_entering_action(set_secondary_red_on)
		self.main_yellow.add_exiting_action(set_primary_yellow_off)
		self.main_yellow.add_exiting_action(set_secondary_red_off)

		# secondary_red state # PLUSIEUR TRANSITIONS
		self.secondary_red: MainSecRoadsIntersectionController.State = MonitoredState()
		self.secondary_red.add_entering_action(set_primary_red_on)
		self.secondary_red.add_entering_action(set_secondary_red_on)
		self.secondary_red.add_in_state_action(lambda: setattr(self, 'custom_value', get_day_period()))
		self.secondary_red.add_exiting_action(set_primary_red_off)
		self.secondary_red.add_exiting_action(set_secondary_red_off)

		# secondary_green state
		self.secondary_green: MainSecRoadsIntersectionController.State = MonitoredState()
		self.secondary_green.add_entering_action(set_primary_red_on)
		self.secondary_green.add_entering_action(set_secondary_green_on)
		self.secondary_green.add_exiting_action(set_primary_red_off)
		self.secondary_green.add_exiting_action(set_secondary_green_off)

		# secondary_yellow state
		self.secondary_yellow: MainSecRoadsIntersectionController.State = MonitoredState()
		self.secondary_yellow.add_entering_action(set_primary_red_on)
		self.secondary_yellow.add_entering_action(set_secondary_yellow_on)
		self.secondary_yellow.add_exiting_action(set_primary_red_off)
		self.secondary_yellow.add_exiting_action(set_secondary_yellow_off)

		# flashing_main state # PLUSIEUR TRANSITIONS
		self.flashing_main: MainSecRoadsIntersectionController.State = MonitoredState()
		self.flashing_main.add_entering_action(set_primary_yellow_on)
		self.flashing_main.add_in_state_action(lambda: setattr(self, 'custom_value', get_day_period()))
		self.flashing_main.add_exiting_action(set_primary_yellow_off)

		# flashing_secondary state
		self.flashing_secondary: MainSecRoadsIntersectionController.State = MonitoredState()
		self.flashing_main.add_entering_action(set_secondary_red_on)
		self.flashing_main.add_exiting_action(set_secondary_red_off)

		#creations des conditions et transitions
		day_condition= AllConditions()
		day_condition.add_condition(StateEntryDurationCondition(duration=120, monitored_state=self.initialization))
		day_condition.add_condition(StateValueCondition(expected_value=DayPeriod.DAY, monitored_state=self.initialization))
		from_initialization_to_main_red: MainSecRoadsIntersectionController.Transition = MonitoredTransition(next_state=self.main_red, condition=day_condition)

		night_condition= AllConditions()
		night_condition.add_condition(StateEntryDurationCondition(duration=120, monitored_state=self.initialization))
		night_condition.add_condition(StateValueCondition(expected_value=DayPeriod.NIGHT, monitored_state=self.initialization))
		from_initialization_to_flashing_main: MainSecRoadsIntersectionController.Transition = MonitoredTransition(next_state=self.flashing_main, condition=night_condition)

		self.initialization.add_transition(from_initialization_to_main_red)
		self.initialization.add_transition(from_initialization_to_flashing_main)

		# day transitions
		from_main_red_to_main_green: MainSecRoadsIntersectionController.Transition = MonitoredTransition(next_state=self.main_green, condition=StateEntryDurationCondition(duration=7, monitored_state=self.main_red))
		self.main_red.add_transition(from_main_red_to_main_green)

		from_main_green_to_main_yellow: MainSecRoadsIntersectionController.Transition = MonitoredTransition(next_state=self.main_yellow, condition=StateEntryDurationCondition(duration=120, monitored_state=self.main_green))
		self.main_green.add_transition(from_main_green_to_main_yellow)

		from_main_yellow_to_secondary_red: MainSecRoadsIntersectionController.Transition = MonitoredTransition(next_state=self.secondary_red, condition=StateEntryDurationCondition(duration=8, monitored_state=self.main_yellow))
		self.main_yellow.add_transition(from_main_yellow_to_secondary_red)

		night_condition = StateValueCondition(expected_value=DayPeriod.NIGHT, monitored_state=self.secondary_red)
		from_secondary_red_to_flashing_secondary: MainSecRoadsIntersectionController.Transition = MonitoredTransition(next_state=self.flashing_secondary, condition=night_condition)
		from_secondary_red_to_secondary_green: MainSecRoadsIntersectionController.Transition = MonitoredTransition(next_state=self.secondary_green, condition=StateEntryDurationCondition(duration=6, monitored_state=self.secondary_red))
		self.secondary_red.add_transition(from_secondary_red_to_flashing_secondary)
		self.secondary_red.add_transition(from_secondary_red_to_secondary_green)

		from_secondary_green_to_secondary_yellow: MainSecRoadsIntersectionController.Transition = MonitoredTransition(next_state=self.secondary_yellow, condition=StateEntryDurationCondition(duration=62, monitored_state=self.secondary_green))
		self.secondary_green.add_transition(from_secondary_green_to_secondary_yellow)

		from_secondary_yellow_to_main_red: MainSecRoadsIntersectionController.Transition = MonitoredTransition(next_state=self.main_red, condition=StateEntryDurationCondition(duration=7, monitored_state=self.secondary_yellow))
		self.secondary_yellow.add_transition(from_secondary_yellow_to_main_red)

		# night transitions
		day_condition = StateValueCondition(expected_value=DayPeriod.DAY, monitored_state=self.flashing_main)
		from_flashing_main_to_main_yellow: MainSecRoadsIntersectionController.Transition = MonitoredTransition(next_state=self.main_yellow, condition=day_condition)
		from_flashing_main_to_flashing_secondary: MainSecRoadsIntersectionController.Transition = MonitoredTransition(next_state=self.flashing_secondary, condition=StateEntryDurationCondition(duration=1, monitored_state=self.flashing_main))
		self.flashing_main.add_transition(from_flashing_main_to_main_yellow)
		self.flashing_main.add_transition(from_flashing_main_to_flashing_secondary)

		from_flashing_secondary_to_flashing_main: MainSecRoadsIntersectionController.Transition = MonitoredTransition(next_state=self.flashing_main, condition=StateEntryDurationCondition(duration=1, monitored_state=self.flashing_secondary))
		self.flashing_secondary.add_transition(from_flashing_secondary_to_flashing_main)

		layout = FiniteStateMachine.Layout()
		layout.add_state(self.initialization)
		layout.add_state(self.main_red)
		layout.add_state(self.main_green)
		layout.add_state(self.main_yellow)
		layout.add_state(self.secondary_red)
		layout.add_state(self.secondary_green)
		layout.add_state(self.secondary_yellow)
		layout.add_state(self.flashing_main)
		layout.add_state(self.flashing_secondary)
		layout.initial_state = self.initialization
		super(layout=layout)

controller = MainSecRoadsIntersectionController()
controller.start()
		