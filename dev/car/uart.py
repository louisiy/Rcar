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
        self.data = ""
        self.ut.write('uart2 ok!\r\n')
        self.exit = False

    def read(self):
        while True:
            if self.exit:
                break
            if self.ut.any() > 0:
                data = self.ut.read()
                data = data.decode("utf-8")
                if data != "":
                    self.data = data

    def send(self,data):
        self.ut.write(data)

    def listen(self):
        th = _thread.start_new_thread(self.read,())

    def get(self):
        tmp = ""
        if self.data:
            tmp = self.data
            self.data = ""
        return tmp

    def stop(self):
        self.exit = True

    def close(self):
        self.ut.deinit()

if __name__ == "__main__":
    uart = UART2()
    uart.send("hello world\n")
    uart.listen()
    while True:
        print("oh")
        msg = uart.get()
        print(msg)
        if msg:
            print(int(time.time()*1000))
            print("Received:", msg)
            uart.send(msg)
        if msg == 'q':
            break
        time.sleep(0.1)
    uart.stop()
    uart.close()