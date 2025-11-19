'''
    运动操作类
'''

import setting as s
import time

class MOTION:
    def __init__(self,pwms,speed = s.SPEED):
        self.pwms = pwms
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.tl = False
        self.tr = False
        self.speed = speed

    def is_any_true(self):
        return any([self.up, self.down, self.left, self.right])

    def initial(self):
        self.pwms.set_duty(0,1000)
        self.pwms.set_duty(1,1000)
        self.pwms.set_duty(2,1000)
        self.pwms.set_duty(3,1000)
        time.sleep(5)
        self.pwms.set_duty(0,1500)
        self.pwms.set_duty(1,1500)
        self.pwms.set_duty(2,1500)
        self.pwms.set_duty(3,1500)
        time.sleep(1)

    def stop(self):
        self.pwms.set_duty(0,1500)
        self.pwms.set_duty(1,1500)
        self.pwms.set_duty(2,1500)
        self.pwms.set_duty(3,1500)
        print("stop")

    def straight(self,speed):
        self.pwms.set_duty(0,1500+speed)
        self.pwms.set_duty(1,1500-speed)
        self.pwms.set_duty(2,1500+speed)
        self.pwms.set_duty(3,1500-speed)
        if speed > 0:
            print("move forward")
        elif speed < 0:
            print("move backward")

    def turn(self,speed):
        self.pwms.set_duty(0,1500-speed)
        self.pwms.set_duty(1,1500-speed)
        self.pwms.set_duty(2,1500-speed)
        self.pwms.set_duty(3,1500-speed)
        if speed > 0:
            print("turn left")
        elif speed < 0:
            print("turn right")

    def side(self,speed):
        self.pwms.set_duty(0,1500-speed)
        self.pwms.set_duty(1,1500-speed)
        self.pwms.set_duty(2,1500+speed)
        self.pwms.set_duty(3,1500+speed)
        if speed > 0:
            print("move left")
        elif speed < 0:
            print("move right")

    def slash(self,speed,direction):
        self.pwms.set_duty(0,1500+speed*direction)
        self.pwms.set_duty(1,1500-speed*(1-direction))
        self.pwms.set_duty(2,1500+speed*(1-direction))
        self.pwms.set_duty(3,1500-speed*direction)
        if speed > 0 and not direction:
            print("move forward left")
        elif speed < 0 and not direction:
            print("move backward right")
        elif speed > 0 and direction:
            print("move forward right")
        elif speed < 0 and direction:
            print("move backward left")

    def joystick(self,speed_1,speed_2):
        self.pwms.set_duty(0,1500+speed_1)
        self.pwms.set_duty(1,1500-speed_2)
        self.pwms.set_duty(2,1500+speed_1)
        self.pwms.set_duty(3,1500-speed_2)
        print("Joystick")

if __name__ == "__main__":
    import setting
    from pwm import PWMs
    def car_test():
        mv.straight(s.SPEED)
        time.sleep(s.DELAY_TIME_S)

        mv.straight(-s.SPEED)
        time.sleep(s.DELAY_TIME_S)

        mv.turn(s.SPEED)
        time.sleep(s.DELAY_TIME_S)

        mv.turn(-s.SPEED)
        time.sleep(s.DELAY_TIME_S)

        mv.side(s.SPEED)
        time.sleep(s.DELAY_TIME_S)

        mv.side(-s.SPEED)
        time.sleep(s.DELAY_TIME_S)

        mv.slash(s.SPEED,s.B)
        time.sleep(s.DELAY_TIME_S)

        mv.slash(s.SPEED,s.F)
        time.sleep(s.DELAY_TIME_S)

        mv.slash(-s.SPEED,s.F)
        time.sleep(s.DELAY_TIME_S)

        mv.slash(-s.SPEED,s.B)
        time.sleep(s.DELAY_TIME_S)

        mv.stop()
        time.sleep(s.DELAY_TIME_S)

    pwms = PWMs(s.PINs, s.FREQ)
    mv = MOTION(pwms)
    mv.initial()
    while True:
        car_test()
    pwms.close()