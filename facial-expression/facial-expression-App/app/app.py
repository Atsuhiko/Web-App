import os
import random
from keras.preprocessing.image import load_img
import numpy as np
import cv2

from tensorflow.keras.models import load_model
model = load_model('2020-09-27-epoch50.h5')

filenames = os.listdir("../images")
IMAGE_SIZE=(48, 48)

sample = random.choice(filenames)
img = load_img("./images/"+sample, target_size=IMAGE_SIZE)
img_org = img