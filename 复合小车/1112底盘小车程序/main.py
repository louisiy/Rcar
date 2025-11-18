'''
编写信息
作者：郑养波
日期：2025年7月3日
'''
#一、库文件导入
import machine
import time
# 从`factory`包中导入各种自定义模块，分别用于控制LED、蜂鸣器、按键、ADC、串口、文件、舵机、运动学和PS2手柄
from iCenterRobot.z1_led import Robot_LED
from iCenterRobot.z2_beep import Robot_BEEP
from iCenterRobot.z3_key import Robot_KEY
from iCenterRobot.z4_adc import Robot_ADC
from iCenterRobot.z5_hcsr04 import Robot_HCSR04
import iCenterRobot.z6_sensor as Robot_AI   #导入传感器模块并重命名
import iCenterRobot.z7_uart as Robot_UART
import iCenterRobot.z8_ps2 as Robot_PS2
import iCenterRobot.z9_car as Robot_CAR

'''
#MOVE_TAG  0-保留；1—循迹控制；2—自由避障；3—定距跟随
'''
    
if __name__ == '__main__':
    global nled,beep,key
    
    #实例化对象
    nled = Robot_LED()                                    # 实例化led灯对象
    beep = Robot_BEEP()                                   # 实例化蜂鸣器对象
    key = Robot_KEY()                                     # 实例化 按键 对象
    
    Robot_UART.UART_Initial()								# 初始化 串口
    Robot_PS2.PS2_Initial()									# 初始化 手柄
    Robot_CAR.PWM_Initial()									# 初始化 PWM-电调驱动
    Robot_AI.setup_sensor()									# 初始化 传感器
    
    beep.beep_on_times(3,0.1)                          # 启动完成
    print('main init ok')
    
    while 1:    									# 无限循环
        nled.loop_nled()    						# led灯循环亮灭
        Robot_UART.UART_recv_str()					# 循环收取串口数据
        Robot_PS2.PS2_Control()						# 循环检测手柄数据
        Robot_AI.ziyou_bizhang()					# 循环自由避障模式
        time.sleep(0.1)