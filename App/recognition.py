import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os

model = tf.keras.models.load_model('App/recog_model')

image_number = 1
while os.path.isfile(f"App/temp/digit{image_number}.png"):
    try:
        img = cv2.imread(f"App/temp/digit{image_number}.png") [:,:,0]
        img = np.invert(np.array([img]))
        prediction = model.predict(img)
        print(f"Digit: {np.argmax(prediction)}")
        plt.imshow(img[0], cmap= plt.cm.binary)
        plt.show()
    except:
        print("error")
    finally:
        image_number += 1