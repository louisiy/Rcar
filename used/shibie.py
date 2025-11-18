from maix import camera, display, image, nn, app

#mo xing pei zhi
detector = nn.YOLOv5(model="/root/models/cscs/model_165950.mud")

#摄像头初始化
cam = camera.Camera(detector.input_width(), detector.input_height(), detector.input_format())
dis = display.Display()

while not app.need_exit():
    img = cam.read()
    objs = detector.detect(img, conf_th = 0.5, iou_th = 0.45)
    
    for obj in objs:    #有几个球处理几次
        img.draw_rect(obj.x, obj.y, obj.w, obj.h, color = image.COLOR_RED)  
        # x 和 y 是框的左上角坐标，w 和 h 是框的宽度和高度，
        msg = f'{detector.labels[obj.class_id]}: {obj.score:.2f}'
        img.draw_string(obj.x, obj.y, msg, color = image.COLOR_RED)
        print(obj.class_id)
        if   obj.class_id == 0 :
            print(f'black   {obj.x} {obj.y}  ')
        elif  obj.class_id == 1 :
            print(f'red     {obj.x} {obj.y} ')
        elif  obj.class_id == 2 :
            print(f'yellow  {obj.x} {obj.y}  ')

    dis.show(img)

