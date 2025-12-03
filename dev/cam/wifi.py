'''
    管理WiFi热点
'''


from maix.network import wifi

class WIFIHANDLER:
    def __init__(self,
                 ssid="CAMAP",
                 password="12345678",
                 mode="g",
                 channel=1,
                 ip="192.168.66.1",
                 netmask="255.255.255.0",
                 hidden=False
                ):
        self.ssid = ssid
        self.password = password
        self.mode = mode
        self.channel = channel
        self.ip = ip
        self.netmask = netmask
        self.hidden = hidden
        self.wifi = wifi.Wifi()
    def start(self):
        print(f"[WiFi] 正在以 AP 模式启动，无线名称(SSID): {self.ssid}")
        ret = self.wifi.start_ap(self.ssid,
                                 self.password,
                                 self.mode,
                                 self.channel,
                                 self.ip,
                                 self.netmask,
                                 self.hidden)
        if ret == 0:
            print(f"[WiFi] AP 启动成功，SSID: {self.ssid}，IP: {self.ip}")
        else:
            print(f"[WiFi] 启动 AP 失败，错误码: {ret}")

    def stop(self):
        print("[WiFi] 正在关闭 AP 模式...")
        ret = self.wifi.stop_ap()
        if ret == 0:
            print("[WiFi] AP 已成功关闭")
        else:
            print(f"[WiFi] 关闭 AP 失败，错误码: {ret}")
