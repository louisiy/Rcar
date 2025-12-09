import network
import socket
import time
from machine import Pin, PWM

servo = PWM(Pin(6))
servo.freq(50)

def set_servo_angle(angle):
    min_pulse = 500000     # 0° = 0.5ms
    max_pulse = 2500000    # 180° = 2.5ms
    pulse_width = min_pulse + (max_pulse - min_pulse) * angle / 180
    servo.duty_ns(int(pulse_width))


SERVER_IP = "192.168.1.100"
SERVER_PORT = 8888

def start_tcp_client():
    sock = socket.socket()
    print("正在连接到服务器:", SERVER_IP)
    sock.connect((SERVER_IP, SERVER_PORT))
    print("TCP连接成功！等待指令...")

    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("连接断开")
                break

            cmd = data.decode().strip().lower()
            print("收到指令:", cmd)

            # ===== 处理 up / down 指令 =====
            if cmd == "up":
                set_servo_angle(180)
                print("👉 舵机转到 180°")
                sock.send(b"OK\n")

            elif cmd == "down":
                set_servo_angle(0)
                print("👉 舵机转到 0°")
                sock.send(b"OK\n")

            else:
                print("未知指令:", cmd)

        except Exception as e:
            print("错误:", e)
            break

    sock.close()


# ========== 程序入口 =============
connect_wifi()
start_tcp_client()
