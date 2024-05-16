from FiniteStateMachine import FiniteStateMachine
from State import ActionState, MonitoredState, TaskState
from Condition import ManualControlCondition, StateValueCondition, StateEntryDurationCondition, AlwaysTrueCondition
from WonderingFSM import WonderingFSM
from Transition import ConditionalTransition
from Robot import Robot
from ManualControl import ManualControlFSM
from time import perf_counter

class C64(FiniteStateMachine):
    def __init__(self):
        self.robot = Robot()

        robot_instantiation = MonitoredState()
        robot_instantiation.custom_value = self.robot.is_instanciated

        instantiation_failed = MonitoredState()
        instantiation_failed.add_entering_action(lambda : print("Robot instantiation failed"))

        robot_integrity = MonitoredState()
        robot_integrity.custom_value = self.robot.has_integrity

        integrity_failed = MonitoredState()

        def integrity_failed_entering_action():
            print("Robot integrity failed")
            self.robot.set_eyes_color("red")
            self.robot.eye_blinker.blink(self.robot.eye_blinker.Side.BOTH, cycle_duration=0.5, percent_on=0.5, begin_on=True)

        def integrity_failed_exiting_action():
            self.robot.turn_off_eyes()

        integrity_failed.add_entering_action(integrity_failed_entering_action)
        integrity_failed.add_exiting_action(integrity_failed_exiting_action)

        integrity_succeeded = MonitoredState()

        def integrity_succeeded_entering_action():
            print("Robot integrity succeeded")
            self.robot.set_eyes_color("green")
            self.robot.eye_blinker.blink(self.robot.eye_blinker.Side.BOTH, cycle_duration=1., percent_on=0.5, begin_on=True)
    
        

        def integrity_succeeded_exiting_action():
            print('stop')
            self.robot.turn_off_eyes()

        integrity_succeeded.add_entering_action(integrity_succeeded_entering_action)
        integrity_succeeded.add_in_state_action(lambda: self.robot.eye_blinker.track())
        integrity_succeeded.add_exiting_action(integrity_succeeded_exiting_action)


        shut_down_robot = MonitoredState()

        def shut_down_robot_entering_action():
            print("Shutting down robot")
            self.robot.set_eyes_color("yellow")
            self.robot.eye_blinker.blink(self.robot.eye_blinker.Side.RIGHT_RECIPROCAL, cycle_duration=0.75, percent_on=0.5, begin_on=True)

        end = ActionState(ActionState.Parameters(terminal=True))

        home = MonitoredState()
        home.add_entering_action(lambda : print("Robot is home"))
#         def home_listen_input():
#             home.custom_value = self.robot.read_input(read_once=True)
#             print(f'\rkey = {home.custom_value}', end='                                   ')
#         home.add_in_state_action(home_listen_input)
#         def home_reset_input():
#             home.custom_value = self.robot.KeyCodes.NONE
#             print(f'\rkey exit home = {home.custom_value}', end='                                   ')
#         home.add_exiting_action(home_reset_input)

        task1 = TaskState()  
        task1.task_value = ManualControlFSM(robot=self.robot)
        
        def task1_eyes_entering_action():
            self.robot.set_left_eye_color("red")
            self.robot.set_right_eye_color("blue")
            self.robot.eye_blinker.blink(self.robot.eye_blinker.Side.RIGHT_RECIPROCAL, cycle_duration=0.5, percent_on=0.5, begin_on=True)

        def task1_eyes_in_state_action():
            task1.custom_value = self.robot.read_input()
            task1.task_value.track()

        def task1_eyes_exiting_action():
            self.robot.turn_off_eyes()

        task1.add_entering_action(lambda: print("Task 1"))
        task1.add_entering_action(task1_eyes_entering_action)
        task1.add_in_state_action(task1_eyes_in_state_action)
        task1.add_exiting_action(task1_eyes_exiting_action)

        task2 = MonitoredState()
        task2.custom_value = WonderingFSM(robot=self.robot)
        
        task2.add_entering_action(lambda: print("Task 2"))

        # --------- ROBOT INSTANTIATION ---------
        robot_instantiation_succeeded = StateValueCondition(expected_value=True, monitored_state=robot_instantiation)
        robot_instantiation_failed = StateValueCondition(expected_value=False, monitored_state=robot_instantiation)

        robot_instantiation_to_robot_integrity = ConditionalTransition(next_state=robot_integrity, condition=robot_instantiation_succeeded)
        robot_instantiation_to_instanciation_failed = ConditionalTransition(next_state=instantiation_failed, condition=robot_instantiation_failed)

        robot_instantiation.add_transition(robot_instantiation_to_robot_integrity)
        robot_instantiation.add_transition(robot_instantiation_to_instanciation_failed)
        
        # --------- INSTANTIATION FAILED ---------
        instantiation_failed_condition = AlwaysTrueCondition()
        instantiation_failed_to_end = ConditionalTransition(next_state=end, condition=instantiation_failed_condition)
        instantiation_failed.add_transition(instantiation_failed_to_end)

        # --------- ROBOT INTEGRITY ---------
        robot_integrity_succeeded = StateValueCondition(expected_value=True, monitored_state=robot_integrity)
        robot_integrity_failed = StateValueCondition(expected_value=False, monitored_state=robot_integrity)

        robot_integrity_to_integrity_failed = ConditionalTransition(next_state=integrity_failed, condition=robot_integrity_failed)
        robot_integrity_to_integrity_succeeded = ConditionalTransition(next_state=integrity_succeeded, condition=robot_integrity_succeeded)

        robot_integrity.add_transition(robot_integrity_to_integrity_failed)
        robot_integrity.add_transition(robot_integrity_to_integrity_succeeded)

        # --------- INTEGRITY FAILED ---------
        integrity_failed_duration = StateEntryDurationCondition(duration=5, monitored_state=integrity_failed)
        integrity_failed_to_shut_down_robot = ConditionalTransition(next_state=shut_down_robot, condition=integrity_failed_duration)
        integrity_failed.add_transition(integrity_failed_to_shut_down_robot)

        # --------- INTEGRITY SUCCEEDED ---------
        integrity_succeeded_duration = StateEntryDurationCondition(duration=3, monitored_state=integrity_succeeded)
        integrity_succeeded_to_home = ConditionalTransition(next_state=home, condition=integrity_succeeded_duration)
        integrity_succeeded.add_transition(integrity_succeeded_to_home)

        # --------- SHUT DOWN ROBOT ---------
        shut_down_robot_duration = StateEntryDurationCondition(duration=3, monitored_state=shut_down_robot)
        shut_down_robot_to_end = ConditionalTransition(next_state=end, condition=shut_down_robot_duration)
        shut_down_robot.add_transition(shut_down_robot_to_end)

        # --------- HOME ---------
        home_to_task1 = ConditionalTransition(next_state=task1, condition=ManualControlCondition(robot= self.robot, expected_value=self.robot.KeyCodes.ONE, read_once=True))
        home_to_task2 = ConditionalTransition(next_state=task2, condition=ManualControlCondition(robot= self.robot, expected_value=self.robot.KeyCodes.TWO, read_once=True))
        home_to_shut_down_robot = ConditionalTransition(next_state=shut_down_robot, condition=ManualControlCondition(robot= self.robot, expected_value=self.robot.KeyCodes.OK, read_once=True))
        home.add_transition(home_to_task1)
        home.add_transition(home_to_task2)
        home.add_transition(home_to_shut_down_robot)
        
        # --------- TASK 1 ------------
        task1_to_home = ConditionalTransition(next_state=home, condition=ManualControlCondition(robot= self.robot,expected_value=self.robot.KeyCodes.OK, read_once=True))
        task1.add_transition(task1_to_home)

        # --------- TASK 2 ------------
        task2_duration = StateEntryDurationCondition(duration=3600, monitored_state=task2)
        task2_to_home = ConditionalTransition(next_state=task2, condition=task2_duration)
        task2.add_transition(task2_to_home)


        self.layout = FiniteStateMachine.Layout()
        self.layout.add_states([robot_instantiation, instantiation_failed, robot_integrity, integrity_failed, integrity_succeeded, shut_down_robot, end, home, task1, task2])
        self.layout.initial_state = robot_instantiation
        super().__init__(layout=self.layout)
