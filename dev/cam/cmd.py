'''
    命令处理
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
        fn(b)
    else:
        print(f"[CMD] 未处理消息 {key}")

#
@reg("TASK:CHUSHIHUA")
def initial(b):
    print(f"[BUS] 等待设备连接")
    while not b.ready:
        time.sleep(0.5)
    print(f"[BUS] 总线通讯就绪")
    b.s.done()

@reg("CAR:HELLO")
def car_ready(b):
    print(f"[UART] 小车连接完毕")

@reg("ARM:HELLO")
def arm_ready(b):
    print(f"[UART] 机械臂连接完毕")

@reg("TCP:OK")
def tcp_ready(b):
    b.ready = True
    print(f"[TCP] 移动设备连接完毕")

#
@reg("TASK:WAITGOGOGO")
def waitgogogo(b):
    print(f"[MAIN] 等待PS2手柄退出")
    while not b.s.go:
        time.sleep(0.5)
    print(f"[MAIN] PS2手柄退出，任务正式开始")
    b.s.done()

@reg("CAR:GOGOGO")
def gogogo(b):
    b.s.go = True

#
@reg("TASK:MOVE")
def car_move(b):
    b.send("CAR","MOVE")
    print(f"[CMD] 小车开始移动")

@reg("CAR:MOVEOK")
def car_move_ok(b):
    print(f"[CMD] 小车移动完毕")
    b.s.done()

@reg("CAR:MOVEERR")
def car_move_err(b):
    print(f"[CMD] 小车远离轨迹，任务提前停止")
    b.s.over = True

#
@reg("TASK:LEFT")
def arm_left(b):
    b.send("ARM","LEFT")
    print(f"[CMD] 机械臂左转90°")

@reg("ARM:LEFT_OK")
def arm_left_ok(b):
    print(f"[CMD] 机械臂左转完毕")
    b.s.done()

#
@reg("TASK:ATAG")
def atag_pos(b):
    b.s.at = True
    print(f"[CMD] ATAG开始对齐")

@reg("ARM:REATAG")
def atag_re_pos(b):
    b.s.at = True
    print(f"[CMD] 再次确认ATAG位置")

@reg("ARM:ATAGOK")
def atag_pos_ok(b):
    b.s.done()
    print(f"[CMD] ATAG对齐完毕")

#
# @reg("XIQU")
# def xiqu(b):
#     print(f"[CMD] 开始吸取")

#
# @reg("TASK:XIQU")
# def xiqu(b):
#     b.send("PITE","DOWN")
#     print(f"[CMD] 发送命令")

# @reg("PITE:DOK")
# def dok(b):
#     b.send("PITE","UP")
#     print(f"[CMD] 发送命令")

# @reg("PITE:UOK")
# def uok(b):
#     b.send("PITE","OK")
#     print(f"[CMD] 发送命令")
#     b.s.done()
