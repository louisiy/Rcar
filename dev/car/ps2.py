'''
    PS2类
'''

import setting as s
from machine import Pin
import time

class PS2:
    def __init__(self, dat_pin, cmd_pin, sel_pin, clk_pin):
        self.DAT = Pin(dat_pin, Pin.IN, Pin.PULL_UP)
        self.CMD = Pin(cmd_pin, Pin.OUT)
        self.SEL = Pin(sel_pin, Pin.OUT)
        self.CLK = Pin(clk_pin, Pin.OUT)

        self.data = [0] * 21
        self.last_buttons = 0
        self.buttons = 0
        self.last_read_time = 0
        self.read_delay = 1
        self.is_rumble_enabled = False
        self.is_pressure_enabled = False

    def byte_transfer(self, byte):
        temp = 0
        for i in range(8):
            self.CMD.value(byte & (1 << i))
            self.CLK.value(0)
            time.sleep_us(s.SHORT_DELAY_US)

            if self.DAT.value():
                temp |= (1 << i)

            self.CLK.value(1)
            time.sleep_us(s.SHORT_DELAY_US)
        self.CMD.value(1)
        time.sleep_us(s.SHORT_DELAY_US)
        return temp

    def send(self, command):
        self.SEL.value(0)
        time.sleep_us(s.SHORT_DELAY_US)
        for byte in command:
            self.byte_transfer(byte)
        self.SEL.value(1)
        time.sleep_ms(self.read_delay)

    def read(self, motor1=False, motor2=0):
        elapsed = time.ticks_ms() - self.last_read_time
        if elapsed > 1500:
            self.reset()
        if elapsed < self.read_delay:
            time.sleep_ms(self.read_delay - elapsed)

        data_to_send = [0x01, 0x42, 0, motor1, int((motor2 / 255) * 0xFF), 0, 0, 0, 0]
        extra_data = [0] * 12

        for _ in range(5):
            self.CMD.value(1)
            self.CLK.value(1)
            self.SEL.value(0)
            time.sleep_us(s.SHORT_DELAY_US)

            for i in range(9):
                self.data[i] = self.byte_transfer(data_to_send[i])

            if self.data[1] == 0x79:
                for i in range(12):
                    self.data[i + 9] = self.byte_transfer(extra_data[i])

            self.SEL.value(1)

            if (self.data[1] & 0xF0) == 0x70:
                break

            self.reset()
            time.sleep_ms(self.read_delay)

        if (self.data[1] & 0xF0) != 0x70:
            self.read_delay = min(self.read_delay + 1, 10)

        self.last_buttons = self.buttons
        self.buttons = (self.data[4] << 8) + self.data[3]
        self.last_read_time = time.ticks_ms()
        return (self.data[1] & 0xF0) == 0x70

    def config(self, pressure=False, rumble=False):

        self.CMD.value(1)
        self.CLK.value(1)

        for _ in range(10):
            self.send(s.CMD_ENTER_CONFIG)
            self.send(s.CMD_SET_MODE)
            if rumble:
                self.send(s.CMD_ENABLE_RUMBLE)
                self.is_rumble_enabled = True
            if pressure:
                self.send(s.CMD_ENABLE_PRESSURE)
                self.is_pressure_enabled = True

            self.send(s.CMD_EXIT_CONFIG)
            self.read()

            if pressure and self.data[1] == 0x79:
                break
            if self.data[1] == 0x73:
                break

        if self.data[1] not in [0x41, 0x42, 0x73, 0x79]:
            return 1

        self.read_delay = 1
        return 0

    def reset(self):
        self.send(s.CMD_ENTER_CONFIG)
        self.send(s.CMD_SET_MODE)
        if self.is_rumble_enabled:
            self.send(s.CMD_ENABLE_RUMBLE)
        if self.is_pressure_enabled:
            self.send(s.CMD_ENABLE_PRESSURE)
        self.send(s.CMD_EXIT_CONFIG)

    def is_pressed(self, button_name):
        mask = s.BUTTONS[button_name]
        return self.last_buttons & mask and not self.buttons & mask

    def is_released(self, button_name):
        mask=s.BUTTONS[button_name]
        return not self.last_buttons & mask and self.buttons & mask

    def is_held(self, button_name):
        mask=s.BUTTONS[button_name]
        return not self.last_buttons & mask and not self.buttons & mask

    def get_joysticks(self, axis):
        joystick_map = {'rx': 5,'ry': 6,'lx': 7,'ly': 8}
        if axis == 'all':
            return {key: self.data[joystick_map[key]] for key in joystick_map}
        elif axis in joystick_map:
            return self.data[joystick_map[axis]]