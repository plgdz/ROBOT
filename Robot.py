from enum import Enum, auto
import easygopigo3 as gpg

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
        ROTATE = auto()

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
        self.max_distance = 100.0

        self.led_blinker = LedBlinker(self)
        self.eye_blinker = EyeBlinker(self)
        

    # -------------------------------------------------------------------------
    def init_remote(self):
        remote_control_port = 'AD1'
        try:
            self.__remote_control = self.__gpg.init_remote(port=remote_control_port)
        except:
            self.__remote_control = None

    def init_servo_motor(self):
        servo_cam_port = 'SERVO1'
        servo_range_port = 'SERVO2'

        try:
            self.__camera_servo_control = self.__gpg.init_servo(port=servo_cam_port)
        except:
            self.__camera_servo_control = None

        try:
            self.__range_sensor_servo_control = self.__gpg.init_servo(port=servo_range_port)
        except:
            self.__range_sensor_servo_control = None

    def init_distance_sensor(self):
        distance_sensor_port = 'I2C'
        try:
            self.__distance_sensor = self.__gpg.init_distance_sensor(port=distance_sensor_port)
        except:
            self.__distance_sensor = None

    # -------------------------------------------------------------------------
    @property
    def is_instanciated(self) -> bool:
        return self.__gpg is not None
    
    @property
    def has_integrity(self) -> bool:
        return self.__remote_control is not None and self.__camera_servo_control is not None and self.__range_sensor_servo_control is not None and self.__distance_sensor is not None


    def turn_on_left_led(self) -> None:
        self.__gpg.led_on('left')

    def turn_off_left_led(self) -> None:
        self.__gpg.led_off('left')

    def turn_on_right_led(self) -> None:
        self.__gpg.led_on('right')
        
    def turn_off_right_led(self) -> None:
        self.__gpg.led_off('right')
        
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

    def turn_off_right_eye(self) -> None:
        self.__gpg.close_right_eye()

    def set_eyes_color(self, color : str) -> None:
        self.__gpg.set_eye_color(self.COLORS[color])
        self.left_eye_color = color
        self.right_eye_color = color

    def turn_on_eyes(self) -> None:
        self.__gpg.open_eyes()
        
    def turn_off_eyes(self) -> None:
        self.__gpg.close_eyes()

    def move(self, config):
        if config == Robot.MoveDirection.FORWARD:
            self.__gpg.forward()
        elif config == Robot.MoveDirection.RIGHT:
            self.__gpg.right()
        elif config == Robot.MoveDirection.LEFT:
            self.__gpg.left()
        elif config == Robot.MoveDirection.BACKWARD:
            self.__gpg.backward()
        elif config == Robot.MoveDirection.STOP:
            self.__gpg.stop()
        elif config == Robot.MoveDirection.ROTATE:
            self.__gpg.turn_degrees(1980)
        
    def read_input(self):
        return Robot.KeyCodes(self.__remote_control.read())
    
    def read_distance_sensor(self):
        # returns the distance in mm (float)
        return self.__distance_sensor.read_mm()
    
    def reached_max_distance(self):
        # returns the distance in mm (float)
        return self.__distance_sensor.read_mm() <= self.max_distance
