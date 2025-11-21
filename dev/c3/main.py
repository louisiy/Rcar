import network
import time
import usocket as socket

# ============================
#  用户需要修改的参数（现在是假设值）
# ============================
WIFI_SSID = "TEST_AP"
WIFI_PASSWORD = "testpassword"

SERVER_IP = "192.168.4.1"
SERVER_PORT = 5000

# ============================
#  连接 Wi-Fi（STA）
# ============================
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("[WiFi] 正在连接:", WIFI_SSID)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        for i in range(30):  # 最长等待约 15 秒
            if wlan.isconnected():
                break
            print(".", end="")
            time.sleep(0.5)
        print()

    if wlan.isconnected():
        print("[WiFi] 连接成功:", wlan.ifconfig())
        return wlan
    else:
        print("[WiFi] 连接失败！")
        return None


# ============================
#  TCP 客户端连接
# ============================
def connect_server():
    while True:
        try:
            print("[TCP] 尝试连接服务器:", SERVER_IP, SERVER_PORT)
            sock = socket.socket()
            sock.connect((SERVER_IP, SERVER_PORT))
            print("[TCP] 连接成功！")
            return sock
        except Exception as e:
            print("[TCP] 连接失败:", e)
            time.sleep(2)


# ============================
#  主逻辑（自动重连 + 心跳 + 收发数据）
# ============================
def main():
    wlan = connect_wifi()
    if wlan is None:
        print("[系统] 无 Wi-Fi，退出")
        return
    
    sock = connect_server()

    last_send = time.ticks_ms()

    while True:
        # --- Wi-Fi 自动重连 ---
        if not wlan.isconnected():
            print("[WiFi] 掉线，重新连接...")
            wlan = connect_wifi()
            time.sleep(1)

        # --- TCP 自动重连 ---
        try:
            # 每 2 秒发送一次心跳包
            if time.ticks_ms() - last_send > 2000:
                last_send = time.ticks_ms()
                msg = b"ESP32C3 heartbeat\r\n"
                sock.send(msg)
                print("[TCP] 已发送心跳")

            # 如果服务器发送数据
            sock.settimeout(0.01)
            try:
                data = sock.recv(1024)
                if data:
                    print("[TCP] 收到:", data)
                    # 回显测试
                    sock.send(b"ECHO: " + data)
            except:
                pass  # 没数据继续

        except Exception as e:
            print("[TCP] 连接中断:", e)
            print("[TCP] 正在重连...")
            sock.close()
            sock = connect_server()

        time.sleep(0.05)  # 降低 CPU 占用


# 开机自动运行
main()
