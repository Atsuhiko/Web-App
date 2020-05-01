import numpy as np
import pandas as pd
from PIL import Image
import cv2

from keras.models import Model # keras 2.2.4
from keras.layers import Dense
from keras import optimizers
from keras.preprocessing import image
#from keras.preprocessing.image import ImageDataGenerator, load_img
from keras.utils import to_categorical
from keras.applications.vgg16 import VGG16

#from sklearn.model_selection import train_test_split
#import matplotlib.pyplot as plt
# import random
# import os

def build_vgg():
    IMAGE_CHANNELS=3
    vggmodel = VGG16(weights='imagenet', include_top=True)
    X= vggmodel.layers[-2].output
    predictions = Dense(2, activation="softmax")(X)
    model = Model(input = vggmodel.input, output = predictions)
    model.compile(loss = "categorical_crossentropy", optimizer = optimizers.SGD(lr=0.0001, momentum=0.9), metrics=["accuracy"])
    model.load_weights('vgg16_1.h5')
    return model

def Predict_Dogs_Cats(img, model):
    IMAGE_WIDTH=224
    IMAGE_HEIGHT=224
    IMAGE_SIZE=(IMAGE_WIDTH, IMAGE_HEIGHT)
    
    img = cv2.resize(img, dsize=IMAGE_SIZE)
    img = np.expand_dims(img, axis=0)
    result = model.predict(img)
    
    return result

