'''
    uart端口类
'''
import setting
from machine import UART
import _thread

class UART2:
    def __init__(self,port=2,baud=115200,bits=8,parity=None,stop=1):
        self.ut = UART(port,baud, bits, parity, stop)
        self.data = ""
        self.ut.write('uart2 ok!\r\n')

    def read(self):
        while True:
            if self.ut.any() > 0:
                data = self.ut.read()
                data = data.decode("uft-8",errors="ignore")
                if data != "":
                    self.data = data

    def send(self,data):
        self.ut.write(data)

    def listen(self):
        uth = _thread.start_new_thread(self.read)

    def stop(self):
        self.ut.deinit()

if __name__ == "__main__":
    import time
    uart = UART2()
    uart.send("hello world\n")
    while True:
        msg = uart.data
        if msg:
            print(int(time.time()*1000))
            print("Received:", msg)
            uart.send(msg)
        if msg == 'q':
            break
        time.sleep(0.1)
    uart.send("Bye world\n")
    uart.close()