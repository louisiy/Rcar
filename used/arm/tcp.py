import threading

class TCPHANDLER:
    def __init__(
                 self,
                 is_server=True,
                 ip="192.168.5.1",
                 port=5200,
                 timeout=0
                ):
        self.is_server = is_server
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.socket = None
        self.err = None
        self.cb = None

    def start(self):
        self.err, self.socket = TCPCreate(self.is_server, self.ip, self.port)
        TCPStart(self.socket, self.timeout)

    def read(self):
        while True:
            self.err,data = TCPRead(self.socket,data)

            if not data:
                continue
            raw = data.decode().strip()

            if not raw:
                continue
            print("[TCP] 收到:",raw)

            if self.cb:
                self.cb(msg)


    def send(self,data):
        TCPWrite(self.socket, data)

    def listen(self):
        sth = threading.Thread(target=self.read,args=())
        sth.daemon = True
        sth.start()

    def stop(self):
        TCPDestroy(self.socket)
