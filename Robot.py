# import easygopigo3 as gpg


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

    def __init__(self) -> None:
        from LedBlinker import LedBlinker
        from EyeBlinker import EyeBlinker

        # self.__gpg = gpg.EasyGoPiGo3()

        self.right_eye_color = None
        self.left_eye_color = None

        self.led_blinker = LedBlinker(self)
        self.eye_blinker = EyeBlinker(self)

    def is_instanciated(self) -> bool:
        if isinstance(self.__gpg, gpg.EasyGoPiGo3):
            return True
        return False
    
    def has_integrity(self) -> bool:
        pass

    #--------------------------------------------------------------------------------------------

    def turn_on_left_led(self) -> None:
    #    self.__gpg.led_on('left')
        print("turn_on_left_led")

    def turn_off_left_led(self) -> None:
        # self.__gpg.led_off('left')
        print("turn_off_left_led")

    def turn_on_right_led(self) -> None:
        # self.__gpg.led_on('right')
        print("turn_on_right_led")

    def turn_off_right_led(self) -> None:
        # self.__gpg.led_off('right')
        print("turn_off_right_led")

    #--------------------------------------------------------------------------------------------

    def set_left_eye_color(self, color : str) -> None:
        # self.__gpg.set_left_eye_color(self.COLORS[color])
        print(f"set_left_eye_color : {self.COLORS[color]}")
        self.left_eye_color = color

    def turn_on_left_eye(self) -> None:
        # self.__gpg.open_left_eye()
        print(f"turn_on_left_eye : {self.left_eye_color}")

    def turn_off_left_eye(self) -> None:
        # self.__gpg.close_left_eye()
        print("turn_off_left_eye")

    def set_right_eye_color(self, color : str) -> None:
        # self.__gpg.set_right_eye_color(self.COLORS[color])
        print(f"set_right_eye_color : {self.COLORS[color]}")
        self.right_eye_color = color

    def turn_on_right_eye(self) -> None:
        # self.__gpg.open_right_eye()
        print(f"turn_on_right_eye : {self.right_eye_color}")

    def turn_off_right_eye(self) -> None:
        # self.__gpg.close_right_eye()
        print("turn_off_right_eye")

    def set_eyes_color(self, color : str) -> None:
        # self.__gpg.set_eye_color(self.COLORS[color]
        print(f"set_eyes_color : {self.COLORS[color]}")
        self.left_eye_color = color
        self.right_eye_color = color

    def turn_on_eyes(self) -> None:
        # self.__gpg.open_eyes()
        print(f"turn_on_eyes : {self.right_eye_color} {self.left_eye_color}")

    def turn_off_eyes(self) -> None:
        # self.__gpg.close_eyes()
        print("turn_off_eyes")

    

if __name__ == "__main__":
    robot = Robot()
    # robot.led_blinker.blink(robot.led_blinker.Side.LEFT, cycle_duration=1., percent_on=0.5, begin_on=True)
    robot.set_left_eye_color('red')
    robot.set_right_eye_color('blue')
    robot.eye_blinker.blink(robot.eye_blinker.Side.LEFT_RECIPROCAL, cycle_duration=1., percent_on=0.5, begin_on=True)

    while True:
        robot.eye_blinker.track()
        
    