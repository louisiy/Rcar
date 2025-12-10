'''
    移液枪电机客户端 ID:PITE
'''


import network
import time
import socket
from machine import Pin, PWM

# SERVO
servo = PWM(Pin(4))
servo.freq(50)

def set_angle(angle):
    min_p = 500000
    max_p = 2500000
    pulse = min_p + (max_p - min_p) * angle / 180
    servo.duty_ns(int(pulse))

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

@reg("UP")
def up(sock):
    print("[PITE] UP")
    # FIXME: 确认这是正确的角度
    set_angle(0)
    time.sleep(2)
    sock.send(b"PITE:UOK\n")

@reg("DOWN")
def down(sock):
    print("[PITE] DOWN")
    # FIXME: 确认这是正确的角度
    set_angle(120)
    time.sleep(2)
    sock.send(b"PITE:DOK\n")

def main():
    wlan = wifi_connect()
    sock = server_connect()

    sock.send(b"PITE:HELLO\n")
    print("[TCP] 发送: PITE:HELLO")

    # FIXME: 修改初始化角度到正确的角度
    set_angle(0)

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
            print("[PITE] 未知命令:", raw)
        time.sleep(0.02)

if __name__ == "__main__":
    main()
