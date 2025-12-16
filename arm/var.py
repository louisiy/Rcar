_cmd = {}

def reg(name):
    def deco(fn):
        _cmd[name] = fn
        return fn
    return deco

## 示例
@reg("XIQU")
def xiqu(socket):
  # 具体的吸取代码
  TCPWrite(socket,"ARM:XQOK")

