'''
    命令处理v1.0
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

# ------------------------------------ 初始化 ----------------------------------- #
@reg("TASK:CHUSHIHUA")
def initial(b):
    log.info(f"[BUS] 等待设备连接")
    while not b.ready:
        time.sleep(0.5)
    log.info(f"[BUS] 总线通讯就绪")
    time.sleep(5)
    b.s.done()

@reg("TCP:OK")
def tcp_ready(b):
    b.ready = True
    log.info(f"[TCP] 移动设备连接完毕")
    time.sleep(0.5)
    #b.send("ARM","HELLO")

@reg("ARM:HELLO")
def arm_ready(b):
    #b.ready = True
    log.info(f"[UART] 机械臂连接完毕")
    time.sleep(0.5)
    b.send("CAR","HELLO")

@reg("CAR:HELLO")
def car_ready(b):
    b.ready = True
    log.info(f"[UART] 小车连接完毕")

# --------------------------------- 等待PS2手柄退出 -------------------------------- #
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

# ----------------------------------- 小车移动 ----------------------------------- #
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

# ----------------------------------- 机械臂左转 ---------------------------------- #
@reg("TASK:LEFT")
def arm_left(b):
    b.send("ARM","LEFT")
    log.info(f"[CMD] 机械臂左转90°")

@reg("ARM:LEFT_OK")
def arm_left_ok(b):
    log.info(f"[CMD] 机械臂左转完毕")
    b.s.done()

# ---------------------------------- ATAG码对齐 --------------------------------- #
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

# ----------------------------------- 抓取移液枪 ---------------------------------- #
@reg("TASK:PITE_GRAB")
def pite_grab(b):
    b.send("ARM","PIPETTE_GRAB")
    log.info(f"[CMD] 抓取移液枪")

@reg("ARM:PIPETTE_GRAB_OK")
def pite_grab_ok(b):
    log.info(f"[CMD] 移液枪抓取完毕")
    b.s.done()

# ----------------------------------- 移液枪移动 ---------------------------------- #
@reg("TASK:SOL_MV")
def solution_move(b):
    b.send("ARM","SOLUTION_MOVE")
    log.info(f"[CMD] 移液枪对准烧杯")

@reg("ARM:SOLUTION_MOVE_OK")
def solution_move_ok(b):
    log.info(f"[CMD] 移液枪对准完毕")
    b.s.done()

# ------------------------------------ 移液枪操作 ----------------------------------- #
@reg("TASK:PITE")
def xiqu(b):
    b.send("PITE","IDOWN")
    log.info(f"[CMD] 移液枪按下")

@reg("PITE:IDOK")
def dok(b):
    b.send("ARM","SOLUTION_DOWN")
    log.info(f"[CMD] 移液枪放下")

@reg("ARM:SOLUTION_DOWN_OK")
def solution_down_ok(b):
    b.send("PITE","IUP")
    log.info(f"[CMD] 移液枪松开")

@reg("PITE:IUOK")
def uok(b):
    b.send("ARM","SOLUTION_UP")
    log.info(f"[CMD] 移液枪抬起")

@reg("ARM:SOLUTION_UP_OK")
def solution_up_ok(b):
    log.info(f"[CMD] 吸液完毕")
    b.s.done()

# ------------------------------------ 加液 ------------------------------------ #
@reg("TASK:ADD")
def task_add(b):
    b.send("ARM","ADD_MOVEDOWN")
    log.info(f"[CMD] 加液开始")

@reg("ARM:ADD_MOVEDOWN_OK")
def add_dok(b):
    b.send("PITE","FDOWN")
    log.info(f"[CMD] 移液枪按下")

@reg("PITE:FDOK")
def add_up(b):
    b.send("ARM","ADD_UP")
    log.info(f"[CMD] 移液枪抬起")

@reg("ARM:ADD_UP_OK")
def add_up_ok(b):
    b.send("PITE","FUP")
    log.info(f"[CMD] 移液枪松开")

@reg("PITE:FUOK")
def fuok(b):
    log.info(f"[CMD] 加液完成")
    b.s.done()

# ----------------------------------- 放回移液枪 ---------------------------------- #
@reg("TASK:FANGHUI")
def fanghui(b):
    b.send("ARM","PIPETTE_DROP")
    log.info(f"[CMD] 放回移液枪")

@reg("ARM:PIPETTE_DROP_OK")
def fanghui_ok(b):
    log.info(f"[CMD] 放回完毕")
    b.s.done()

# ----------------------------------- 夹起容器 ----------------------------------- #
@reg("TASK:JIAQI")
def jiaqi(b):
    b.send("ARM","CONTAINER_GRAB")
    log.info(f"[CMD] 夹起容器")

@reg("ARM:CONTAINER_GRAB_OK")
def jiaqi_ok(b):
    log.info(f"[CMD] 夹起完毕")
    b.s.done()

# ----------------------------------- 小车移动 ----------------------------------- #

# ----------------------------------- 机械臂左转 ---------------------------------- #

# ----------------------------------- ATAG ----------------------------------- #

# ------------------------------------ 放容器 ----------------------------------- #
@reg("TASK:FANGXIA")
def fangxia(b):
    b.send("ARM","EXTRACTION_DROP")
    log.info(f"[CMD] 容器放下")


@reg("ARM:EXTRACTION_DROP_OK")
def fangxia_ok(b):
    log.info(f"[CMD] 放下完毕")
    b.s.done()

# ----------------------------------- 寻找相界面 ---------------------------------- #
@reg("TASK:COLOR")
def color_move(b):
    b.send("ARM","INTERFACE_MOVE")
    log.info(f"[CMD] 移动到相界面附近")

@reg("ARM:INTERFACE_MOVE_OK")
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

# ----------------------------------- 夹取针头 ----------------------------------- #
@reg("TASK:ZHUAZHEN")
def zhuazhen(b):
    b.send("ARM","NEEDLE_GRAB")
    log.info(f"[CMD] 抓取针头")

@reg("ARM:NEEDLE_GRAB_OK")
def zhuazhen_ok(b):
    log.info(f"[CMD] 抓取针头完毕")
    b.s.done()

# ----------------------------------- 移动针头 ----------------------------------- #
@reg("TASK:YIZHEN")
def yizhen(b):
    b.send("ARM","PUMP_MOVE")
    log.info(f"[CMD] 移动针头")

@reg("ARM:PUMP_MOVE_OK")
def yizhen_ok(b):
    log.info(f"[CMD] 移动针头完毕")
    b.s.done()

# ------------------------------------ 注射泵 ----------------------------------- #
@reg("TASK:PUMP")
def pump(b):
    b.send("PUMP","XI")
    log.info(f"[CMD] 注射泵吸液")

@reg("PUMP:XOK")
def pump_xok(b):
    log.info(f"[CMD] 吸液完毕")
    b.s.done()

@reg("TASK:PUMPOUT")
def out(b):
     b.send("PUMP","PAI")
     log.info(f"[CMD] 注射泵排液")

@reg("PUMP:POK")
def pok(b):
    log.info(f"[CMD] 排液完毕")
    b.s.done()

# ------------------------------------ 放回针 ----------------------------------- #
@reg("TASK:FANGZHEN")
def fangzhen(b):
    b.send("ARM","PUMP_UP")
    log.info(f"[CMD] 升起针头")

@reg("ARM:PUMP_UP_OK")
def taizhen_ok(b):
    #b.s.done()
    b.send("ARM","DROPNEEDLE")
    log.info(f"[CMD] 放回针头")

@reg("ARM:DROPNEEDLE_OK")
def fanzheng_ok(b):
    log.info(f"[CMD] 放针完毕")
    b.s.done()


# ----------------------------------- 任务完成 ----------------------------------- #
@reg("TASK:OVER")
def task_over(b):
    b.send("CAR","OVER")
    log.info(f"[MAIN] 归还PS2手柄控制")

@reg("CAR:BYE")
def car_byr(b):
    b.s.done()

# ----------------------------------- 小车离线 ----------------------------------- #
@reg("CAR:SHUTDOWN")
def car_shutdown(b):
    log.info(f"[CMD] 小车离线，异常，任务提前停止")
    b.s.over = True