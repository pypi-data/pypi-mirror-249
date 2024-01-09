import numpy as np
import serial
import serial.tools.list_ports
import time

from typing import Optional

from .exception import AeroShieldException


class AeroShield:
    HANDSHAKE = 0
    RUN = 1
    STOP = 2

    # Wait time after opening connection
    _TIMEOUT = 3

    def __init__(self, baudrate:Optional[int]=115200, port:Optional[str]=None) -> None:
        if port is None:
            port = self.find_arduino()

        self.conn = serial.Serial(port, baudrate=baudrate)
        self.conn.timeout = 1

        self.zero_angle = 0

    def find_arduino(self):
        """Get the name of the port that is connected to Arduino. Raises exception if not port was found"""
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if p.manufacturer is not None and "Arduino" in p.manufacturer:
                return p.device

        raise AeroShieldException("No Arduino Found")

    @staticmethod
    def raw_angle_to_deg(raw: int) -> float:
        """Convert raw angle to degrees.

        :param raw: 12-bit value of angle.
        :type raw: int
        :return: Angle value scaled to degrees.
        :rtype: float
        """
        return raw * 360 / 4096

    @staticmethod
    def raw_angle_to_rad(raw: int) -> float:
        return raw * np.pi / 2048

    def calibrated_angle_deg(self, raw_angle: float) -> float:
        """Calibrate the angle with the zero angle read at the start of the run.

        :param raw_angle: Raw 12-bit angle value.
        :type raw_angle: int
        :return: Calibrated angle in degrees.
        :rtype: float
        """

        angle = self.raw_angle_to_deg(raw_angle) - self.zero_angle
        if angle < -90:
            angle += 360

        return angle

    def raw_pot_to_percent(self, raw:int) -> float:
        return raw * 100 / 1024

    def read(self) -> tuple[float]:
        try:
            data = self.conn.read(3)

            pot = data[0] // 16 * 256 + data[1]
            angle = data[0] % 16 * 256 + data[2]

            return self.raw_pot_to_percent(pot), self.calibrated_angle_deg(angle)

        except IndexError:
            raise AeroShieldException("No data received from Arduino")

    def write(self, flag:int, motor:float):
        motor = int(min(max((motor), 0), 255))
        self.conn.write(bytes([flag, motor]))
        return motor

    def open(self):
        self.conn.reset_input_buffer()
        self.conn.reset_output_buffer()
        if not self.conn.is_open:
            self.conn.open()

        time.sleep(self._TIMEOUT)

        self.write(self.RUN, 0)
        _, self.zero_angle = self.read()

        return self

    def close(self, *args):
        self.write(self.STOP, 0)
        self.conn.close()

    def __enter__(self):
        return self.open()

    def __exit__(self, *args):
        self.close(*args)
