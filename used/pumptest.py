from machine import UART, Pin
import time
uart = UART(1, baudrate=9600, bits=8, parity=None, stop=1, tx=2, rx=3)
speed = b'\xCC\x00\x4B\x20\x03\xDD\x17\x02'
uart.write(speed)
while True:
    if uart.any():
        response = uart.read()
        if response == b'\xcc\x00\x02\x00\x00\xdd\xab\x01':
            print("转速初始化成功")
            break
    time.sleep(0.1)
    print(".",end="")
    
def send(command):
    precalculated_commands = {
    0.0: b'\xCC\x00\x45\x00\x00\xDD\xEE\x01',
    0.5: b'\xCC\x00\x4D\xB0\x04\xDD\xAA\x02',
    1.0: b'\xCC\x00\x4D\x60\x09\xDD\x5F\x02',
    1.5: b'\xCC\x00\x4D\x10\x0E\xDD\x14\x02',
    2.0: b'\xCC\x00\x4D\xC0\x12\xDD\xC8\x02',
    2.5: b'\xCC\x00\x4D\x70\x17\xDD\x7D\x02',
    3.0: b'\xCC\x00\x4D\x20\x1C\xDD\x32\x02',
    3.5: b'\xCC\x00\x4D\xD0\x20\xDD\xE6\x02',
    4.0: b'\xCC\x00\x4D\x80\x25\xDD\x9B\x02',
    4.5: b'\xCC\x00\x4D\x30\x2A\xDD\x50\x02',
    5.0: b'\xCC\x00\x4D\xE0\x2E\xDD\x04\x03'
    }
    uart.write(precalculated_commands[command])
    print("命令已发送")
    # 读取响应
    while True:
        if uart.any():
            response = uart.read()
            if response == b'\xcc\x00\x00\x00\x00\xdd\xa9\x01':
                print(1)
                return 1
        time.sleep(0.1)
        print(".",end="")
        
if __name__ == "__main__":
    # 测试单个体积
    print("=== 注射泵控制测试 ===")
    send(2.5)