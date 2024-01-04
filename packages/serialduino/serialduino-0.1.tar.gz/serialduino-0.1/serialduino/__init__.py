import sched
import serial
import time
from typing import Callable

protocols = {
    "MP_SHIFT_OUT": 0,
    "MP_WRITE": 1,

    "DIGITAL_READ": 2,
    "DIGITAL_WRITE": 3,

    "PIN_MODE": 4,
    "GET_PIN_MODE": 5,

    "PING": 6,

    "MP_READ_GLOBAL": 7,
    "MP_READ_PIN": 8,

    "SEND_PULSE_READ_ECHO": 9,
    "SEND_IMPULSION": 10,

    "SETUP_MP": 11
}

class Arduino:
    board: serial.Serial
    logs: [] = []
    scheduler: sched.scheduler

    us_sensor_trigger = -1
    us_sensor_echo = -1

    mp_latch = -1
    mp_clock = -1
    mp_data = -1


    def __init__(self, port: str, baudrate: int, timeout: float):
        self.board = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.ping()
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def tick(self, func, args: tuple, millis: int):
        """
        Creates clock to update arduino status / get arduino status
        :param func: should take an Arduino argument first, should return args as tuple after
        :param args: additional args (without arduino)
        :param millis: time interval in milliseconds (note: should be kinda high ~ 100 +)
        :return:
        """
        def wrapper(f: Callable[..., tuple], ags: tuple):
            ags = f(*((self,) + ags))
            self.scheduler.enter(millis / 1000, 1, action=wrapper, kwargs={"f": f, "ags": ags})

        self.scheduler.enter(millis / 1000, 1, action=wrapper, kwargs={"f": func, "ags": args})
        self.scheduler.run()

    def is_microprocessor_setup(self) -> bool:
        """
        Checks if microprocessor is set up
        :return:
        """
        return self.mp_clock != -1 and self.mp_data != -1 and self.mp_latch != -1

    def is_us_sensor_setup(self) -> bool:
        """
        Checks if ultrasound sensor is set up
        :return:
        """
        return self.us_sensor_echo != -1 and self.us_sensor_trigger != -1

    def readline(self) -> str:
        """
        Reads the arduino serial
        Flushes the line returned from serial buffer
        :return: new line if available and if not log line or empty string
        """
        line = self.board.readline().decode("ascii").replace("\n", "")
        if line != "":
            self.logs.append(line.replace("log:", ""))

        if line.startswith("log:"):
            return ""

        return line

    def send_message(self, protocol: int, data):
        """
        Sends a message through arduino serial, message ends with $ sign to mark end
        :param protocol: See protocols object
        :param data: data to pass, see builtin functions to implement, no $ sign allowed
        :return:
        """
        self.board.write(bytes(f'{protocol}:{data}$', "ascii"))

    def set_microprocessor_pin(self, pin: int, value: 0 | 1):
        """
        Sets a particular pin's value in microprocessor
        Use set_microprocessor_binary if setting multiple pins at one to reduce lag/stress
        :param pin: from 0 to 7
        :param value: 0 or 1 (LOW or HIGH)
        :return:
        """

        if not self.is_microprocessor_setup():
            return

        self.send_message(protocols["MP_WRITE"], f'{pin}:{value}')
        self.wait_for_newline()

    def set_microprocessor_binary(self, value: int):
        """
        Sets the microprocessor's binary
        See 74hc595 doc for more info
        :param value: From 0 to 255 (8 bits)
        :return:
        """

        if not self.is_microprocessor_setup():
            return

        self.send_message(protocols["MP_SHIFT_OUT"], value)
        self.wait_for_newline()

    def digital_read(self, pin) -> int:
        """
        Asks for a digital pin's data and waits for response
        :param pin: starts at 1, no "d" before
        :return: 0 or 1 (LOW or HIGH)
        """
        self.send_message(protocols["DIGITAL_READ"], pin)
        return int(self.wait_for_newline().split(":")[2])

    def digital_write(self, pin: int, val: int):
        """
        Sets a digital pin's value
        :param pin: starts at 1, no "d" before
        :param val: 0 or 1 (LOW or HIGH)
        :return:
        """
        self.send_message(protocols["DIGITAL_WRITE"], f'{pin}:{val}')
        print(self.wait_for_newline())

    def ping(self):
        """
        Send ping to arduino
        Used when setting up the arduino serial
        Should send "Pong" in logs
        :return:
        """
        self.send_message(protocols["PING"], "")
        self.wait_for_newline()
        print("Arduino connected")

    def get_microprocessor_state(self) -> int:
        """
        Gets the microprocessor's binary
        :return: from 0 to 255 (8 bits)
        """

        if not self.is_microprocessor_setup():
            return - 1

        self.send_message(protocols["MP_READ_GLOBAL"], "")
        return int(self.wait_for_newline().split(":")[1])

    def get_microprocessor_pin(self, pin: int):
        """
        Gets a specific pin's value from the microprocessor
        :param pin: from 0 to 7
        :return:
        """

        if not self.is_microprocessor_setup():
            return -1

        self.send_message(protocols["MP_READ_PIN"], pin)
        return int(self.wait_for_newline().split(":")[2])

    def set_pin_mode(self, pin: int, output: bool):
        """
        Set's a digital pin's mode
        :param pin: start at 1, no "d" before
        :param output: true: is output ; false: is input
        :return:
        """
        self.send_message(protocols["PIN_MODE"], f'{pin}:{int(output)}')
        self.wait_for_newline()

    def get_pin_mode(self, pin: int):
        """
        Gets a digital pin's mode
        :param pin: start at 1, no "d" before
        :return: 0 if input, 1 if output
        """
        self.send_message(protocols["GET_PIN_MODE"], f'{pin}')
        return int(self.wait_for_newline().split(":")[2])

    def read_log_line(self) -> str:
        """
        Reads the arduino logger
        :return: first log line in buffer
        :return:
        """
        line = self.logs[0]
        return line

    def wait_for_newline(self) -> str:
        """
        Wait until new serial input
        :return: new serial input
        """
        line = self.readline()
        loop_count = 0
        while line == "":
            loop_count += 1
            line = self.readline()

            if loop_count > 50:
                return "waited_too_long"
            continue

        return line

    def send_impulsion(self, pin: int, millis: int):
        """
        Sends impulsion on pin
        :param pin: start at 1, no "d" before
        :param millis: impulsion time
        :return:
        """
        if not self.is_us_sensor_setup():
            return

        self.send_message(protocols["SEND_IMPULSION"], f'{pin}:{millis}')
        self.wait_for_newline()

    def setup_ultrasound_sensor(self, trigger: int, echo: int):
        """
        Setups the ultrasound sensor
        :param trigger: trigger pin, start at 1, no "d" before
        :param echo: echo pin, start at 1, no "d" before
        :return:
        """
        if echo == -1 or trigger == -1:
            return

        self.us_sensor_trigger = trigger
        self.us_sensor_echo = echo
        self.set_pin_mode(trigger, True)
        self.set_pin_mode(echo, False)

    def setup_microprocessor(self, data: int, latch: int, clock: int):
        """
        Setups the microprocessor (usually, data=4,latch=5,clock=6)
        :param data: data pin, start at 1, no "d" before
        :param latch: latch pin, start at 1, no "d" before
        :param clock: clock pin, start at 1, no "d" before
        :return:
        """

        if data == -1 or latch == -1 or clock == -1:
            return

        self.mp_clock = clock
        self.mp_latch = latch
        self.mp_data = data

        self.send_message(protocols["SETUP_MP"], f'{data}:{latch}:{clock}')
        self.wait_for_newline()

    def get_us_sensor_distance(self) -> float:
        """
        Measures ultrasound sensor's measured distance in millimeters
        :return: -1 if out of range
        """

        if not self.is_us_sensor_setup():
            return -1

        self.send_message(protocols["SEND_PULSE_READ_ECHO"], f'{self.us_sensor_trigger}:{self.us_sensor_echo}:10')
        res = float(self.wait_for_newline().split(":")[2]) / 580
        if res > 0:
            return res

        return -1

    def wait_millis(self, millis: int):
        """
        Wait x milliseconds
        :param millis: time to wait
        :return:
        """

        time.sleep(millis / 1000)
