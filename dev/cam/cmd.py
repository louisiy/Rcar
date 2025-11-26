_cmd = {}   # "ID:MSG" -> 函数

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


# ====== 这里开始加 PITE 任务逻辑 ======

# 0: 未开始
# 1: 已发送 DOWN，等待第一次 OK
# 2: 已发送 UP，等待第二次 OK
# 3: 任务完成
_pite_step = 0

# ===== 下面写具体命令处理 =====
@reg("PITE:HELLO")
def hello(b, id_, msg):
    global _pite_step
    _pite_step = 1
    print("[CMD] 启动 PITE 任务：先发送 DOWN")
    b.send("PITE", "DOWN")


@reg("PITE:OK")
def on_pite_ok(b, id_, msg):
    global _pite_step

    if _pite_step == 1:
        # 收到的是 DOWN 的 OK
        print("[CMD] PITE 完成 DOWN，继续发送 UP")
        b.send("PITE", "UP")
        _pite_step = 2

    elif _pite_step == 2:
        # 收到的是 UP 的 OK
        print("[CMD] PITE 完成 UP，任务结束")
        _pite_step = 3

    else:
        # 不在任务流程里但收到了 OK
        print("[CMD] 收到 PITE:OK，但当前没有在执行任务")


@reg("PUMP:OK")
def on_pump_ok(b, id_, msg):
    print("[CMD] PUMP 完成动作")


@reg("PUMP:ERR")
def on_pump_err(b, id_, msg):
    print("[CMD] PUMP 报错")
