
    # def mode_select(ps2,pwms):
    #     if ps2.is_pressed('SELECT'):
    #         pctrl.car_mode += 1
    #         if pctrl.car_mode >=4:
    #             pctrl.car_mode = 0
    #         print("Car_mode = ",pctrl.car_mode)

    #     elif ps2.is_pressed('START'):
    #         if pctrl.car_mode == 0:
    #             print("START+STOP")
    #             mn.stop(pwms)

    #         if pctrl.car_mode == 1:
    #             print("Path Tracking")
    #             mn.stop(pwms)

    #         if pctrl.car_mode == 2:
    #             print("Obstacle Avoidance")
    #             mn.stop(pwms)

    #         if pctrl.car_mode == 3:
    #             print("Distance Following")
    #             mn.stop(pwms)

    # def dead_or_it(value):
    #     #temp = int(7.8 * (128 - value))
    #     temp = int(4 * (128 - value))
    #     return temp if abs(temp) > s.DEAD_ZONE else 0

    # def slash_speed(x,y):
    #     if x > 0 and y > 0:
    #         return -x if x < y else -y
    #     elif x < 0 and y < 0:
    #         return -x if x > y else -y
    #     elif x < 0 and y > 0:
    #         return x if -x < y else -y
    #     elif x > 0 and y < 0:
    #         return x if x < -y else -y

    # def joystick_move(ps2,pwms,pctrl):
    #     if ps2.is_held('L3') and ps2.is_held('R3'):
    #         pctrl.joy_mode = 1 - pctrl.joy_mode
    #         print(pctrl.joy_mode)
    #         print("Joystick Mode is switched.")
    #         time.sleep_ms(s.READ_DELAY_MS)

    #     left_x = ps2.get_joysticks('lx')
    #     left_y = ps2.get_joysticks('ly')
    #     right_x = ps2.get_joysticks('rx')
    #     right_y = ps2.get_joysticks('ry')

    #     speed_lx = dead_or_it(left_x)
    #     speed_ly = dead_or_it(left_y)
    #     speed_rx = dead_or_it(right_x)
    #     speed_ry = dead_or_it(right_y)

    #     if not pctrl.joy_mode:
    #         if abs(speed_ly) > 0 or abs(speed_ry) > 0 :
    #             pctrl.joy_active = True
    #             mn.joystick(pwms,speed_ly,speed_ry)
    #         else :
    #             if pctrl.joy_active:
    #                 mn.stop(pwms)
    #                 pctrl.joy_active = False
    #     elif pctrl.joy_mode:
    #         if abs(speed_lx) > 0 or abs(speed_ly) > 0 :
    #             pctrl.joy_active = True
    #             if speed_lx * speed_ly > 0 :
    #                 mn.slash(pwms,slash_speed(speed_lx,speed_ly),B)
    #             elif speed_lx * speed_ly < 0 :
    #                 mn.slash(pwms,slash_speed(speed_lx,speed_ly),F)
    #             elif speed_lx == 0:
    #                 mn.straight(pwms,-speed_ly)
    #             elif speed_ly == 0:
    #                 mn.side(pwms,-speed_lx)
    #         elif abs(speed_rx) > 0:
    #             pctrl.joy_active = True
    #             mn.turn(pwms,-speed_rx)
    #         else :
    #             if pctrl.joy_active:
    #                 mn.stop(pwms)
    #                 pctrl.joy_active = False

    # def dpad_and_shoulder_move(ps2,pwms,mv):
    #     if ps2.is_pressed('PAD_UP'):
    #         mv.up = True
    #     elif ps2.is_released('PAD_UP'):
    #         mv.up = False
    #     if ps2.is_pressed('PAD_DOWN'):
    #         mv.down = True
    #     elif ps2.is_released('PAD_DOWN'):
    #         mv.down = False
    #     if ps2.is_pressed('PAD_LEFT'):
    #         mv.left = True
    #     elif ps2.is_released('PAD_LEFT'):
    #         mv.left = False
    #     if ps2.is_pressed('PAD_RIGHT'):
    #         mv.right = True
    #     elif ps2.is_released('PAD_RIGHT'):
    #         mv.right = False
    #     if ps2.is_pressed('L2'):
    #         mv.tl = True
    #     elif ps2.is_released('L2'):
    #         mv.tl = False
    #     if ps2.is_pressed('R2'):
    #         mv.tr = True
    #     elif ps2.is_released('R2'):
    #         mv.tr = False

    #     if mv.up and mv.left:
    #         mn.slash(pwms,mv.speed,s.B)
    #     elif mv.up and mv.right:
    #         mn.slash(pwms,mv.speed,s.F)
    #     elif mv.down and mv.left:
    #         mn.slash(pwms,-mv.speed,s.F)
    #     elif mv.down and mv.right:
    #         mn.slash(pwms,-mv.speed,s.B)
    #     elif mv.up:
    #         mn.straight(pwms,mv.speed)
    #     elif mv.down:
    #         mn.straight(pwms,-mv.speed)
    #     elif mv.left:
    #         mn.side(pwms,mv.speed)
    #     elif mv.right:
    #         mn.side(pwms,-mv.speed)
    #     elif mv.tl:
    #         mn.turn(pwms,mv.speed)
    #     elif mv.tr:
    #         mn.turn(pwms,-mv.speed)
    #     else:
    #         mn.stop(pwms)

    # def handler(ps2, pwms, mv, pctrl):
    #     #     mode_select(ps2,pwms)
    #     joystick_move(ps2,pwms,pctrl)

    #     if not pctrl.joy_active:
    #         dpad_and_shoulder_move(ps2,pwms,mv)

    #     return 0

