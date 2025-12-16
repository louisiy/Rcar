'''
    颜色识别
'''


from maix import image

class COLORHANDLER:
    def __init__(
                 self,
                 thresholds=[[0, 100, -20, -10, 60, 80]],
                 interval=2
                ):
        self.thresholds = thresholds
        self.interval = interval
        self.err = 0
        self.d = 0

    def search(self,img):
        blobs = img.find_blobs(self.thresholds, pixels_threshold=10)
        if blobs == []:
            self.err = 1
        elif blobs != []:
            for blob in blobs:
                x, y, w, h = blob[0], blob[1], blob[2], blob[3]
                img.draw_rect(x, y, w, h, image.COLOR_GREEN, 5)
                bottom = y + h
                center = 240
                self.d = bottom - center
        return img

    def dis(self):
        dis = round(self.d,2)

        return f"{dis}"