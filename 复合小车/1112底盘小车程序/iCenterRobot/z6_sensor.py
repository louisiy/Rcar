'''
修改信息
作者：郑养波
日期：2025年6月1日
定义了定距跟随、自由避障、智能循迹、循迹避障等功能 可以单独进行测试
建议其他传感器在此定义
'''
from machine import Pin
import time
from iCenterRobot.z5_hcsr04 import Robot_HCSR04
# from iCenterRobot.z7_uart import Robot_UART
import iCenterRobot.z7_uart as Robot_UART
import iCenterRobot.z9_car as Robot_CAR

'''
#MOVE_TAG 			0-保留；1—循迹控制；2—自由避障；3—定距跟随
'''
MOVE_TAG = 0

MIN_PULSE_US = 1000   							#电调PWM最小值 车子反向最大速度
MAX_PULSE_US = 2000								#电调PWM最大值 车子正向最大速度
PWM_PINs = [32, 33, 25, 26, 27, 14]				#定义PWM引脚
FREQ = 50										#PWM周期50HZ

#定义跟随循迹参数
XUNJI_SPEED_PWM = 120					#底盘运动速度PWM数值
XUNJI_RUN_TIME =0.02

TEST_SPEED_PWM=120
TEST_TIME=0.5

systick_ms_gs = 0						#定距跟随（gensui）的上一次时间戳ms
systick_ms_zybz = 0						#循迹避障（ziyou bizhang）的上一次时间戳ms
systick_ms_xun = 0						#智能循迹（xunji）的时间戳ms
systick_ms_xjbz = 0						#循迹避障（xunji bizhang）的时间戳ms
systick_ms_xjfs = 0						#循迹发送（xunji bizhang）的时间戳ms
systick_ms_xjjc = 0						#循迹检测（xunji bizhang）的时间戳ms
xunji_fl_pin = 0						#左循迹传感器引脚
xunji_fr_pin = 0						#右循迹传感器引脚
xunji_rf_pin = 0						#左循迹传感器引脚
xunji_rb_pin = 0						#右循迹传感器引脚


def setup_sensor():
    global sensor
    setup_xunji(34,36,35,39)      
    sensor = Robot_HCSR04(trigger_pin=4, echo_pin=2)   # 定义超声波模块Tring控制管脚及超声波模块Echo控制管脚,S3接口

def loop_sensor():
    ziyou_bizhang()
    
# 定距跟随 定距跟随模式：试图与前方物体保持一定距离（40~60厘米）
def dingju_gensui():
    global systick_ms_gs, sensor
    ##millis() 提取系统当前时间戳，并50ms执行一次
    if millis() - systick_ms_gs > 50:
        systick_ms_gs = millis()
        dis = sensor.distance_cm()
        
        if dis < 20:
            #如果距离小于20厘米，小车后退（速度为负值）200毫秒
            Robot_CAR.houtui(TEST_SPEED_PWM)
            time.sleep(TEST_TIME)
            
            Robot_CAR.tingzhi()
            time.sleep(TEST_TIME)
            
        elif 25 < dis < 35 or dis > 70:
            #如果距离在25~35厘米之间或大于70厘米，小车停止
            Robot_CAR.tingzhi()
            time.sleep(TEST_TIME)
            
        elif 40 < dis < 60:
            #如果距离在40~60厘米之间，小车前进（速度正值）
            Robot_CAR.qianjin(TEST_SPEED_PWM)
            time.sleep(TEST_TIME)

# 自由避障
def ziyou_bizhang():
    global systick_ms_xjbz, sensor
    if millis() - systick_ms_xjbz > 50:
        systick_ms_xjbz = millis()
        dis = sensor.distance_cm()
        
#         print("dis=",dis)
        if dis >0 and dis < 40:
            print("dis=",dis)
            #如果距离小于20厘米，小车停止2秒，再后退，再左转
            Robot_CAR.houtui(TEST_SPEED_PWM)
            time.sleep(TEST_TIME)
            
            Robot_CAR.tingzhi()
#         else:
#             #否则，小车直行
#             Robot_CAR.qianjin(TEST_SPEED_PWM)
#             time.sleep(TEST_TIME)

# 智能循迹 智能循迹模式：根据两个循迹传感器的值（黑线为1，白线为0）控制小车沿黑线行驶
def car_xunji():
    global systick_ms_xun,systick_ms_xjfs,systick_ms_xjjc,uart
    if millis() - systick_ms_xun > 50:
        systick_ms_xun = millis()
        systick_ms_xjjc = millis()
        
        Robot_CAR.qianjin(XUNJI_SPEED_PWM)
        time.sleep(XUNJI_RUN_TIME*5)

        while 1:
            print("xunji_fl=",xunji_fl(),"xunji_fr=",xunji_fr(),"xunji_rf=",xunji_rf(),"xunji_rb=",xunji_rb())
            #循迹压在黑线上是0，压在白底上是1
            if xunji_fl() == 0 and xunji_fr() == 0 and xunji_rf() == 0 and xunji_rb() == 0:
                #都压在黑线上，停止开展作业
                Robot_CAR.tingzhi()
                time.sleep(0.1)        
                break
            
            if xunji_fl() == 1 and xunji_fr() == 1:
                #前循迹传感器全在外侧
                Robot_CAR.tingzhi()
                time.sleep(0.1)
                break            
            if xunji_fl() == 0 and xunji_fr() == 0 and xunji_rf() == 1 and xunji_rb() == 1:
                Robot_CAR.qianjin(XUNJI_SPEED_PWM)
                time.sleep(XUNJI_RUN_TIME)
                
            if xunji_fl() == 0 and xunji_fr() == 0 and xunji_rf() == 0 and xunji_rb() == 1:
                Robot_CAR.qianjin(XUNJI_SPEED_PWM)
                time.sleep(XUNJI_RUN_TIME)
                
            if xunji_fl() == 0 and xunji_fr() == 0 and xunji_rf() == 1 and xunji_rb() == 0:
                Robot_CAR.qianjin(XUNJI_SPEED_PWM)
                time.sleep(XUNJI_RUN_TIME)
                
            if xunji_fl() == 1 and xunji_fr() == 0:
                #前循迹传感器左偏，车子要右转
                Robot_CAR.youzhuan(XUNJI_SPEED_PWM)
                time.sleep(XUNJI_RUN_TIME)
    
            if xunji_fl() == 0 and xunji_fr() == 1:
                #前循迹传感器右偏，车子要左转
                Robot_CAR.zuozhuan(XUNJI_SPEED_PWM)
                time.sleep(XUNJI_RUN_TIME)
#             
#             Robot_CAR.tingzhi()
#             time.sleep(0.1)   
                
            if millis() - systick_ms_xjjc > 5000:
                Robot_UART.UART_send_str("yunxing")
                systick_ms_xjjc = millis()

# 循迹避障
def xunji_bizhang():
    global systick_ms_zybz, sensor
    if millis() - systick_ms_zybz > 50:
        systick_ms_zybz = millis()
        dis = sensor.distance_cm()
        #如果超声波检测到障碍物（距离小于20厘米），小车停止
        if dis < 20:
            Robot_CAR.tingzhi()
            time.sleep(XUNJI_RUN_TIME)
        else:
            Robot_CAR.tingzhi()
            time.sleep(XUNJI_RUN_TIME)
            
def setup_xunji(xunji_fl_PIN,xunji_fr_PIN,xunji_rf_PIN,xunji_rb_PIN):
    global xunji_fl_pin,xunji_fr_pin,xunji_rf_pin,xunji_rb_pin
    #设置循迹传感器的两个引脚为输入模式

    xunji_fl_pin = Pin(xunji_fl_PIN, Pin.IN)    # 将对应引脚设置为输入模式		PIN34
    xunji_fr_pin = Pin(xunji_fr_PIN, Pin.IN)    # 将对应引脚设置为输入模式		PIN36
    xunji_rf_pin = Pin(xunji_rf_PIN, Pin.IN)    # 将对应引脚设置为输入模式		PIN35
    xunji_rb_pin = Pin(xunji_rb_PIN, Pin.IN)    # 将对应引脚设置为输入模式		PIN39
        
def xunji_fl():
    return xunji_fl_pin.value()
def xunji_fr():
    return xunji_fr_pin.value()
def xunji_rf():
    return xunji_rf_pin.value()
def xunji_rb():
    return xunji_rb_pin.value()

#获取系统时间，毫秒为单位
def millis():
    return int(time.time_ns()//1000000)

'''
#MOVE_TAG 			0-保留；1—循迹控制；2—自由避障；3—定距跟随
'''
def MOV_Control():
    global MOVE_TAG
    if MOVE_TAG == 1:
       car_xunji()
    if MOVE_TAG == 2:
       ziyou_bizhang()
    if MOVE_TAG == 3:
       dingju_gensui() 


# 程序入口
if __name__ == '__main__':
    
    global uart
    
    Robot_CAR.PWM_Initial()
    Robot_UART.UART_Initial()
    setup_sensor()
    
    while 1:
        #测试时，逐一测试-郑养波
#         dingju_gensui()
#         ziyou_bizhang() 
        car_xunji()
#         xunji_bizhang()