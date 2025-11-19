from maix import uart
import threading

class UARTHANDLER:
    def __init__(self, device, baudrate=115200):
        self.ut = uart.UART(device,baudrate)
        self.data = ""

    def read(self):
        while True:
            data = self.ut.read()
            data = data.decode("utf-8",errors="ignore")
            if data != "":
                self.data = data

    def send(self,data):
        self.ut.write_str(data)

    def listen(self):
        uth = threading.Thread(target=self.read)
        uth.daemon = True
        uth.start()

    def stop(self):
        self.ut.close()