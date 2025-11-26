import socket
import threading

class TCPHANDLER:
    def __init__(self,
                 ip="192.168.66.1",
                 port=8080,
                 required_clients=3   # 固定必须连上 3 个客户端
                ):
        self.ip = ip
        self.port = port
        self.required_clients = required_clients

        self.s = None
        self.running = False
        self.clients = {}
        self.ready_event = threading.Event()

    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.ip, self.port))

        self.s.listen()

        self.running = True
        print(f"[TCP] 正在监听 {self.ip}:{self.port}，等待 {self.required_clients} 个客户端连接...")

        t = threading.Thread(target=self._accept_loop)
        t.daemon = True
        t.start()

    def stop(self):
        print("[TCP] 正在停止 TCP 服务器...")
        self.running = False

        # 关闭所有客户端
        for addr, c in list(self.clients.items()):
            c.close()
        self.clients.clear()

        if self.s:
            self.s.close()
            self.s = None

        print("[TCP] 已停止")

    def wait_all_clients_ready(self):
        print(f"[TCP] 等待 {self.required_clients} 个客户端全部连接...")
        self.ready_event.wait()
        print(f"[TCP] 已有 {len(self.clients)} 个客户端连接，可以开始任务")

    def _accept_loop(self):
        while self.running:
            c, addr = self.s.accept()
            print(f"[TCP服务] 客户端 {addr} 已连接")

            self.clients[addr] = c

            if len(self.clients) >= self.required_clients:
                self.ready_event.set()

            t = threading.Thread(target=self._handle_client, args=(c, addr))
            t.daemon = True
            t.start()

    def _handle_client(self, c, addr):

        c.sendall(b"DOWN\n")
        print(f"[TCP服务] 已向 {addr} 发送命令: DOWN")

        while self.running:
            data = c.recv(1024)
            if not data:
                break

            text = data.decode("utf-8")
            if not text:
                continue

            for line in text.splitlines():
                print(f"[TCP] 来自 {addr}: {line}")

        c.close()
        if addr in self.clients:
            del self.clients[addr]
        print(f"[TCP] 客户端 {addr} 已断开")
