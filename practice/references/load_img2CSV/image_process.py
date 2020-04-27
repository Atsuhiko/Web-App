import cv2

def canny(image):
    return cv2.Canny(image, 100, 200)