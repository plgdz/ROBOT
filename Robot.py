<<<<<<< Updated upstream
import easygopigo3 as gpg
=======
from enum import Enum, auto
import easygopigo3 as gpg

>>>>>>> Stashed changes

class Robot():

    COLORS = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'white': (255, 255, 255),
        'off': (0, 0, 0)
    }
    
    class KeyCodes(Enum):
        NONE = 0
        UP = 1
        LEFT = 2
        OK = 3
        RIGHT = 4 
        DOWN = 5
        ONE = 6
        TWO = 7
        THREE = 8
        FOUR = 9
        FIVE = 10
        SIX = 11
        SEVEN = 12
        EIGHT = 13
        NINE = 14
        STAR = 15
        ZERO = 16
        HASH = 17
    
    class MoveDirection(Enum):
        FORWARD = auto()
        BACKWARD = auto()
        LEFT = auto()
        RIGHT = auto()
        STOP = auto()

    def __init__(self) -> None:
        from LedBlinker import LedBlinker
        from EyeBlinker import EyeBlinker

        try:
            self.__gpg = gpg.EasyGoPiGo3()
        except:
            self.__gpg = None

        self.init_remote()
        self.init_servo_motor()
        self.init_distance_sensor()

        self.right_eye_color = None
        self.left_eye_color = None

        self.led_blinker = LedBlinker(self)
        self.eye_blinker = EyeBlinker(self)
        self.__robot = gpg.EasyGoPiGo3()
        remote_control_port = 'AD1'
        self.__remote_control = self.__robot.init_remote(port=remote_control_port)

    # -------------------------------------------------------------------------
    def init_remote(self):
        remote_control_port = 'AD1'
        try:
            self.remote = self.__gpg.init_remote(port=remote_control_port)
        except:
            self.remote = None
       
    def init_servo_motor(self):
        servo_cam_port = 'SERVO1'
        servo_range_port = 'SERVO2'

        try:
            self.camera_servo_control = self.__gpg.init_servo(port=servo_cam_port)
        except:
            self.camera_servo_control = None

        try:
            self.range_sensor_servo_control = self.__gpg.init_servo(port=servo_range_port)
        except:
            self.range_sensor_servo_control = None

    def init_distance_sensor(self):
        distance_sensor_port = 'I2C'
        try:
            self.distance_sensor = self.__gpg.init_distance_sensor(port=distance_sensor_port)
        except:
            self.distance_sensor = None

    # -------------------------------------------------------------------------
    @property
    def is_instanciated(self) -> bool:
        return self.__gpg is not None
    
    @property
    def has_integrity(self) -> bool:
        return self.remote is not None and self.camera_servo_control is not None and self.range_sensor_servo_control is not None and self.distance_sensor is not None


    def turn_on_left_led(self) -> None:
<<<<<<< Updated upstream
        self.__gpg.led_on('left')
        #print("turn_on_left_led")

    def turn_off_left_led(self) -> None:
        self.__gpg.led_off('left')
        #print("turn_off_left_led")

    def turn_on_right_led(self) -> None:
        self.__gpg.led_on('right')
        #print("turn_on_right_led")

    def turn_off_right_led(self) -> None:
        self.__gpg.led_off('right')
        #print("turn_off_right_led")
=======
        self.__robot.led_on('left')
        print("turn_on_left_led")

    def turn_off_left_led(self) -> None:
        self.__robot.led_off('left')
        print("turn_off_left_led")

    def turn_on_right_led(self) -> None:
        self.__robot.led_on('right')
        print("turn_on_right_led")

    def turn_off_right_led(self) -> None:
        self.__robot.led_off('right')
        print("turn_off_right_led")
>>>>>>> Stashed changes

    #--------------------------------------------------------------------------------------------

    def set_left_eye_color(self, color : str) -> None:
        self.__gpg.set_left_eye_color(self.COLORS[color])
        #print(f"set_left_eye_color : {self.COLORS[color]}")
        self.left_eye_color = color

    def turn_on_left_eye(self) -> None:
        self.__gpg.open_left_eye()
        #print(f'turn_on_left_eye : {self.left_eye_color}')

    def turn_off_left_eye(self) -> None:
        self.__gpg.close_left_eye()
        #print("turn_off_left_eye")

    def set_right_eye_color(self, color : str) -> None:
        self.__gpg.set_right_eye_color(self.COLORS[color])
        #print(f"set_right_eye_color : {self.COLORS[color]}")
        self.right_eye_color = color

    def turn_on_right_eye(self) -> None:
        self.__gpg.open_right_eye()
        #print(f"turn_on_right_eye : {self.right_eye_color}")

    def turn_off_right_eye(self) -> None:
        self.__gpg.close_right_eye()
        #print("turn_off_right_eye")

    def set_eyes_color(self, color : str) -> None:
        self.__gpg.set_eye_color(self.COLORS[color])
        #print(f'set_eyes_color : {self.COLORS[color]}')
        self.left_eye_color = color
        self.right_eye_color = color

    def turn_on_eyes(self) -> None:
        self.__gpg.open_eyes()
        #print(f"turn_on_eyes : {self.right_eye_color} {self.left_eye_color}")

    def turn_off_eyes(self) -> None:
<<<<<<< Updated upstream
        self.__gpg.close_eyes()
        #print("turn_off_eyes")
=======
        # self.__gpg.close_eyes()
        print("turn_off_eyes")
        
    def move(self, config):
        if config == Robot.MoveDirection.FORWARD:
            self.__robot.forward()
        elif config == Robot.MoveDirection.RIGHT:
            self.__robot.right()
        elif config == Robot.MoveDirection.LEFT:
            self.__robot.left()
        elif config == Robot.MoveDirection.BACKWARD:
            self.__robot.backward()
        elif config == Robot.MoveDirection.STOP:
            self.__robot.stop()
        
    def read_input(self):
        return Robot.KeyCodes(self.__remote_control.read())
>>>>>>> Stashed changes

    def forward(self) -> None:
        self.__gpg.forward()

    def backward(self) -> None:
        self.__gpg.backward()

    def stop(self) -> None:
        self.__gpg.stop()

    def turn_right(self) -> None:
        self.__gpg.right()

    def turn_left(self) -> None:
        self.__gpg.left()