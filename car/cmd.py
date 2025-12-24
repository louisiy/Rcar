'''
    命令处理
'''


_cmd = {}

def reg(name: str):
    def deco(fn):
        _cmd[name] = fn
        return fn
    return deco

def dispatch(uart,mv, rm,raw):
    fn = _cmd.get(raw)
    if fn:
        fn(uart,mv,rm)
    else:
        print(f"[CAR] 未知命令: {raw}")

@reg("MOVE")
def car_move(uart,mv,rm):
    print(f"[CAR] 前进命令")
    i = mv.move_time_traj(125,5)
    if i:
        uart.send("CAR:MOVEERR")
    else:
        uart.send("CAR:MOVEOK")

@reg("OVER")
def over(uart,mv,rm):
    print("[RM] PS2手柄重新获得控制权")
    rm.initial()
    uart.send("CAR:BYE")

@reg("HELLO")
def hello(uart,mv,rm):
    print("[RM] 主控确认连接")
    uart.send("CAR:HELLO")