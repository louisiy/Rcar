'''
    uart端口类
'''
import setting
from machine import UART
import time

class UART2:
    def __init__(self,port=2,baud=115200,bits=8,parity=None,stop=1,errors="strict"):
        self.ut = UART(port,baud, bits, parity, stop)
        self.size = BUFFER_SIZE
        self.max = MAX_FRAME
        self.buf = bytearray(self.size)
        self.tmp = bytearray()
        self.start = FRAME_START
        self.end = FRAME_END
        self.state = 0
        self.r = 0
        self.w = 0
        self.err = errors
        self.ut.write(b'uart2 ok!\r\n')
        # self.ut.write('uart2 ok!\r\n')
    def _rb_write(self,data):
        for b in data:
            n = (self.w+1)%self.size
            if n == self.r:
                self.r=self.w
                self._set_state(0)
                print("Buffer overflow! Resyncing...\n")
                break
            self.buf[self.w]=b
            self.w=n
    def _rb_read(self):
        if self.r == self.w:
            return None
        b = self.buf[self.r]
        self.r = (self.r+1)%self.size
        return b

    def _set_state(self,flag):
        self.state = 1 if flag else 0
        self.tmp = bytearray()

    def poll(self):
        data = self.ut.read()
        if data:
            self._rb_write(data)
        # out = []
        while True:
            if not self.state:
                b = self._rb_read()
                if b is None:
                    break
                if b == self.start:
                    self._set_state(1)
            else:
                b = self._rb_read()
                if b is None:
                    break
                if b == self.end:
                    try:
                        s = self.tmp.decode("utf-8", errors=self.err)
                        # out.append(s)
                        print("Read frame completely!\n")
                        self._set_state(0)
                        return s
                    except:
                        print("Decoding error! Dropping frame...\n")
                        self._set_state(0)
                else:
                    self.tmp.append(b)
                    if len(self.tmp) > self.max:
                        print("Frame too large! Dropping frame...\n")
                        self._set_state(0)
        # return out
        return None

    def send(self,data):
        if isinstance(data,str):
            data = data.encode()
        self.ut.write(data)


    def close(self):
        self.ut.deinit()

if __name__ == "__main__":
    uart = UART2()
    uart.send("hello world\n")
    while True:
        msg = uart.poll()
        if msg:
            print(int(time.time()*1000))
            print("Received:", msg)
            uart.send(msg)
        if msg == 'q':
            break
        time.sleep(0.1)
    uart.send("Bye world\n")
    uart.close()