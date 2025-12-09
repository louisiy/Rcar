_cmd = {}

def reg(name: str):
    def deco(fn):
        _cmd[name] = fn
        return fn
    return deco

def dispatch(uart,raw):
    fn = _cmd.get(raw)
    if fn:
        fn(uart)
    else:
        print(f"[ARM] 未知命令: {raw}")