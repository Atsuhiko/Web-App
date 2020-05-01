import numpy as np
import cv2

def Predict_Dogs_Cats(img, model):
    IMAGE_WIDTH=224
    IMAGE_HEIGHT=224
    IMAGE_SIZE=(IMAGE_WIDTH, IMAGE_HEIGHT)
    
    img = cv2.resize(img, dsize=IMAGE_SIZE)
    img = np.expand_dims(img, axis=0)
    result = model.predict(img)
    
    return result

