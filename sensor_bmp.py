from machine import Pin, I2C
from bmp280 import *
import time
import machine


class SensorBmp:
    def __init__(self):
        i2c = I2C(0, scl=Pin(9), sda=Pin(8))
        self.bmp280_object = BMP280(i2c,
                                    addr=0x76,
                                    use_case=BMP280_CASE_WEATHER)

        self.bmp280_object.power_mode = BMP280_POWER_NORMAL
        self.bmp280_object.oversample = BMP280_OS_HIGH
        self.bmp280_object.temp_os = BMP280_TEMP_OS_8
        self.bmp280_object.press_os = BMP280_TEMP_OS_4
        self.bmp280_object.standby = BMP280_STANDBY_250
        self.bmp280_object.iir = BMP280_IIR_FILTER_2

    def read_temperature(self):
        return self.bmp280_object.temperature

    def read_pressure(self):
        return (self.bmp280_object.pressure * 0.01) - 3  # -3 is ERROR
