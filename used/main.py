from maix import camera, display, image, app, pinmap, uart, app, time
import threading

i = 0
thresholds = [[0,100,-20,-10,60,80]] 

def re_uart (serial) :
    global stuts0, stuts1, serial0, serial1
    while 1:
        # 串口  接收数据
        data = serial.read() 
        data = data.decode("utf-8",errors="ignore")
        if data != "" and serial == serial0:  #串口0 赋值
         #   print(data)
            stuts0  = data
            data    = ""
        if data != "" and serial == serial1:  #串口1 赋值
            stuts1  = data
            data    = ""

# 串口初始化
pinmap.set_pin_function("A29", "UART2_RX")
pinmap.set_pin_function("A28", "UART2_TX")
device = "/dev/ttyS0"
serial0 = uart.UART(device, 115200)
device = "/dev/ttyS2"
serial1 = uart.UART(device, 115200)

uart0_thread = threading.Thread(target=re_uart, args = (serial0,))
uart0_thread.daemon = True
uart0_thread.start()

uart1_thread = threading.Thread(target=re_uart, args = (serial1,))
uart1_thread.daemon = True
uart1_thread.start()

#摄像头初始化
cam = camera.Camera(640, 480, fps=60 ) 
disp = display.Display()



while not app.need_exit():
    img = cam.read()
    if i >= 2 :  #60帧判断一次
        blobs = img.find_blobs(thresholds, pixels_threshold=10)  #pixels_threshold 色块阈值
        if blobs != [] :    #判断是否识别成功
            for blob in blobs:
                print(blob[0], blob[1], blob[2], blob[3])
                img.draw_rect(blob[0], blob[1], blob[2], blob[3], image.COLOR_GREEN, 5)     #左上角为0点 矩形框选 （x, y, 宽，高, 线宽）
                if     abs(blob[0]  +  ( blob[2]/2 ) - 320) > 30 and ( blob[0]  +  ( blob[2]/2 ) ) < 320 :    # 先判断偏移量，x坐标加半径，320为中点， 再判断偏离方向
                    pass
                elif   abs(blob[0]  +  ( blob[2]/2 ) - 320) > 30 and ( blob[0]  +  ( blob[2]/2 ) ) > 320 :
                    print(b'horizontal',blob[0]  +  ( blob[2]/2 ) - 320)        # 向左边移动
                elif   abs(blob[1]  +  ( blob[3]/2 ) - 240) > 30 and ( blob[1]  +  ( blob[3]/2 ) ) < 240 :
                    print(b'vertical',blob[1]  +  ( blob[3]/2 ) - 240)        # 向下边移动
                elif   abs(blob[1]  +  ( blob[3]/2 ) - 240) > 30 and ( blob[1]  +  ( blob[3]/2 ) ) > 240 :
                    print(b'vertical',blob[1]  +  ( blob[3]/2 ) - 240)        # 向上边移动            
        i = 0

    img.draw_rect( 320, 240, 30, 30, image.COLOR_RED, 5)   #在中心绘制中心点
    i = i + 1  
    disp.show(img)