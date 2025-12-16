'''
    主程序入口
'''

from maix import app, pinmap
import video
import log
import web
import atag
import color
import wifi
import bus
import cmd
import time
import state

log.setup()

pinmap.set_pin_function("A29", "UART2_RX")
pinmap.set_pin_function("A28", "UART2_TX")

at = atag.ATAGHANDLER()
ch = color.COLORHANDLER()

ap = wifi.WIFIHANDLER()
ap.start()

b = bus.BUS()
b.cb = lambda id_, msg: cmd.dispatch(b, id_, msg)
b.start()

s = state.STATE("./task.json")
s.cb = lambda id_, msg: cmd.dispatch(b, id_, msg)
b.s = s

v = video.VIDEO(s,b,at,ch)
v.start()

web.start(port = 5000)

while not app.need_exit():
    s.update()
    if getattr(s, "over", False):
        log.info("[MAIN] 所有任务完成，准备退出")
        break

b.stop()
ap.stop()
v.stop()
