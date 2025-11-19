from maix import app,camera,display,pinmap
import uart
import atag
import yolo
import wifi

cam = camera.Camera(640,480)
dis = display.Display()

pinmap.set_pin_function("A29", "UART2_RX")
pinmap.set_pin_function("A28", "UART2_TX")

u0 = uart.UARTHANDLER("/dev/ttyS0")
u2 = uart.UARTHANDLER("/dev/ttyS2")
u0.listen()
u2.listen()

at = atag.ATAGHANDLER()

#dt = yolo.YOLOHANDLER()

ap = wifi.WIFIHANDLER()

ap.start()
while not app.need_exit():
    img = cam.read()

    img = at.search(img)
    #img = dt.search(img)

    dis.show(img)
ap.stop()