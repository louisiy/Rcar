import socket
import threading

class TCPHANDLER:
    def __init__(self,
                 ip="192.168.66.1",
                 port=8080,
                 max_clients=5
                ):
        self.ip = ip
        self.port = port
        self.max = max_clients
        self.s = None

    def start(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.bind((self.ip,self.port))
        self.s.listen(self.m)
        print(f"[TCPHandler] Listening on {self.ip}:{self.port}...")
        accept_thread = threading.Thread(target=self._wait_accept)
        accept_thread.daemon = True
        accept_thread.start()

    def _wait_accept(self):
        while True:
            c,addr = self.s.accept()
            print(f"[TCPHandler] Client {client_addr} connected.")
            cthread = threading.Thread(target=self._handle_client, args=(client_socket, client_addr))
            cthread.daemon = True
            cthread.start()

    def stop(self):
        print("[TCPHandler] Stopping server...")
        if self.s:
            self.s.close()
