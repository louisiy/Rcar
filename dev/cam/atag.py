'''
    识别Apriltag
'''


from maix import image
import math

class ATAGHANDLER:
    def __init__(self):
        self.family = image.ApriltagFamilies.TAG36H11
        self.k = 1
        self.img = ""
        self.err = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.d = 0

    def distance(self,k,x,y,z):
        return abs(k*math.sqrt(x*x+y*y+z*z))

    def search(self,img):
        self.img = img.resize(320,240)
        atags = self.img.find_apriltags()
        if atags == []:
            self.err = 1
        elif atags != []:
            atag = atags[0]
            corners = atag.corners()
            for i in range(4):
                img.draw_line(((corners[i][0])*2), ((corners[i][1])*2), ((corners[(i + 1) % 4][0])*2), ((corners[(i + 1) % 4][1])*2), image.COLOR_GREEN, 5)
            self.x = -atag.x_translation()
            self.y = atag.y_translation()
            self.z = -atag.z_translation()
            self.d = int(self.distance(self.k,self.x,self.y,self.z)*100)
        return img

    def xyz(self):
        x = round(self.x, 2)
        y = round(self.y, 2)
        z = round(self.z, 2)

        return f"{x},{y},{z}"
