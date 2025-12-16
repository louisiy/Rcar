'''
    通信总线
'''


from maix import pinmap
import uart
import tcp

class BUS:
    def __init__(self):
        self.u0 = uart.UARTHANDLER("/dev/ttyS0")
        self.u2 = uart.UARTHANDLER("/dev/ttyS2")
        self.tp = tcp.TCPHANDLER()
        self.cb = None

        self.id_ = ""
        self.msg = ""
        self.buf = False

        self.s = None

        self.ready = False

    def start(self):
        self.u0.cb = self._on_msg
        self.u2.cb = self._on_msg
        self.tp.cb = self._on_msg

        self.u0.start()
        self.u2.start()
        self.tp.start()

    def stop(self):
        self.u0.stop()
        self.u2.stop()
        self.tp.stop()

    def send(self, id_, msg: str):
        if id_ == "ARM":
            self.u0.send(msg)
        elif id_ == "CAR":
            self.u2.send(msg)
        else:
            self.tp.send(id_, msg)

    # def recv(self):
    #     if not self.buf:
    #         return None, None
    #     id_ = self.id_
    #     msg = self.msg
    #     self.buf = False
    #     return id_, msg

    def _on_msg(self, id_, msg):
        self.id_ = id_
        self.msg = msg
        self.buf = True

        if self.cb:
            self.cb(id_, msg)

        self.buf = False
