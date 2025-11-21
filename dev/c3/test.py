import network
import time

# 你要让它广播的热点名和密码
AP_SSID = "ESP32C3_AP"
AP_PASSWORD = "12345678"  # 至少 8 位

ap = network.WLAN(network.AP_IF)   # 选择 AP 接口
ap.active(True)                    # 打开 AP

# 配置热点：名称、密码、加密方式
ap.config(
    essid=AP_SSID,
    password=AP_PASSWORD,
    authmode=network.AUTH_WPA_WPA2_PSK  # 加密方式：WPA/WPA2
    # 可以按需加上 channel=6 等
)

# 等待 AP 生效
time.sleep(1)

print("AP 已开启")
print("SSID:", AP_SSID)
print("密码:", AP_PASSWORD)
print("AP IP 地址:", ap.ifconfig()[0])   # 一般是 192.168.4.1

while True:
    # 打印一下当前连接到这个 AP 的设备数量
    print("当前是否有站点连接? ->", ap.isconnected())
    time.sleep(5)
