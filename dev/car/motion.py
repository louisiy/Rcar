'''
    运动操作类
'''

import setting as s
import time

class MOTION:
    def __init__(self,pwms,flag):
        self.pwms = pwms
        self.flag = flag

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
        # print("[MV] 停止")

    def straight(self,speed):
        self.pwms.set_duty(0,1500+speed)
        self.pwms.set_duty(1,1500-speed)
        self.pwms.set_duty(2,1500+speed)
        self.pwms.set_duty(3,1500-speed)
        if speed > 0:
            print("[MV] 前进")
        elif speed < 0:
            print("[MV] 后退")

    def turn(self,speed):
        self.pwms.set_duty(0,1500-speed)
        self.pwms.set_duty(1,1500-speed)
        self.pwms.set_duty(2,1500-speed)
        self.pwms.set_duty(3,1500-speed)
        if speed > 0:
            print("[MV] 左转")
        elif speed < 0:
            print("[MV] 右转")

    def side(self,speed):
        self.pwms.set_duty(0,1500-speed)
        self.pwms.set_duty(1,1500-speed)
        self.pwms.set_duty(2,1500+speed)
        self.pwms.set_duty(3,1500+speed)
        if speed > 0:
            print("[MV] 左平移")
        elif speed < 0:
            print("[MV] 右平移")

    def slash(self,speed,direction):
        self.pwms.set_duty(0,1500+speed*direction)
        self.pwms.set_duty(1,1500-speed*(1-direction))
        self.pwms.set_duty(2,1500+speed*(1-direction))
        self.pwms.set_duty(3,1500-speed*direction)
        if speed > 0 and not direction:
            print("[MV] 向左前方")
        elif speed < 0 and not direction:
            print("[MV] 向右后方")
        elif speed > 0 and direction:
            print("[MV] 向右前方")
        elif speed < 0 and direction:
            print("[MV] 向左后方")

    def joystick(self,speed_1,speed_2):
        self.pwms.set_duty(0,1500+speed_1)
        self.pwms.set_duty(1,1500-speed_2)
        self.pwms.set_duty(2,1500+speed_1)
        self.pwms.set_duty(3,1500-speed_2)
        print("[MV] 手柄控制")

    def move_time_traj(self,speed,duration):
        start = time.time()
        while (time.time()-start)> duration:
            if flag == s.TCRT_ON:
                self.straight(speed)
            elif flag == s.TCRT_OFF:
                self.stop()
                return 1
            elif flag == s.TCRT_LEFT:
                self.turn(-speed/10)
            elif flag == s.TCRT_RIGHT:
                self.turn(speed/10)
        return 0

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