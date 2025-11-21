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

        self.data = [0] * 9
        self.prev_buttons = 0
        self.buttons = 0

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

    def poll(self, motor1=False, motor2=0):
        m1 = motor1
        m2 = int(0x40 + (motor2 * 191 / 255)) if motor2 > 0 else 0
        cmd = [0x01, 0x42, 0, m1, m2, 0, 0, 0, 0]

        self.CMD.value(1)
        self.CLK.value(1)
        self.SEL.value(0)
        time.sleep_us(s.SHORT_DELAY_US)
        for i in range(9):
            self.data[i] = self.byte_transfer(cmd[i])
        self.SEL.value(1)

        self.prev_buttons = self.buttons
        self.buttons = (self.data[4] << 8) + self.data[3]

    def send(self, cmd):
        self.SEL.value(0)
        time.sleep_us(s.SHORT_DELAY_US)
        for byte in cmd:
            self.byte_transfer(byte)
        self.SEL.value(1)
        time.sleep_ms(s.READ_DELAY_MS)

    def config(self):

        self.CMD.value(1)
        self.CLK.value(1)

        for _ in range(10):
            self.send(s.CMD_ENTER_CONFIG)
            self.send(s.CMD_SET_MODE)
            self.send(s.CMD_ENABLE_RUMBLE)
            self.send(s.CMD_EXIT_CONFIG)
            self.poll()
            if self.data[1] == s.ANALOG:
                return 0
        return 1

    def is_pressed(self, button_name):
        mask = s.BUTTONS[button_name]
        return self.prev_buttons & mask and not self.buttons & mask

    def is_released(self, button_name):
        mask=s.BUTTONS[button_name]
        return not self.prev_buttons & mask and self.buttons & mask

    def is_held(self, button_name):
        mask=s.BUTTONS[button_name]
        return not self.prev_buttons & mask and not self.buttons & mask

    def get_joysticks(self, axis):
        joystick_map = {'rx': 5,'ry': 6,'lx': 7,'ly': 8}
        if axis == 'all':
            return {key: self.data[joystick_map[key]] for key in joystick_map}
        elif axis in joystick_map:
            return self.data[joystick_map[axis]]

if __name__ == "__main__":
    ps2 = PS2(s.DAT_PIN, s.CMD_PIN, s.SEL_PIN, s.CLK_PIN)
    error = 1
    error = ps2.config()
    if error:
        print("Error configuring PS2")
    else :
        print("Found PS2, configured successful")
        print("Vibrating controller for 1 second...")
        ps2.poll(True, 255)
        time.sleep(1)
        ps2.poll(False, 0)
        print("Controller is ready. Press START + SELECT together to exit.")
        while True:
            ps2.poll()
            for name in s.BUTTONS:
                if ps2.is_pressed(name):
                    print(f"{name} is being pressed")
            if ps2.is_held('L1') or ps2.is_held('R1'):
                value = ps2.get_joysticks("all")
                for axis, val in value.items():
                    print(f"{axis.upper()} = {val}")
            time.sleep_ms(s.READ_DELAY_MS)