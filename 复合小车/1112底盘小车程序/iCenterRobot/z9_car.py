'''
编写信息
作者：郑养波
日期：2025年7月3日
'''
import machine
import time

MIN_PULSE_US = 1000   							#电调PWM最小值 车子反向最大速度
MAX_PULSE_US = 2000								#电调PWM最大值 车子正向最大速度
PWM_PINs = [32, 33, 25, 26, 27, 14]				#定义PWM引脚
FREQ = 50										#PWM周期50HZ
SPEED_PWM = 200									#底盘运动速度PWM数值
TEST_SPEED_PWM = 200							#底盘运动速度PWM数值
SPEED_PWM_DIF = 10								#底盘运动速度PWM数值偏差
RUN_TIME = 1    								#运动时间
TEST_TIME = 1									#测试运动时间

class Robot_PWMController:
    def __init__(self, pins, freq): 
        """
        PWM控制器初始化
        :param pins: 引脚列表 (例如 [32, 33, 25, 26, 27, 14])
        :param freq: 初始PWM频率 (默认1000Hz)
        """
        self.pwm_pins = []
        self.freq = freq
        
        # 初始化所有引脚为PWM输出machine.PWM(machine.Pin(27))
        for pin in pins:
            self.pwm_pins.append(machine.PWM(machine.Pin(pin), freq=self.freq, duty=0))
    
    def set_frequency(self, freq):
        """
        设置所有引脚的PWM频率
        :param freq: PWM频率 (Hz)
        """
        self.freq = freq
        for pwm in self.pwm_pins:
            pwm.freq(self.freq)
    
    def set_duty(self, pin_index, pwm):
        """
        设置指定引脚的占空比
        :param pin_index: 引脚索引 (0~5)
        :param duty: 占空比 (0~65535)
        """
        
        if pwm > MAX_PULSE_US:
            pwm = MAX_PULSE_US
        elif pwm < MIN_PULSE_US:
            pwm = MIN_PULSE_US
        
        self.duty = int(((pwm * 65535) / (1000000 /FREQ)))
        print("PWM=",pwm,"Duty=",self.duty)

        if 0 <= pin_index < len(self.pwm_pins):
            
            self.pwm_pins[pin_index].duty_u16(self.duty)
    
    def deinit(self):
        """关闭所有PWM输出并释放资源"""
        for pwm in self.pwm_pins:
            pwm.deinit()
            
def PWM_Initial():
    global controller
    controller = Robot_PWMController(PWM_PINs, FREQ)
    #初始化触发引脚
    controller.set_duty(0,1000)
    controller.set_duty(1,1000)
    controller.set_duty(2,1000)
    controller.set_duty(3,1000)
    time.sleep(5)
    tingzhi()    
    time.sleep(1)

#停止函数
def tingzhi():
    controller.set_duty(0,1500)
    controller.set_duty(1,1500)
    controller.set_duty(2,1500)
    controller.set_duty(3,1500)
    print("tingzhi")
#前进函数
def qianjin(speed_pwm):
    controller.set_duty(0,1500+speed_pwm)
    controller.set_duty(1,1500-speed_pwm)
    controller.set_duty(2,1500+speed_pwm)
    controller.set_duty(3,1500-speed_pwm)
    print("qianjin")
#后退函数
def houtui(speed_pwm):
    controller.set_duty(0,1500-speed_pwm)
    controller.set_duty(1,1500+speed_pwm)
    controller.set_duty(2,1500-speed_pwm)
    controller.set_duty(3,1500+speed_pwm)
    print("houtui")
#左转函数
def zuozhuan(speed_pwm):
    controller.set_duty(0,1500-speed_pwm)
    controller.set_duty(1,1500-speed_pwm)
    controller.set_duty(2,1500-speed_pwm)
    controller.set_duty(3,1500-speed_pwm)
    print("zuozhuan")
#右转函数
def youzhuan(speed_pwm):
    controller.set_duty(0,1500+speed_pwm)
    controller.set_duty(1,1500+speed_pwm)
    controller.set_duty(2,1500+speed_pwm)
    controller.set_duty(3,1500+speed_pwm)
    print("youzhuan")
#左平移函数
def zuopingyi(speed_pwm):
    controller.set_duty(0,1500-speed_pwm)
    controller.set_duty(1,1500-speed_pwm)
    controller.set_duty(2,1500+speed_pwm)
    controller.set_duty(3,1500+speed_pwm)
    print("zuopingyi")
#右平移函数
def youpingyi(speed_pwm):
    controller.set_duty(0,1500+speed_pwm)
    controller.set_duty(1,1500+speed_pwm)
    controller.set_duty(2,1500-speed_pwm)
    controller.set_duty(3,1500-speed_pwm)
    print("youpingyi")
#底盘测试函数
def car_test():
    qianjin(TEST_SPEED_PWM)
    time.sleep(TEST_TIME)
    houtui(TEST_SPEED_PWM)
    time.sleep(TEST_TIME)
    zuozhuan(TEST_SPEED_PWM)
    time.sleep(TEST_TIME)
    youzhuan(TEST_SPEED_PWM)
    time.sleep(TEST_TIME)
    zuopingyi(TEST_SPEED_PWM)
    time.sleep(TEST_TIME)
    youpingyi(TEST_SPEED_PWM)
    time.sleep(TEST_TIME)
    tingzhi()
    time.sleep(TEST_TIME)

# 使用示例
if __name__ == "__main__":

    PWM_Initial()
    
    while True:
        qianjin(TEST_SPEED_PWM)
        print("qianjin")
        time.sleep(10)
        
        tingzhi()
        print("tingzhi")
        time.sleep(3)
        
        houtui(TEST_SPEED_PWM)
        print("houtui")
        time.sleep(10)
        
        tingzhi()
        print("tingzhi")
        time.sleep(3)
        
        zuopingyi(TEST_SPEED_PWM)
        print("zuopingyi")
        time.sleep(10)
        
        tingzhi()
        print("tingzhi")
        time.sleep(3)
        
        youpingyi(TEST_SPEED_PWM)
        print("youpingyi")
        time.sleep(10)
        
        tingzhi()
        print("tingzhi")
        time.sleep(3)
        
        zuozhuan(TEST_SPEED_PWM)
        print("zuozhuan")
        time.sleep(10)
        
        tingzhi()
        print("tingzhi")
        time.sleep(3)
        
        youzhuan(TEST_SPEED_PWM)
        print("youzhuan")
        time.sleep(10)
        
        tingzhi()
        print("tingzhi")
        time.sleep(3)