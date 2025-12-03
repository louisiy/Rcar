'''
    处理所有的字符串信号
'''


import time

_cmd = {}

def reg(name: str):
    def deco(fn):
        _cmd[name] = fn
        return fn
    return deco

def dispatch(b, id_, msg):
    key = f"{id_}:{msg}"
    fn = _cmd.get(key)
    if fn:
        fn(b, id_, msg)
    else:
        print(f"[CMD] 未处理消息 {key}")

@reg("TCP:OK")
def ready(b,id_,msg):
    b.ready = True
    print(f"[TCP] 移动设备连接完毕")

@reg("TASK:CHUSHIHUA")
def initial(b,id_,msg):
    while not b.ready:
        print(f"[BUS] 等待设备连接")
        time.sleep(0.5)
    print(f"[BUS] 总线通讯就绪")
    b.s.done()

@reg("TASK:DENGDAI")
def waitps2(b,id_,msg):
    while not b.s.go:
        print(f"[MAIN] 等待PS2手柄退出")
        time.sleep(0.5)
    print(f"[MAIN] PS2手柄退出，任务正式开始")
    b.s.done()

@reg("TASK:XIQU")
def xiqu(b,id_,msg):
    b.send("PITE","DOWN")
    print(f"[CMD] 发送命令")

@reg("PITE:DOK")
def dok(b,id_,msg):
    b.send("PITE","UP")
    print(f"[CMD] 发送命令")

@reg("PITE:UOK")
def uok(b,id_,msg):
    b.send("PITE","OK")
    print(f"[CMD] 发送命令")
    b.s.done()
