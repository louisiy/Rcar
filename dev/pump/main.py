'''
    注射泵客户端 ID:PUMP
'''


import network
import time
import socket
from machine import Pin, PWM

# UART
# TODO:UART初始化

# PUMP
# TODO:泵的功能代码

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

# @reg("UP")
# def up(sock):
#     print("[CMD] UP")
#     set_angle(0)
#     time.sleep(2)
#     sock.send(b"PITE:UOK\n")

# TODO: 信号调度

def main():
    wlan = wifi_connect()
    sock = server_connect()

    sock.send(b"PUMP:HELLO\n")
    print("[TCP] 发送: PUMP:HELLO")
    # TODO:初始化泵代码

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
