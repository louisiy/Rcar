'''
    超声波测距传感器HC-SR04
'''

import setting as s
import time
from machine import Pin, time_pulse_us

class HC_SR04:
    def __init__(self, trig_pin, echo_pin, timeout_us=1000*30):
        self.timeout = timeout_us
        self.trigger = Pin(trig_pin, Pin.OUT)
        self.trigger.value(0)
        self.echo = Pin(echo_pin, Pin.IN)

    def _measure(self):
        self.trigger.value(0)
        time.sleep_us(2)
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            t = time_pulse_us(self.echo, 1, self.timeout)
            return t
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('[HCSR] Out of range')
            raise ex

    def distance_mm(self):
        t = self._measure()
        # 343.2 m/s = 343.2 mm/ms = 343.2 mm/(1000us) = 0.3432 mm/us
        # 0.5t long v_e = 0.1712 mm/us
        mm = t * 0.1712
        return mm

    def distance_cm(self):
        t = self._measure()
        # v_e = 0.01712 cm/us
        cm = t * 0.01712
        return cm

if __name__ == "__main__":
    hcsr = HC_SR04(trig_pin = s.TRIG_PIN, echo_pin = s.ECHO_PIN)
    while True:
        d = hcsr.distance_cm()
        print (f"{d:.1f} cm\n")
        time.sleep(0.1)