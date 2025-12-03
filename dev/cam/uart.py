'''
    管理UART接口
'''


from maix import uart
import threading

class UARTHANDLER:
    def __init__(self, dev, baud=115200):
        self.ut = uart.UART(dev,baud)
        self.run = False
        self.cb = None

    def start(self):
        self.run = True
        t = threading.Thread(target=self._read)
        t.start()

    def stop(self):
        self.run = False
        self.ut.close()

    def send(self,msg:str):
        self.ut.write_str(msg)

    def _read(self):
        while self.run:
            data = self.ut.read()
            if not data:
                continue

            raw = data.decode().strip()

            if not raw:
                continue

            if ":" not in raw:
                print(f"[UART] 未知信息 {raw}")
                continue

            id_, msg = raw.split(":", 1)

            if self.cb:
                self.cb(id_, msg)