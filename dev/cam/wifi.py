from maix.network import wifi
from maix import err

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
        print(f"[WiFiHandler] Starting AP mode with SSID: {self.ssid}")
        err = self.wifi.start_ap(self.ssid, self.password, self.mode, self.channel, self.ip, self.netmask, self.hidden)
        if err == err.ERR_NONE:
            print(f"[WiFiHandler] Wi-Fi AP started successfully with SSID: {self.ssid}")
        else:
            print(f"[WiFiHandler] Failed to start Wi-Fi AP: {err}")
    def stop(self):
        print(f"[WiFiHandler] Stopping AP mode...")
        err = self.wifi.stop_ap()
        if err == err.ERR_NONE:
            print("[WiFiHandler] Wi-Fi AP stopped successfully")
        else:
            print(f"[WiFiHandler] Failed to stop Wi-Fi AP: {err}")