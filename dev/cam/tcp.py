'''
    管理TCP服务
'''


import socket
import threading

class TCPHANDLER:
    def __init__(self, ip="192.168.66.1", port=8080):
        self.ip = ip
        self.port = port

        self.sock = None
        self.run = False

        self.clis = {}             # addr -> sock
        self.ids = {}              # id -> addr

        self.cb = None             # 回调：cb(id, msg)

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.ip, self.port))
        self.sock.listen()
        self.run = True
        print(f"[TCP] 监听 {self.ip}:{self.port}")

        t = threading.Thread(target=self._accept, daemon=True)
        t.start()

    def stop(self):
        self.run = False
        if self.sock:
            self.sock.close()

        for addr, cli in self.clis.items():
            cli.close()

        self.clis.clear()
        self.ids.clear()
        print("[TCP] 停止")

    def send(self, id_, msg: str):
        addr = self.ids.get(id_)
        if not addr:
            print(f"[TCP] {id_} 不存在")
            return 1
        cli = self.clis.get(addr)
        if cli:
            cli.sendall(msg.encode())
        return 0

    def _accept(self):
        while self.run:
            cli, addr = self.sock.accept()
            self.clis[addr] = cli
            print(f"[TCP] 连接 {addr}")

            t = threading.Thread(target=self._recv, args=(cli, addr), daemon=True)
            t.start()

    def _recv(self, cli: socket.socket, addr):
        while self.run:
            data = cli.recv(1024)
            if not data:
                break

            raw = data.decode().strip()
            if not raw:
                continue

            if ":" not in raw:
                print(f"[TCP] 未知信息 {raw}")
                continue

            id_, msg = raw.split(":", 1)

            if msg == "HELLO":
                self.ids[id_] = addr
                print(f"[TCP] 注册 id={id_}")
                if self.cb and len(self.ids) == 1:
                    self.cb("TCP", "OK")
            else:
                if self.cb:
                    self.cb(id_, msg)

        if addr in self.clis:
            del self.clis[addr]

        dead = None
        for k, v in self.ids.items():
            if v == addr:
                dead = k
                break
        if dead:
            del self.ids[dead]
            print(f"[TCP] id {dead} 注销")

        cli.close()
        print(f"[TCP] 断开连接 {addr}")
