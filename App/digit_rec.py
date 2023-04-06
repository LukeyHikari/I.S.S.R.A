import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from PIL import Image

class recognition:
    def __init__(self):
        self.img = None
        self.gray = None
        self.blur = None
        self.resize = None
        self.invert = None
        self.edges = None
        self.thresh = None
        self.dilatekernel = None
        self.erodekernel = None
        self.dilate = None
        self.erode = None
        self.contours = None
        self.rectx = []
        self.recty = []
        self.rectw = []
        self.recth = []

    def preprocess(self):
        #Load Image
        self.img = cv.imread('App/temp/sample.jpg')
        assert self.img is not None, "file could not be read, check with os.path.exists()"

        #Image Preprocessing and Canny
        self.gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        self.blur = cv.blur(self.gray, (3,3))
        self.resize = cv.resize(self.blur, (640,480))
        self.invert = cv.bitwise_not(self.resize)
        self.edges = cv.Canny(self.invert,300,400)
        self.thresh = cv.threshold(self.edges, 0,255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
        self.dilatekernel = cv.getStructuringElement(cv.MORPH_RECT, (3,7))
        self.dilate = cv.dilate(self.thresh,self.dilatekernel, iterations=1)

        #Contours
        self.contours = cv.findContours(self.dilate, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        self.contours = self.contours[0] if len(self.contours) == 2 else self.contours[1]
        self.contours = sorted(self.contours, key=lambda x: cv.boundingRect(x)[0])

    def box(self):
        self.preprocess()

        # roiloop = 0
        # for i in self.contours:
        #     x,y,w,h = cv.boundingRect(i)
        #     roiloop = roiloop+1
        #     roi = self.dilate[y-10:y+h+10, x-10:x+w+10]
        #     cv.imwrite(f'App/temp/scoreline{roiloop}.png',roi)
        #     cv.rectangle(self.resize, (x, y), (x + w, y + h), (255,255,255), 2)

        for i in self.contours:
            x,y,w,h = cv.boundingRect(i)

            self.rectx.append(x)
            self.recty.append(y)
            self.rectw.append(w)
            self.recth.append(h)
            
            # if x > 50 and w > 8 and y < 200 and h > 100:
            #     self.rectx.append(x)
            #     self.recty.append(y)
            #     self.rectw.append(w)
            #     self.recth.append(h)
        
        print(self.rectx)
        print(self.rectw)
        print(self.recty)
        print(self.recth)
        
        roi = self.dilate[min(self.recty)-10:max(self.recty) + max(self.recth) +10,
                          self.rectx[0]-20:self.rectx[len(self.rectx)-1] + self.rectw[len(self.rectw)-1]+20]
        cv.imwrite(f'App/temp/score.png', roi)
        im = Image.open(f'App/temp/score.png')
        im.save(f'App/temp/score.png', dpi=(300,300))

        cv.rectangle(self.resize, (self.rectx[0], min(self.recty)),
                     (self.rectx[len(self.rectx)-1] + self.rectw[len(self.rectw)-1], self.recty[5] + max(self.recth)),
                     (255,255,255), 2)

    def displayimg(self):
        self.box()
        cv.imshow("Image", self.resize)
        cv.waitKey(0)
        cv.destroyAllWindows()

if __name__ == '__main__':
    run = recognition()
    run.box()
