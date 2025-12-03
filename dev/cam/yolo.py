from maix import nn,image

class YOLOHANDLER:
    def __init__(self):
        self.det = nn.YOLOv5(model="/root/models/cscs/model_165950.mud")
        self.img = ""
        self.objs =[]

    def search(self,img):
        self.img = img.resize(self.det.input_width(),self.det.input_height()).to_format(image.FMT_RGB888)
        self.objs = self.det.detect(self.img, conf_th = 0.5, iou_th = 0.45)
        if self.objs != []:
            obj = self.objs[0]
            img.draw_rect(obj.x, obj.y, obj.w, obj.h, color = image.COLOR_RED)  
            msg = f'{detector.labels[obj.class_id]}: {obj.score:.2f}'
            img.draw_string(obj.x, obj.y, msg, color = image.COLOR_RED)
        return img