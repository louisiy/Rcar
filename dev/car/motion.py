'''
    实例运动操作
'''

import setting as s
import time

class MOVE:
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.tl = False
        self.tr = False
        self.speed = s.SPEED

    def is_any_true(self):
        return any([self.up, self.down, self.left, self.right])

def initial(controller):
    controller.set_duty(0,1000)
    controller.set_duty(1,1000)
    controller.set_duty(2,1000)
    controller.set_duty(3,1000)
    time.sleep(5)
    controller.set_duty(0,1500)
    controller.set_duty(1,1500)
    controller.set_duty(2,1500)
    controller.set_duty(3,1500)
    time.sleep(1)

def stop(controller):
    controller.set_duty(0,1500)
    controller.set_duty(1,1500)
    controller.set_duty(2,1500)
    controller.set_duty(3,1500)
    print("stop")

def straight(controller,speed):
    controller.set_duty(0,1500+speed)
    controller.set_duty(1,1500-speed)
    controller.set_duty(2,1500+speed)
    controller.set_duty(3,1500-speed)
    if speed > 0:
        print("move forward")
    elif speed < 0:
        print("move backward")

def turn(controller,speed):
    controller.set_duty(0,1500-speed)
    controller.set_duty(1,1500-speed)
    controller.set_duty(2,1500-speed)
    controller.set_duty(3,1500-speed)
    if speed > 0:
        print("turn left")
    elif speed < 0:
        print("turn right")

def side(controller,speed):
    controller.set_duty(0,1500-speed)
    controller.set_duty(1,1500-speed)
    controller.set_duty(2,1500+speed)
    controller.set_duty(3,1500+speed)
    if speed > 0:
        print("move left")
    elif speed < 0:
        print("move right")

def slash(controller,speed,direction):
    controller.set_duty(0,1500+speed*direction)
    controller.set_duty(1,1500-speed*(1-direction))
    controller.set_duty(2,1500+speed*(1-direction))
    controller.set_duty(3,1500-speed*direction)
    if speed > 0 and not direction:
        print("move forward left")
    elif speed < 0 and not direction:
        print("move backward right")
    elif speed > 0 and direction:
        print("move forward right")
    elif speed < 0 and direction:
        print("move backward left")

def joystick(controller,speed_1,speed_2):
    controller.set_duty(0,1500+speed_1)
    controller.set_duty(1,1500-speed_2)
    controller.set_duty(2,1500+speed_1)
    controller.set_duty(3,1500-speed_2)
    print("Joystick")

if __name__ == "__main__":
    import setting
    from pwm import PWMs
    def car_test(controller):
        straight(controller,s.SPEED)
        time.sleep(s.DELAY_TIME_S)

        straight(controller,-s.SPEED)
        time.sleep(s.DELAY_TIME_S)

        turn(controller,s.SPEED)
        time.sleep(s.DELAY_TIME_S)

        turn(controller,-s.SPEED)
        time.sleep(s.DELAY_TIME_S)

        side(controller,s.SPEED)
        time.sleep(s.DELAY_TIME_S)

        side(controller,-s.SPEED)
        time.sleep(s.DELAY_TIME_S)

        slash(controller,s.SPEED,s.B)
        time.sleep(s.DELAY_TIME_S)

        slash(controller,s.SPEED,s.F)
        time.sleep(s.DELAY_TIME_S)

        slash(controller,-s.SPEED,s.F)
        time.sleep(s.DELAY_TIME_S)

        slash(controller,-s.SPEED,s.B)
        time.sleep(s.DELAY_TIME_S)

        stop(controller)
        time.sleep(s.DELAY_TIME_S)

    ctrl = PWMs(s.PINs, s.FREQ)
    initial(ctrl)
    while True:
        car_test(ctrl)