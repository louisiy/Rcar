'''
    日志管理
'''


import logging, time

_BUF_MAX = 500
_buf = []          # [(seq, line)]
_seq = 0
_t0 = time.monotonic()
_inited = False

class _UptimeFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        s = int(time.monotonic() - _t0)
        h = s // 3600
        m = (s % 3600) // 60
        sec = s % 60
        return f"{h:02d}:{m:02d}:{sec:02d}"


class _BufferHandler(logging.Handler):
    def emit(self, record):
        global _seq
        line = self.format(record)
        _seq += 1
        _buf.append((_seq, line))
        if len(_buf) > _BUF_MAX:
            del _buf[: len(_buf) - _BUF_MAX]

def setup(level=logging.INFO):
    global _inited
    if _inited:
        return
    _inited = True
    fmt = _UptimeFormatter("%(asctime)s %(message)s")

    root = logging.getLogger()
    root.setLevel(level)

    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    root.addHandler(sh)

    bh = _BufferHandler()
    bh.setFormatter(fmt)
    root.addHandler(bh)

def info(msg: str):
    logging.info(msg)

def read_since(since: int):
    if not _buf:
        return [], since
    latest = _buf[-1][0]
    if since >= latest:
        return [], latest
    out = [(seq, line) for (seq, line) in _buf if seq > since]
    return out, latest
