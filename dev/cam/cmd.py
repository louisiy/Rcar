'''
    命令处理
'''


import time
import log

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
        log.info(f"[CMD] 未处理消息 {key}")

#
@reg("TASK:CHUSHIHUA")
def initial(b):
    log.info(f"[BUS] 等待设备连接")
    while not b.ready:
        time.sleep(0.5)
    log.info(f"[BUS] 总线通讯就绪")
    b.s.done()

@reg("CAR:HELLO")
def car_ready(b):
    log.info(f"[UART] 小车连接完毕")

@reg("ARM:HELLO")
def arm_ready(b):
    #单独测试机械臂
    b.ready = True
    log.info(f"[UART] 机械臂连接完毕")

@reg("TCP:OK")
def tcp_ready(b):
    b.ready = True
    log.info(f"[TCP] 移动设备连接完毕")

#
@reg("TASK:WAITGOGOGO")
def waitgogogo(b):
    log.info(f"[MAIN] 等待PS2手柄退出")
    while not b.s.go:
        time.sleep(0.5)
    log.info(f"[MAIN] PS2手柄退出，任务正式开始")
    b.s.done()

@reg("CAR:GOGOGO")
def gogogo(b):
    b.s.go = True

#
@reg("TASK:MOVE")
def car_move(b):
    b.send("CAR","MOVE")
    log.info(f"[CMD] 小车开始移动")

@reg("CAR:MOVEOK")
def car_move_ok(b):
    log.info(f"[CMD] 小车移动完毕")
    b.s.done()

@reg("CAR:MOVEERR")
def car_move_err(b):
    log.info(f"[CMD] 小车远离轨迹，任务提前停止")
    b.s.over = True

#
@reg("TASK:LEFT")
def arm_left(b):
    b.send("ARM","LEFT")
    log.info(f"[CMD] 机械臂左转90°")

@reg("ARM:LEFT_OK")
def arm_left_ok(b):
    log.info(f"[CMD] 机械臂左转完毕")
    b.s.done()

#
@reg("TASK:ATAG")
def atag_pos(b):
    b.s.at = True
    log.info(f"[CMD] ATAG开始对齐")

@reg("ARM:REATAG")
def atag_re_pos(b):
    b.s.at = True
    log.info(f"[CMD] 再次确认ATAG位置")

@reg("ARM:ATAGOK")
def atag_pos_ok(b):
    log.info(f"[CMD] ATAG对齐完毕")
    b.s.done()

#
@reg("TASK:PHASEINTERFACE")
def phase_interface(b):
    b.s.ch = True
    log.info(f"[CMD] 寻找相界面")

@reg("ARM:REPHASE")
def rephase(b):
    b.s.ch = True
    log.info(f"[CMD] 再次寻找相界面")

@reg("ARM:PHASEOK")
def phase_ok(b):
    log.info(f"[CMD] 相界面寻找完毕")
    b.s.done()

# TODO:更新注射泵具体命令信号
#
@reg("TASK:XIYE")
def pump_xiye(b):
    b.send("PUMP","XI")
    log.info(f"[CMD] 注射泵吸液")

@reg("PUMP:XOK")
def pump_paiye(b):
    b.send("PUMP","PAI")
    log.info(f"[CMD] 注射泵排液")

#
# @reg("TASK:XIQU")
# def xiqu(b):
#     b.send("PITE","DOWN")
#     log.info(f"[CMD] 发送命令")

# @reg("PITE:DOK")
# def dok(b):
#     b.send("PITE","UP")
#     log.info(f"[CMD] 发送命令")

# @reg("PITE:UOK")
# def uok(b):
#     b.send("PITE","OK")
#     log.info(f"[CMD] 发送命令")
#     b.s.done()
