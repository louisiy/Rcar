from maix import image
import math

class ATAGHANDLER:
    def __init__(self):
        self.family = image.ApriltagFamilies.TAG36H11
        self.k = 1
        self.img = ""
        self.atags = []
        self.x = 0
        self.y = 0
        self.z = 0
        self.d = 0

    def distance(self,k,x,y,z):
        return abs(k*math.sqrt(x*x+y*y+z*z))

    def search(self,img):
        self.img = img.resize(320,240)
        self.atags = self.img.find_apriltags()
        if self.atags != []:
            atag = atags[0]
            corners = atag.corners()
            for i in range(4):
                img.draw_line(((corners[i][0])*2), ((corners[i][1])*2), ((corners[(i + 1) % 4][0])*2), ((corners[(i + 1) % 4][1])*2), image.COLOR_GREEN, 10)
            self.x = -atag.x_translation()
            self.y = atag.y_translation()
            self.z = -atag.z_translation()
            self.d = int(distance(self.k,self.x,self.y,self.z)*100)
        return img



