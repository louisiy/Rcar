'''
    命令处理
'''


_cmd = {}

def reg(name: str):
    def deco(fn):
        _cmd[name] = fn
        return fn
    return deco

def dispatch(uart,mv,raw):
    fn = _cmd.get(raw)
    if fn:
        fn(uart,mv)
    else:
        print(f"[CAR] 未知命令: {raw}")

@reg("MOVE")
def car_move(uart,mv):
    i = mv.move_time_traj(150,4)
    if i:
        b.send("CAR:MOVEERR")
    else:
        b.send("CAR:MOVEOK")

