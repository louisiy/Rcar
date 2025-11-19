import threading

class TCPHANDLER:
    def __init__(self,
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
        self.data = ""

    def start(self):
        self.err, self.socket = TCPCreate(self.is_server, self.ip, self.port)
        TCPStart(self.socket, self.timeout)

    def read(self):
        while True:
            self.err,data = TCPRead(self.socket,data)
            data = data.decode('utf-8', errors='ignore')
            if data !="":
                self.data = data

    def send(self,data):
        TCPWrite(self.socket, data)

    def listen(self):
        sth = threading.Thread(target=self.read,args=())
        sth.daemon = True
        sth.start()

    def stop(self):
        TCPDestroy(self.socket)

