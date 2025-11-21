#####################################################
#   本例程可实现在多线程状态下实时读取手柄状态参数，在主
#   函数中通过 shoubing_chuli数据处理函数解码通讯指令解
#   码指令只含改了两个摇杆和3个按键的解码，需要更多按键的
#   解码可以自行添加。
#   if self.button(ps2.按键定义名称):
#   按键定义名称如下：
#   self.PS2_BTN_SELECT
#   self.PS2_BTN_L3 
#   self.PS2_BTN_R3 
#   self.PS2_BTN_START
#   self.PS2_BTN_UP
#   self.PS2_BTN_RIGHT 
#   self.PS2_BTN_DOWN 
#   self.PS2_BTN_LEFT
#   self.PS2_BTN_L2 
#   self.PS2_BTN_R2
#   self.PS2_BTN_L1 
#   self.PS2_BTN_R1 
#   self.PS2_BTN_TRIANGLE
#   self.PS2_BTN_CIRCLE 
#   self.PS2_BTN_CROSS 
#   self.PS2_BTN_SQUARE                        
#   版本：2025/11/20    1.0.0                        
#   作者：郝昱宇                                     
#####################################################
from machine import UART, Pin, I2C, PWM
from PS2 import PS2Controller
import time, _thread
        
def shoubin_ps2(self):
    try:
        while True:
            #数据更新
            self.update()
            time.sleep(0.1)
                
    except Exception:
        print("PS手柄故障")
        
def shoubing_chuli(self):
    small_motor          = False
    large_motor_strength = 0
    # 2. 检测数字按键
    if self.button(ps2.PS2_BTN_CROSS):
        large_motor_strength = 255
        print("按下了: 叉叉  大震！")
    
        
    if self.button(ps2.PS2_BTN_CIRCLE):
        small_motor  = True
        print("按下了: 圆圈 小震！")
        
    if self.button(ps2.PS2_BTN_UP):
        print("按下了: 上 (UP)")

    # 3. 读取模拟摇杆 (范围 0-255, 中间值约为 127-128)
    lx = self.analog_x('left')
    ly = self.analog_y('left')
    rx = self.analog_x('right')
    ry = self.analog_y('right')

    # 设置死区 (防止漂移导致误触)
    if abs(lx - 128) > 10 or abs(ly - 128) > 10:
        print(f"左摇杆: X={lx}, Y={ly}")
        
    if abs(rx - 128) > 10 or abs(ry - 128) > 10:
        print(f"右摇杆: X={rx}, Y={ry}")
        
    # 更新震动状态
    ps2.set_rumble(small_motor, large_motor_strength)
    time.sleep(0.1)
    # 震动参数初始化，停止震动
    small_motor          = False
    large_motor_strength = 0


ps2 = PS2Controller(di=19, do=18, cs=15, clk=23)
_thread.start_new_thread(shoubin_ps2 , (ps2,))
while True:
    if ps2.scan[1] != 0xFF and ps2.scan[1] != 0x00:
        print("手柄连接OK")
        ps2.init_vibration()
        time.sleep(0.5)
        break

if __name__ == '__main__':
    
    while True:
        shoubing_chuli(ps2)
        time.sleep(0.5)