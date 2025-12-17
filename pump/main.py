'''
    注射泵客户端 ID:PUMP
'''


import network
import time
import socket
from machine import Pin, PWM, UART

# UART
uart = UART(1, baudrate=9600, bits=8, parity=None, stop=1, tx=2, rx=3)

# PUMP
RESET = b'\xCC\x00\x45\x00\x00\xDD\xEE\x01'
DRPM400 = b'\xCC\x00\x4B\x90\x01\xDD\x85\x02'
#吸
EX4ML  = b'\xCC\x00\x4D\x80\x25\xDD\x9B\x02'
#排
DI4ML = b'\xCC\x00\x42\x80\x25\xDD\x90\x02'

def send(msg):
    rlen = 8
    timeout = 5

    uart.write(msg)
    print(f"[UART] 发送 {msg}")

    start = time.time()
    buf = bytearray()

    while time.time() - start < timeout:
        if uart.any():
            buf.extend(uart.read())
            if len(buf) >= rlen:
                print("[UART] 接收", bytes(buf))
                return bytes(buf)
        time.sleep(0.001)

    print("[UART] 超时未接收到回应")
    return None

def init():
    send(DRPM400)
    send(RESET)
    print(f"[PUMP] 初始化完毕")

def aspirate():
    r = send(EX4ML)
    if not r :
        print(f"[PUMP] 泵未响应")
        return 1
    return 0

def dispense():
    r = send(DI4ML)
    if not r :
        print(f"[PUMP] 泵未响应")
        return 1
    return 0

# WIFI TCP
WIFI_SSID = "CAMAP"
WIFI_PASSWORD = "12345678"

SERVER_IP = "192.168.66.1"
SERVER_PORT = 8080

def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("[WiFi] 连接中...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("[WiFi] 连接成功:", wlan.ifconfig())
    return wlan

def server_connect():
    while True:
        try:
            sock = socket.socket()
            print("[TCP] 尝试连接服务器...")
            sock.connect((SERVER_IP, SERVER_PORT))
            print("[TCP] 连接成功")
            return sock
        except Exception as e:
            print("[TCP] 连接失败:", e)
            time.sleep(1)

# CMD
_cmd = {}

def reg(name):
    def deco(fn):
        _cmd[name] = fn
        return fn
    return deco

@reg("XI")
def xiye(sock):
    print("[PUMP] 吸取")
    err = aspirate()
    time.sleep(5)
    if err:
        sock.send(b"PUMP:EER")
        print("[TCP] 发送: PUMP:ERR")
    else:
        sock.send(b"PUMP:XOK")
        print("[TCP] 发送: PUMP:XOK")

@reg("PAI")
def paiye(sock):
    print("[PUMP] 排液")
    err = dispense()
    time.sleep(5)
    if err:
        sock.send(b"PUMP:EER")
        print("[TCP] 发送: PUMP:ERR")
    else:
        sock.send(b"PUMP:POK")
        print("[TCP] 发送: PUMP:POK")

def main():
    wlan = wifi_connect()
    sock = server_connect()

    sock.send(b"PUMP:HELLO\n")
    print("[TCP] 发送: PUMP:HELLO")
    init()

    while True:
        data = sock.recv(128)
        if not data:
            continue

        raw = data.decode().strip()
        if not raw:
            continue

        print("[TCP] 收到:", raw)

        fn = _cmd.get(raw)
        if fn:
            fn(sock)
        else:
            print("[PUMP] 未知命令:", raw)
        time.sleep(0.02)

if __name__ == "__main__":
    main()
