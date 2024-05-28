"""
MIT License

Copyright (c) 2024 esophagoose

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Module Source:
https://github.com/esophagoose/gt911-micropython/


This module has been modified slightly:
 - gt911_constants.py has been replaced with real constants in this file.
 - Modified I2C constructor to avoid depreciation warning.
 - Default frequency has been changed to 400000.
 - Formatting has been slightly changed.
 - Added rotation option.
"""

import time
from collections import namedtuple
import machine



# _CONSTANTS:
class Addr:
    ADDR1 = 0x5D
    ADDR2 = 0x14

_ROTATION_LEFT = const(0)
_ROTATION_INVERTED = const(1)
_ROTATION_RIGHT = const(2)
_ROTATION_NORMAL = const(3)

# Real-time command (Write only)
_COMMAND = const(0x8040)
_ESD_CHECK = const(0x8041)
_COMMAND_CHECK = const(0x8046)

# Configuration information (R/W)
_CONFIG_START = const(0x8047)
_CONFIG_VERSION = const(0x8047)
_X_OUTPUT_MAX_LOW = const(0x8048)
_X_OUTPUT_MAX_HIGH = const(0x8049)
_Y_OUTPUT_MAX_LOW = const(0x804A)
_Y_OUTPUT_MAX_HIGH = const(0x804B)
_TOUCH_NUMBER = const(0x804C)
_MODULE_SWITCH_1 = const(0x804D)
_MODULE_SWITCH_2 = const(0x804E)
_SHAKE_COUNT = const(0x804F)
_FILTER = const(0x8050)
_LARGE_TOUCH = const(0x8051)
_NOISE_REDUCTION = const(0x8052)
_SCREEN_TOUCH_LEVEL = const(0x8053)
_SCREEN_RELEASE_LEVEL = const(0x8054)
_LOW_POWER_CONTROL = const(0x8055)
_REFRESH_RATE = const(0x8056)
_X_THRESHOLD = const(0x8057)
_Y_THRESHOLD = const(0x8058)
_X_SPEED_LIMIT = const(0x8059)  # Reserve
_Y_SPEED_LIMIT = const(0x805A)  # Reserve
_SPACE_TOP_BOTTOM = const(0x805B)
_SPACE_LEFT_RIGHT = const(0x805C)
_MINI_FILTER = const(0x805D)
_STRETCH_R0 = const(0x805E)
_STRETCH_R1 = const(0x805F)
_STRETCH_R2 = const(0x8060)
_STRETCH_RM = const(0x8061)
_DRV_GROUPA_NUM = const(0x8062)
_DRV_GROUPB_NUM = const(0x8063)
_SENSOR_NUM = const(0x8064)
_FREQ_A_FACTOR = const(0x8065)
_FREQ_B_FACTOR = const(0x8066)
_PANEL_BIT_FREQ_L = const(0x8067)
_PANEL_BIT_FREQ_H = const(0x8068)
_PANEL_SENSOR_TIME_L = const(0x8069)  # Reserve
_PANEL_SENSOR_TIME_H = const(0x806A)
_PANEL_TX_GAIN = const(0x806B)
_PANEL_RX_GAIN = const(0x806C)
_PANEL_DUMP_SHIFT = const(0x806D)
_DRV_FRAME_CONTROL = const(0x806E)
_CHARGING_LEVEL_UP = const(0x806F)
_MODULE_SWITCH3 = const(0x8070)
_GESTURE_DIS = const(0x8071)
_GESTURE_LONG_PRESS_TIME = const(0x8072)
_X_Y_SLOPE_ADJUST = const(0x8073)
_GESTURE_CONTROL = const(0x8074)
_GESTURE_SWITCH1 = const(0x8075)
_GESTURE_SWITCH2 = const(0x8076)
_GESTURE_REFRESH_RATE = const(0x8077)
_GESTURE_TOUCH_LEVEL = const(0x8078)
_NEWGREENWAKEUPLEVEL = const(0x8079)
_FREQ_HOPPING_START = const(0x807A)
_FREQ_HOPPING_END = const(0x807B)
_NOISE_DETECT_TIMES = const(0x807C)
_HOPPING_FLAG = const(0x807D)
_HOPPING_THRESHOLD = const(0x807E)
_NOISE_THRESHOLD = const(0x807F)  # Reserve
_NOISE_MIN_THRESHOLD = const(0x8080)
_HOPPING_SENSOR_GROUP = const(0x8082)
_HOPPING_SEG1_NORMALIZE = const(0x8083)
_HOPPING_SEG1_FACTOR = const(0x8084)
_MAIN_CLOCK_AJDUST = const(0x8085)
_HOPPING_SEG2_NORMALIZE = const(0x8086)
_HOPPING_SEG2_FACTOR = const(0x8087)
_HOPPING_SEG3_NORMALIZE = const(0x8089)
_HOPPING_SEG3_FACTOR = const(0x808A)
_HOPPING_SEG4_NORMALIZE = const(0x808C)
_HOPPING_SEG4_FACTOR = const(0x808D)
_HOPPING_SEG5_NORMALIZE = const(0x808F)
_HOPPING_SEG5_FACTOR = const(0x8090)
_HOPPING_SEG6_NORMALIZE = const(0x8092)
_KEY_1 = const(0x8093)
_KEY_2 = const(0x8094)
_KEY_3 = const(0x8095)
_KEY_4 = const(0x8096)
_KEY_AREA = const(0x8097)
_KEY_TOUCH_LEVEL = const(0x8098)
_KEY_LEAVE_LEVEL = const(0x8099)
_KEY_SENS_1_2 = const(0x809A)
_KEY_SENS_3_4 = const(0x809B)
_KEY_RESTRAIN = const(0x809C)
_KEY_RESTRAIN_TIME = const(0x809D)
_GESTURE_LARGE_TOUCH = const(0x809E)
_HOTKNOT_NOISE_MAP = const(0x80A1)
_LINK_THRESHOLD = const(0x80A2)
_PXY_THRESHOLD = const(0x80A3)
_GHOT_DUMP_SHIFT = const(0x80A4)
_GHOT_RX_GAIN = const(0x80A5)
_FREQ_GAIN0 = const(0x80A6)
_FREQ_GAIN1 = const(0x80A7)
_FREQ_GAIN2 = const(0x80A8)
_FREQ_GAIN3 = const(0x80A9)
_COMBINE_DIS = const(0x80B3)
_SPLIT_SET = const(0x80B4)
_SENSOR_CH0 = const(0x80B7)
_DRIVER_CH0 = const(0x80D5)
_CONFIG_CHKSUM = const(0x80FF)
_CONFIG_FRESH = const(0x8100)
_CONFIG_SIZE = const(0xFF - 0x46)

# Coordinate information
_PRODUCT_ID = const(0x8140)
_FIRMWARE_VERSION = const(0x8140)
_RESOLUTION = const(0x8140)
_VENDOR_ID = const(0x8140)
_IMFORMATION = const(0x8140)
_POINT_INFO = const(0x814E)
_POINT_1 = const(0x814F)
_POINT_2 = const(0x8157)
_POINT_3 = const(0x815F)
_POINT_4 = const(0x8167)
_POINT_5 = const(0x816F)

_POINTS_REG = [
    _POINT_1,
    _POINT_2,
    _POINT_3,
    _POINT_4,
    _POINT_5,
]



def calculate_checksum(configuration: list[int]):
    checksum = sum(configuration[: _CONFIG_SIZE])
    checksum = checksum & 0xFF
    return ((~checksum) + 1) & 0xFF


def config_offset(reg: int):
    return reg - _CONFIG_START


class GT911:
    def __init__(self, sda, scl, interrupt, reset, freq=400_000, rotation=1):
        self.width = 0
        self.height = 0
        self.address = None
        self.configuration = []
        self.i2c =  machine.SoftI2C(freq=freq, scl=machine.Pin(scl), sda=machine.Pin(sda))
        self.interrupt = machine.Pin(interrupt, machine.Pin.OUT)
        self.reset_pin = machine.Pin(reset, machine.Pin.OUT)
        
        self.rotation = rotation % 4


    @micropython.viper
    def _rotate_xy(self, x:int, y:int):
        """Rotate x/y coordinates such that they align with display coordinates."""
        rotation = int(self.rotation)
        width = int(self.width)
        height = int(self.height)
        
        # if landscape mode:
        if rotation % 2 == 1:
            x, y = y, x
            width, height = height, width
        # invert y
        if rotation == 1 or rotation == 2:
            y = height - y
        # invert x
        if rotation == 2 or rotation == 3:
            x = width - x
            
        return x, y


    def enable_interrupt(self, callback):
        self.interrupt.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)


    def begin(self, address):
        self.address = address
        self.reset()
        self.configuration = self.read(_CONFIG_START, _CONFIG_SIZE)
        wl = self.configuration[config_offset(_X_OUTPUT_MAX_LOW)]
        wh = self.configuration[config_offset(_X_OUTPUT_MAX_HIGH)]
        hl = self.configuration[config_offset(_Y_OUTPUT_MAX_LOW)]
        hh = self.configuration[config_offset(_Y_OUTPUT_MAX_HIGH)]
        self.width = (wh << 8) + wl
        self.height = (hh << 8) + hl


    def reset(self):
        self.interrupt.value(0)
        self.reset_pin.value(0)
        time.sleep_ms(10)
        self.interrupt.value(self.address == Addr.ADDR2)
        time.sleep_ms(1)
        self.reset_pin.value(1)
        time.sleep_ms(5)
        self.interrupt.value(0)
        time.sleep_ms(50)
        self.interrupt.init(mode=machine.Pin.IN)
        time.sleep_ms(50)


    def reflash_config(self):
        assert len(self.configuration) == _CONFIG_SIZE
        checksum = calculate_checksum(self.configuration)
        self.write(_CONFIG_START, self.configuration)
        self.write(_CONFIG_CHKSUM, checksum)
        self.write(_CONFIG_FRESH, 1)


    def set_resolution(self, width, height):
        self.configuration[_X_OUTPUT_MAX_LOW - _CONFIG_START] = width & 0xFF
        self.configuration[_X_OUTPUT_MAX_HIGH - _CONFIG_START] = (width >> 8) & 0xFF
        self.configuration[_Y_OUTPUT_MAX_LOW - _CONFIG_START] = height & 0xFF
        self.configuration[_Y_OUTPUT_MAX_HIGH - _CONFIG_START] = (
            height >> 8
        ) & 0xFF
        self.reflash_config()


    def get_points(self):
        points = []
        info = self.read(_POINT_INFO, 1)[0]
        ready = bool((info >> 7) & 1)
        # large_touch = bool((info >> 6) & 1)
        touch_count = info & 0xF
        if ready and touch_count > 0:
            for i in range(touch_count):
                data = self.read(_POINT_1 + (i * 8), 7)
                points.append(self.parse_point(data))
        self.write(_POINT_INFO, [0])
        return points


    def parse_point(self, data):
        track_id = data[0]
        x = data[1] + (data[2] << 8)
        y = data[3] + (data[4] << 8)
        x, y = self._rotate_xy(x, y)
        size = data[5] + (data[6] << 8)
        return TouchPoint(track_id, x, y, size)


    def write(self, reg: int, value: list[int]):
        self.i2c.writeto_mem(self.address, reg, bytes(value), addrsize=16)


    def read(self, reg: int, length: int):
        data = self.i2c.readfrom_mem(self.address, reg, length, addrsize=16)
        return list(data)


TouchPoint = namedtuple("TouchPoint", ["id", "x", "y", "size"])
