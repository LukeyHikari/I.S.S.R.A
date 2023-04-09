import numpy as np
import cv2
from matplotlib import pyplot as plt
from PIL import Image
from scipy.ndimage import interpolation as inter
import easyocr

class recognition:
    def __init__(self):
        self.img = None
        self.skew = None
        self.gray = None
        self.blur = None
        self.resize = None
        self.invert = None
        self.edges = None
        self.thresh = None
        self.dilate = None
        self.erode = None
        self.contours = None
        self.rectx = []
        self.recty = []
        self.rectw = []
        self.recth = []

    def correct_skew(self, image, delta=1, limit=5):
        def determine_score(arr, angle):
            data = inter.rotate(arr, angle, reshape=False, order=0)
            histogram = np.sum(data, axis=1, dtype=float)
            score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
            return histogram, score

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 

        scores = []
        angles = np.arange(-limit, limit + delta, delta)
        for angle in angles:
            histogram, score = determine_score(thresh, angle)
            scores.append(score)

        best_angle = angles[scores.index(max(scores))]

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
        corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
                borderMode=cv2.BORDER_REPLICATE)
        
        return corrected

    def preprocess(self, _imgpath):
        #Load Image
        path = _imgpath
        self.img = cv2.imread(path)
        assert self.img is not None, "file could not be read, check with os.path.exists()"

        #Image Preprocessing
        #Skew Correction, Gray, and Resize
        self.skew = self.correct_skew(self.img)
        self.gray = cv2.cvtColor(self.skew, cv2.COLOR_BGR2GRAY)
        self.blur = cv2.blur(self.gray, (3,3))
        self.resize = cv2.resize(self.blur, (640,480))

        #Digits Finding
        self.invert = cv2.bitwise_not(self.resize)
        self.edges = cv2.Canny(self.invert,225,275)
        self.thresh = cv2.threshold(self.edges, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        self.dilate = cv2.dilate(self.thresh, cv2.getStructuringElement(cv2.MORPH_RECT, (8,9)), iterations=1)
        self.erode = cv2.erode(self.dilate, cv2.getStructuringElement(cv2.MORPH_RECT, (1,13)), iterations=1)
        self.dilate = cv2.dilate(self.erode, cv2.getStructuringElement(cv2.MORPH_RECT, (3,12)), iterations=1) 
        self.erode = cv2.erode(self.dilate, cv2.getStructuringElement(cv2.MORPH_RECT, (3,12)), iterations=1)
        self.dilate = cv2.dilate(self.erode, cv2.getStructuringElement(cv2.MORPH_RECT, (3,8)), iterations=1)

        #Contours
        self.contours = cv2.findContours(self.dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = self.contours[0] if len(self.contours) == 2 else self.contours[1]
        self.contours = sorted(self.contours, key=lambda x: cv2.boundingRect(x)[0])

        # cv2.imshow("Image", self.dilate)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    def indivbox(self, _imgpath):
        self.preprocess(_imgpath)
        roiloop = 0
        for i in self.contours:
            x,y,w,h = cv2.boundingRect(i)
            roiloop = roiloop+1
            roi = self.dilate[y-5:y+h+5, x-4:x+w+4]
            resizedroi = cv2.resize(roi, (28,28))
            invertedroi = cv2.bitwise_not(resizedroi)
            cv2.imwrite(f'App/temp/scoreline{roiloop}.png', invertedroi)
            cv2.rectangle(self.resize, (x, y), (x + w, y + h), (255,255,255), 2)

    def combinedbox(self, _imgpath):
        self.preprocess(_imgpath)

        for i in self.contours:
            x,y,w,h = cv2.boundingRect(i)
            # self.rectx.append(x)
            # self.recty.append(y)
            # self.rectw.append(w)
            # self.recth.append(h)
            
            if len(self.recty) == 0:
                if y < 150:
                    self.rectx.append(x)
                    self.recty.append(y)
                    self.rectw.append(w)
                    self.recth.append(h)
                else:
                    pass
            else:
                if y < self.recty[0]+50:
                    self.rectx.append(x)
                    self.recty.append(y)
                    self.rectw.append(w)
                    self.recth.append(h)
                else:
                    pass 
        
        self.erode = cv2.erode(self.dilate, cv2.getStructuringElement(cv2.MORPH_RECT, (10,1)), iterations=1)
        roi = self.erode[min(self.recty)-10:max(self.recty) + max(self.recth) + 10,
                          self.rectx[0]-30:self.rectx[len(self.rectx)-1] + self.rectw[len(self.rectw)-1]+30]
        invertedroi = cv2.bitwise_not(roi)

        cv2.rectangle(self.resize, (self.rectx[0], min(self.recty)),
                     (self.rectx[len(self.rectx)-1] + self.rectw[len(self.rectw)-1], max(self.recty) + max(self.recth)),
                     (255,255,255), 2)
        
        finalpath = f'App/temp/combined.png'

        cv2.imwrite(finalpath, invertedroi)
        # cv2.imshow("Preprocess", invertedroi)
        # cv2.imshow("Rectangles", self.resize)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        return finalpath

    def displayimg(self):
        self.indivbox()
        cv2.imshow("Image", self.resize)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

class scoresocr:
    def __init__(self):
        self.image = None
        self.invert = None
        self.reader = None
        self.result = None
        self.listed = [] 
    
    def identify_score(self, _imgpath):
        path = _imgpath
        self.image = cv2.imread(_imgpath)
        self.invert = cv2.bitwise_not(self.image)
        self.reader = easyocr.Reader(['en'])
        self.result = self.reader.readtext(self.invert)
        digits = self.result[0][1]
        self.listed = []

        for digit in digits:
            self.listed.append(digit)

        while " " in self.listed:
            self.listed.remove(" ")

        for i in range(len(self.listed)):
            if self.listed[i] == "l" or self.listed[i] == "!" or self.listed[i] == "/":
                self.listed[i] = "1"
            if self.listed[i] == "o" or self.listed[i] == "O":
                self.listed[i] = "0"
            if self.listed[i] == "z":
                self.listed[i] = "3"

        #print(self.listed)
        return self.listed

# if __name__ == '__main__':
#     run = recognition()
#     #run.preprocess()
#     #run.combinedbox('App/temp/sample3.jpg')
#     #run.displayimg()
