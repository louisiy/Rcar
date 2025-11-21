# 文件名: ps2.py
from machine import Pin
import time

class PS2Controller:
    def __init__(self, di, do, cs, clk):
        self.di = Pin(di, Pin.IN)
        self.do = Pin(do, Pin.OUT)
        self.cs = Pin(cs, Pin.OUT)
        self.clk = Pin(clk, Pin.OUT)
        
        self.cs.value(1)
        self.clk.value(1)
        
        # 震动参数
        self.rumble_small = 0x00 # 0x00关, 0xFF开
        self.rumble_large = 0x00 # 0x00-0xFF 强度
        
        # 按键定义
        self.PS2_BTN_SELECT = 0x0001
        self.PS2_BTN_L3 = 0x0002
        self.PS2_BTN_R3 = 0x0004
        self.PS2_BTN_START = 0x0008
        self.PS2_BTN_UP = 0x0010
        self.PS2_BTN_RIGHT = 0x0020
        self.PS2_BTN_DOWN = 0x0040
        self.PS2_BTN_LEFT = 0x0080
        self.PS2_BTN_L2 = 0x0100
        self.PS2_BTN_R2 = 0x0200
        self.PS2_BTN_L1 = 0x0400
        self.PS2_BTN_R1 = 0x0800
        self.PS2_BTN_TRIANGLE = 0x1000
        self.PS2_BTN_CIRCLE = 0x2000
        self.PS2_BTN_CROSS = 0x4000
        self.PS2_BTN_SQUARE = 0x8000

        self.scan = [0x00] * 9
        self.data = 0

    def _transfer(self, byte):
        """模拟SPI传输"""
        res = 0
        for i in range(8):
            if byte & (1 << i):
                self.do.value(1)
            else:
                self.do.value(0)
            self.clk.value(0)
            time.sleep_us(10)
            if self.di.value():
                res |= (1 << i)
            self.clk.value(1)
            time.sleep_us(10)
        return res

    def _send_command(self, command_bytes):
        """发送一串指令"""
        self.cs.value(0)
        time.sleep_us(20)
        for b in command_bytes:
            self._transfer(b)
            time.sleep_us(10)
        self.cs.value(1)
        time.sleep_ms(10) # 指令间通常需要较长延时

    def init_vibration(self):
        """初始化震动模式 (魔法指令)"""
        print("正在配置震动模式...")
        # 1. 进入配置模式 (Enter Config Mode)
        self._send_command([0x01, 0x43, 0x00, 0x01, 0x00])
        # 2. 开启模拟模式并锁定 (Turn on Analog Mode & Lock)
        self._send_command([0x01, 0x44, 0x00, 0x01, 0x03, 0x00, 0x00, 0x00, 0x00])
        # 3. 映射电机 (Map Motors: 启用震动字节发送)
        #    这一步告诉手柄：我会在Polling的第3和第4个字节发震动数据
        self._send_command([0x01, 0x4D, 0x00, 0x00, 0x01])
        # 4. 退出配置模式 (Exit Config Mode)
        self._send_command([0x01, 0x43, 0x00, 0x00, 0x5A, 0x5A, 0x5A, 0x5A, 0x5A])
        print("震动配置完成")

    def set_rumble(self, small, large):
        """
        设置震动
        :param small: True/False (小电机，通常只有开关)
        :param large: 0-255 (大电机，可调强度)
        """
        self.rumble_small = 0xFF if small else 0x00
        self.rumble_large = int(large)
        if self.rumble_large > 255: self.rumble_large = 255

    def update(self):
        self.cs.value(0)
        time.sleep_us(20)
        
        # 标准轮询指令: 0x01, 0x42, 0x00, 小电机, 大电机, ...
        self._transfer(0x01)
        self.scan[1] = self._transfer(0x42)
        self.scan[2] = self._transfer(0x00)
        
        # 关键点：在这里发送震动数据！
        self.scan[3] = self._transfer(self.rumble_small) # Byte 4: 小电机
        self.scan[4] = self._transfer(self.rumble_large) # Byte 5: 大电机
        
        self.scan[5] = self._transfer(0x00)
        self.scan[6] = self._transfer(0x00)
        self.scan[7] = self._transfer(0x00)
        self.scan[8] = self._transfer(0x00)
        
        self.cs.value(1)
        
        self.data = (~((self.scan[4] << 8) | self.scan[3])) & 0xFFFF
        
    def button(self, btn):
        return (self.data & btn) == btn

    def analog_x(self, stick='left'):
        return self.scan[7] if stick == 'left' else self.scan[5]

    def analog_y(self, stick='left'):
        return self.scan[8] if stick == 'left' else self.scan[6]