'''
    uart端口类
'''
import setting as s
from machine import UART
import time
import _thread

class UART2:
    def __init__(self,port=2,baud=115200,bits=8,parity=None,stop=1):
        self.ut = UART(port,baud, bits, parity, stop)
        # self.data = ""
        self.run = False

        self.cb = None

    def start(self):
        self.run = True
        th = _thread.start_new_thread(self._read,())

    def stop(self):
        self.run = False

    def close(self):
        self.ut.deinit()

    def send(self,data):
        self.ut.write(data)

    def _read(self):
        while self.run:
            data = self.ut.read()

            if not data:
                continue

            raw = data.decode().strip()

            if not raw:
                continue

            print(f"[UART] 收到: {raw}")

            if self.cb:
                self.cb(raw)

    # def get(self):
    #     tmp = ""
    #     if self.data:
    #         tmp = self.data
    #         self.data = ""
    #     return tmp

if __name__ == "__main__":
    uart = UART2()
    uart.send("hello world\n")
    uart.start()
    # while True:
    #     print("oh")
    #     msg = uart.get()
    #     print(msg)
    #     if msg:
    #         print(int(time.time()*1000))
    #         print("Received:", msg)
    #         uart.send(msg)
    #     if msg == 'q':
    #         break
    #     time.sleep(0.1)
    uart.stop()
    uart.close()