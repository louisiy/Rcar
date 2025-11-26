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

def set_servo_angle(angle):
    min_pulse = 500000     # 0° = 0.5 ms
    max_pulse = 2500000    # 180° = 2.5 ms
    pulse_width = min_pulse + (max_pulse - min_pulse) * angle / 180
    servo.duty_ns(int(pulse_width))

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    print("[WiFi] 连接中...")

    while not wlan.isconnected():
        time.sleep(0.5)

    print("[WiFi] 连接成功:", wlan.ifconfig())
    return wlan

def connect_server():
    sock = socket.socket()
    print("[TCP] 连接服务器:", SERVER_IP, SERVER_PORT)
    sock.connect((SERVER_IP, SERVER_PORT))
    print("[TCP] 连接成功！")
    return sock

def main():
    wlan = connect_wifi()
    sock = connect_server()

    while True:
        data = sock.recv(1024)
        if not data:
            continue
        cmd = data.decode()
        print("收到指令:", cmd)

        if cmd == "up":
            set_servo_angle(180)
            print("舵机转到 180°")
            sock.send(b"OK\n")

        elif cmd == "down":
            set_servo_angle(0)
            print("舵机转到 0°")
            sock.send(b"OK\n")

        else:
            print("未知指令:", cmd)

        time.sleep(0.05)

# 开机自动运行
main()
