'''
    PWM端口类
'''

import setting as s
import machine

class PWMs:
    def __init__(self, pins, freq):
        self.pins = []
        self.freq = freq
        self.duty = 0

        for pin in pins:
            self.pins.append(machine.PWM(machine.Pin(pin), freq=self.freq, duty=0))

    def set_frequency(self, freq):
        self.freq = freq
        for pin in self.pins:
            pin.freq(self.freq)

    def set_duty(self, pin_index, pulse_us):
        if pulse_us > s.MAX_PULSE_US:
            pulse_us = s.MAX_PULSE_US
        elif pulse_us < s.MIN_PULSE_US:
            pulse_us = s.MIN_PULSE_US

        self.duty = int(((pulse_us * 65535) / (1000000 /self.freq)))
        # print("Pin=",pin_index,"Duty=",self.duty)

        if 0 <= pin_index < len(self.pins):
            self.pins[pin_index].duty_u16(self.duty)

    def close(self):
        for pin in self.pins:
            pin.deinit()