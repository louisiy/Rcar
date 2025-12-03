'''
    主程序入口
'''


from maix import app,camera,display,pinmap
import atag
import yolo
import color
import wifi
import bus
import cmd
import time
import state

cam = camera.Camera(640,480)
dis = display.Display()

pinmap.set_pin_function("A29", "UART2_RX")
pinmap.set_pin_function("A28", "UART2_TX")

#at = atag.ATAGHANDLER()
#dt = yolo.YOLOHANDLER()
#ch = color.COLORHANDLER()

ap = wifi.WIFIHANDLER()
ap.start()

b = bus.BUS()
b.cb = lambda id_, msg: cmd.dispatch(b, id_, msg)
b.start()

s = state.STATE("./task.json")
s.cb = lambda id_, msg: cmd.dispatch(b, id_, msg)
b.s = s

while not app.need_exit():
    img = cam.read()

    #img = at.search(img)
    #img = ch.search(img)
    #img = dt.search(img)
    s.update()
    dis.show(img)
    if getattr(s, "over", False):
        print("[MAIN] 所有任务完成，准备退出")
        break
b.stop()
ap.stop()
