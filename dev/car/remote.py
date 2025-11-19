'''
    ps2手柄控制
'''

import setting as s
import motion as mn
import time

class PS2CTRL:
    def __init__(self):
        self.joy_active = 0
        self.joy_mode = 0
        self.car_mode = 0

def initial(ps2):
    error = ps2.config(pressure=True, rumble=True)
    if error:
        print("Error configuring PS2")
        while True:
            pass
    print("Found PS2, configured successful")
    if ps2.is_rumble_enabled:
        print("Vibrating controller for 2 second...")
        ps2.read(True, 255)
        time.sleep(2)
        ps2.read(False, 0)
    print("Controller is ready. Press START + SELECT together to exit.")

def mode_select(ps2,ctrl):
    if ps2.is_pressed('SELECT'):
        pctrl.car_mode += 1
        if pctrl.car_mode >=4:
            pctrl.car_mode = 0
        print("Car_mode = ",pctrl.car_mode)

    elif ps2.is_pressed('START'):
        if pctrl.car_mode == 0:
            print("START+STOP")
            mn.stop(ctrl)

        if pctrl.car_mode == 1:
            print("Path Tracking")
            mn.stop(ctrl)

        if pctrl.car_mode == 2:
            print("Obstacle Avoidance")
            mn.stop(ctrl)

        if pctrl.car_mode == 3:
            print("Distance Following")
            mn.stop(ctrl)

def dead_or_it(value):
    #temp = int(7.8 * (128 - value))
    temp = int(4 * (128 - value))
    return temp if abs(temp) > s.DEAD_ZONE else 0

def slash_speed(x,y):
    if x > 0 and y > 0:
        return -x if x < y else -y
    elif x < 0 and y < 0:
        return -x if x > y else -y
    elif x < 0 and y > 0:
        return x if -x < y else -y
    elif x > 0 and y < 0:
        return x if x < -y else -y

def joystick_move(ps2,ctrl,pctrl):
    if ps2.is_held('L3') and ps2.is_held('R3'):
        pctrl.joy_mode = 1 - pctrl.joy_mode
        print(pctrl.joy_mode)
        print("Joystick Mode is switched.")
        time.sleep_ms(s.READ_DELAY_MS)

    left_x = ps2.get_joysticks('lx')
    left_y = ps2.get_joysticks('ly')
    right_x = ps2.get_joysticks('rx')
    right_y = ps2.get_joysticks('ry')

    speed_lx = dead_or_it(left_x)
    speed_ly = dead_or_it(left_y)
    speed_rx = dead_or_it(right_x)
    speed_ry = dead_or_it(right_y)

    if not pctrl.joy_mode:
        if abs(speed_ly) > 0 or abs(speed_ry) > 0 :
            pctrl.joy_active = True
            mn.joystick(ctrl,speed_ly,speed_ry)
        else :
            if pctrl.joy_active:
                mn.stop(ctrl)
                pctrl.joy_active = False
    elif pctrl.joy_mode:
        if abs(speed_lx) > 0 or abs(speed_ly) > 0 :
            pctrl.joy_active = True
            if speed_lx * speed_ly > 0 :
                mn.slash(ctrl,slash_speed(speed_lx,speed_ly),B)
            elif speed_lx * speed_ly < 0 :
                mn.slash(ctrl,slash_speed(speed_lx,speed_ly),F)
            elif speed_lx == 0:
                mn.straight(ctrl,-speed_ly)
            elif speed_ly == 0:
                mn.side(ctrl,-speed_lx)
        elif abs(speed_rx) > 0:
            pctrl.joy_active = True
            mn.turn(ctrl,-speed_rx)
        else :
            if pctrl.joy_active:
                mn.stop(ctrl)
                pctrl.joy_active = False

def dpad_and_shoulder_move(ps2,ctrl,mv):
    if ps2.is_pressed('PAD_UP'):
        mv.up = True
    elif ps2.is_released('PAD_UP'):
        mv.up = False
    if ps2.is_pressed('PAD_DOWN'):
        mv.down = True
    elif ps2.is_released('PAD_DOWN'):
        mv.down = False
    if ps2.is_pressed('PAD_LEFT'):
        mv.left = True
    elif ps2.is_released('PAD_LEFT'):
        mv.left = False
    if ps2.is_pressed('PAD_RIGHT'):
        mv.right = True
    elif ps2.is_released('PAD_RIGHT'):
        mv.right = False
    if ps2.is_pressed('L2'):
        mv.tl = True
    elif ps2.is_released('L2'):
        mv.tl = False
    if ps2.is_pressed('R2'):
        mv.tr = True
    elif ps2.is_released('R2'):
        mv.tr = False

    if mv.up and mv.left:
        mn.slash(ctrl,mv.speed,s.B)
    elif mv.up and mv.right:
        mn.slash(ctrl,mv.speed,s.F)
    elif mv.down and mv.left:
        mn.slash(ctrl,-mv.speed,s.F)
    elif mv.down and mv.right:
        mn.slash(ctrl,-mv.speed,s.B)
    elif mv.up:
        mn.straight(ctrl,mv.speed)
    elif mv.down:
        mn.straight(ctrl,-mv.speed)
    elif mv.left:
        mn.side(ctrl,mv.speed)
    elif mv.right:
        mn.side(ctrl,-mv.speed)
    elif mv.tl:
        mn.turn(ctrl,mv.speed)
    elif mv.tr:
        mn.turn(ctrl,-mv.speed)
    else:
        mn.stop(ctrl)

def handler(ps2, ctrl, mv, pctrl):
    if ps2.is_held('START') and ps2.is_held('SELECT'):
        print("START and SELECT pressed together. Exiting...")
        return 1

#     mode_select(ps2,ctrl)

    joystick_move(ps2,ctrl,pctrl)

    if not pctrl.joy_active:
        dpad_and_shoulder_move(ps2,ctrl,mv)

    return 0


if __name__ == "__main__":
    import setting, time
    from ps2 import PS2
    def ps2_test(ps2):
        if ps2.is_held('START') and ps2.is_held('SELECT'):
            print("START and SELECT pressed together. Exiting...")
            return 1
        for name in s.BUTTONS:
            if ps2.is_held(name):
                print(f"{name} is being held")
        if ps2.is_pressure_enabled:
            if ps2.is_held('L1') or ps2.is_held('R1'):
                value = ps2.get_joysticks("all")
                for axis, val in value.items():
                    print(f"{axis.upper()} = {val}")
        return 0

    ps2 = PS2(s.DAT_PIN, s.CMD_PIN, s.SEL_PIN, s.CLK_PIN)
    initial(ps2)
    while True:
        if not ps2.read():
            continue
        if ps2_test(ps2):
            break
        time.sleep_ms(s.READ_DELAY_MS)