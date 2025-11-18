from maix import camera, display, image, app
from maix import uart, time

xunhuan_num = 0
#thresholds  = [[0, 80, 40, 80, 10, 80]]      # red
#thresholds = [[0, 80, 0, 80, 10, 80]]    # green
thresholds = [[0,100,-20,-10,60,80]] 

#摄像头初始化
cam = camera.Camera(640, 480, fps=60 ) 
disp = display.Display()

while not app.need_exit():
    img = cam.read()
    if xunhuan_num >= 2 :  #60帧判断一次
        blobs = img.find_blobs(thresholds, pixels_threshold=10)  #pixels_threshold 色块阈值
        if blobs != [] :    #判断是否识别成功
            for blob in blobs:
                print(blob[0], blob[1], blob[2], blob[3])
                img.draw_rect(blob[0], blob[1], blob[2], blob[3], image.COLOR_GREEN, 5)     #左上角为0点 矩形框选 （x, y, 宽，高, 线宽）
                if     abs(blob[0]  +  ( blob[2]/2 ) - 320) > 30 and ( blob[0]  +  ( blob[2]/2 ) ) < 320 :    # 先判断偏移量，x坐标加半径，320为中点， 再判断偏离方向
                    print(b'horizontal',blob[0]  +  ( blob[2]/2 ) - 320)        # 向右边移动
                elif   abs(blob[0]  +  ( blob[2]/2 ) - 320) > 30 and ( blob[0]  +  ( blob[2]/2 ) ) > 320 :
                    print(b'horizontal',blob[0]  +  ( blob[2]/2 ) - 320)        # 向左边移动
                elif   abs(blob[1]  +  ( blob[3]/2 ) - 240) > 30 and ( blob[1]  +  ( blob[3]/2 ) ) < 240 :
                    print(b'vertical',blob[1]  +  ( blob[3]/2 ) - 240)        # 向下边移动
                elif   abs(blob[1]  +  ( blob[3]/2 ) - 240) > 30 and ( blob[1]  +  ( blob[3]/2 ) ) > 240 :
                    print(b'vertical',blob[1]  +  ( blob[3]/2 ) - 240)        # 向上边移动            
        xunhuan_num = 0

    img.draw_rect( 320, 240, 30, 30, image.COLOR_RED, 5)   #在中心绘制中心点
    xunhuan_num = xunhuan_num + 1  
    disp.show(img)