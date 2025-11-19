from maix import image

class COLORHANDLER:
    def __init__(self,
                 thresholds=[[0, 100, -20, -10, 60, 80]],
                 interval=2
                ):
        self.thresholds = thresholds
        self.interval = interval

    def search(self,img):
        blobs = img.find_blobs(self.thresholds, pixels_threshold=10)
        if blobs != []:
            for blob in blobs:
                print(blob[0], blob[1], blob[2], blob[3])
                img.draw_rect(blob[0], blob[1], blob[2], blob[3], image.COLOR_GREEN, 5)
                if     abs(blob[0]  +  ( blob[2]/2 ) - 320) > 30 and ( blob[0]  +  ( blob[2]/2 ) ) < 320 :
                    print(b'horizontal',blob[0]  +  ( blob[2]/2 ) - 320)
                elif   abs(blob[0]  +  ( blob[2]/2 ) - 320) > 30 and ( blob[0]  +  ( blob[2]/2 ) ) > 320 :
                    print(b'horizontal',blob[0]  +  ( blob[2]/2 ) - 320)
                elif   abs(blob[1]  +  ( blob[3]/2 ) - 240) > 30 and ( blob[1]  +  ( blob[3]/2 ) ) < 240 :
                    print(b'vertical',blob[1]  +  ( blob[3]/2 ) - 240)
                elif   abs(blob[1]  +  ( blob[3]/2 ) - 240) > 30 and ( blob[1]  +  ( blob[3]/2 ) ) > 240 :
                    print(b'vertical',blob[1]  +  ( blob[3]/2 ) - 240)
        return img
