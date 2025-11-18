'''
    循迹传感器TCRT5000
'''

import setting
import time
from machine import Pin

class TCRT:
    def __init__(self,l_pin,r_pin):
        self.left = Pin(l_pin, Pin.IN)
        self.right = Pin(r_pin, Pin.IN)

    def state(self):
        if not self.left.value() and not self.right.value():
            return TCRT_ON
        elif self.left.value() and not self.right.value():
            return TCRT_LEFT
        elif not self.left.value() and self.right.value():
            return TCRT_RIGHT
        elif self.left.value() and self.right.value():
            return TCRT_OFF

if __name__ == '__main__':
    tcrt = TCRT(TCRT_L_PIN,TCRT_R_PIN )
    while True:
        print("left=",tcrt.left.value(),"right=",tcrt.right.value())
        flag = tcrt.state()
        if flag == TCRT_ON:
            print("nothing")
        elif flag == TCRT_OFF:
            print("over")
        elif flag == TCRT_LEFT:
            print("turn right")
        elif flag == TCRT_RIGHT:
            print("turn left")
        time.sleep(0.1)