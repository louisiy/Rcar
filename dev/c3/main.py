import network
import time
import socket
from machine import Pin, PWM

WIFI_SSID = "CAMAP"
WIFI_PASSWORD = "12345678"

SERVER_IP = "192.168.66.1"
SERVER_PORT = 8080

servo = PWM(Pin(6))
servo.freq(50)

def set_angle(angle):
    min_p = 500000
    max_p = 2500000
    pulse = min_p + (max_p - min_p) * angle / 180
    servo.duty_ns(int(pulse))

_cmd = {}

def reg(name):
    def deco(fn):
        _cmd[name] = fn
        return fn
    return deco

@reg("UP")
def cmd_up(sock):
    print("[CMD] UP")
    set_angle(180)
    sock.send(b"PITE:OK\n")

@reg("DOWN")
def cmd_down(sock):
    print("[CMD] DOWN")
    set_angle(0)
    sock.send(b"PITE:OK\n")

def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    print("[WiFi] 连接中...")

    while not wlan.isconnected():
        time.sleep(0.5)

    print("[WiFi] 连接成功:", wlan.ifconfig())
    return wlan

def server_connect():
    sock = socket.socket()
    print("[TCP] 连接服务器中...")
    sock.connect((SERVER_IP, SERVER_PORT))
    print("[TCP] 连接成功")
    return sock

def main():
    wifi_connect()
    sock = server_connect()

    sock.send(b"PITE:HELLO\n")
    print("[TCP] 发送: PITE:HELLO")

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
