'''
    ps2手柄控制
'''

import setting as s
import time
import _thread

class REMOTE:
    def __init__(self,ps2,mv,speed = s.SPEED):
        self.ps2 = ps2
        self.mv = mv
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.tl = False
        self.tr = False
        self.speed = speed
        self.joy_active = 0
        self.joy_mode = 0
        self.run = False
        self.task_start = False

    def joystick_mode(self):
        if self.ps2.is_held('L3') and self.ps2.is_held('R3'):
            self.joy_mode = 1 - self.joy_mode
            print(self.joy_mode)
            print("[RM] 手柄模式切换")

    def joystick_dead_out(self,value):
        #temp = int(7.8 * (128 - value))
        temp = int(1.6 * (128 - value))
        return temp if abs(temp) > s.DEAD_ZONE else 0

    def joystick_slash_speed(self,x,y):
        if x > 0 and y > 0:
            return -x if x < y else -y
        elif x < 0 and y < 0:
            return -x if x > y else -y
        elif x < 0 and y > 0:
            return x if -x < y else -y
        elif x > 0 and y < 0:
            return x if x < -y else -y

    def joystick_move(self):
        left_x = self.ps2.get_joysticks('lx')
        left_y = self.ps2.get_joysticks('ly')
        right_x = self.ps2.get_joysticks('rx')
        right_y = self.ps2.get_joysticks('ry')

        speed_lx = self.joystick_dead_out(left_x)
        speed_ly = self.joystick_dead_out(left_y)
        speed_rx = self.joystick_dead_out(right_x)
        speed_ry = self.joystick_dead_out(right_y)

        if not self.joy_mode:
            if abs(speed_ly) > 0 or abs(speed_ry) > 0 :
                self.joy_active = True
                self.mv.joystick(speed_ly,speed_ry)
            else :
                if self.joy_active:
                    self.mv.stop()
                    self.joy_active = False
        elif self.joy_mode:
            if abs(speed_lx) > 0 or abs(speed_ly) > 0 :
                self.joy_active = True
                if speed_lx * speed_ly > 0 :
                    self.mv.slash(-1*self.joystick_slash_speed(speed_lx,speed_ly),s.B)
                elif speed_lx * speed_ly < 0 :
                    self.mv.slash(-1*self.joystick_slash_speed(speed_lx,speed_ly),s.F)
                elif speed_lx == 0:
                    self.mv.straight(speed_ly)
                elif speed_ly == 0:
                    self.mv.side(speed_lx)
            elif abs(speed_rx) > 0:
                self.joy_active = True
                self.mv.turn(speed_rx)
            else :
                if self.joy_active:
                    self.mv.stop()
                    self.joy_active = False

    def dpad_and_shoulder_move(self):
        if self.ps2.is_pressed('PAD_UP'):
            self.up = True
        elif self.ps2.is_released('PAD_UP'):
            self.up = False
        if self.ps2.is_pressed('PAD_DOWN'):
            self.down = True
        elif self.ps2.is_released('PAD_DOWN'):
            self.down = False
        if self.ps2.is_pressed('PAD_LEFT'):
            self.left = True
        elif self.ps2.is_released('PAD_LEFT'):
            self.left = False
        if self.ps2.is_pressed('PAD_RIGHT'):
            self.right = True
        elif self.ps2.is_released('PAD_RIGHT'):
            self.right = False
        if self.ps2.is_pressed('L2'):
            self.tl = True
        elif self.ps2.is_released('L2'):
            self.tl = False
        if self.ps2.is_pressed('R2'):
            self.tr = True
        elif self.ps2.is_released('R2'):
            self.tr = False

        if self.up and self.left:
            self.mv.slash(self.speed,s.B)
        elif self.up and self.right:
            self.mv.slash(self.speed,s.F)
        elif self.down and self.left:
            self.mv.slash(-self.speed,s.F)
        elif self.down and self.right:
            self.mv.slash(-self.speed,s.B)
        elif self.up:
            self.mv.straight(self.speed)
        elif self.down:
            self.mv.straight(-self.speed)
        elif self.left:
            self.mv.side(self.speed)
        elif self.right:
            self.mv.side(-self.speed)
        elif self.tl:
            self.mv.turn(self.speed)
        elif self.tr:
            self.mv.turn(-self.speed)
        else:
            self.mv.stop()

    def handler(self):
        if self.ps2.is_held('START') and self.ps2.is_held('SELECT'):
            print("[RM] START和SELECT被同时按住。退出中...")
            self.run = False
            self.task_start = True
        self.joystick_mode()
        self.joystick_move()
        if not self.joy_active:
            self.dpad_and_shoulder_move()

    def listen(self):
        while self.run:
            self.ps2.poll()
            self.handler()
            time.sleep_ms(s.READ_DELAY_MS)

    def initial(self):
        error = self.ps2.config()
        if error:
            print("[RM] 无法配置PS2")
            return error
        print("[RM] 成功配置PS2")
        print("[RM] 振动1秒")
        self.ps2.poll(True, 255)
        time.sleep(1)
        self.ps2.poll(False, 0)
        print("[RM] 手柄就绪，同时按住SELECT和START退出手柄控制")
        self.run = True
        _thread.start_new_thread(self.listen,())

    # def stop(self):
    #     _thread.exit()

# if __name__ == "__main__":
#     from ps2 import PS2
#     ps2 = PS2(s.DAT_PIN, s.CMD_PIN, s.SEL_PIN, s.CLK_PIN)
#     rm = REMOTE(ps2,mv)
#     rm.initial()
#     while not rm.exit:
#         pass
#     rm.stop()