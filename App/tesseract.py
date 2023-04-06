import pytesseract as pyt
import argparse
import cv2 as cv

pyt.pytesseract.tesseract_cmd =  r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image = cv.imread("App/temp/score.png")
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
text = pyt.image_to_string(image, config= "outputbase digits")
print(f'Score:{text}')



