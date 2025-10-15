from preprocessing import imageProcessing
import cv2
import numpy as np

def recordScreenBoxFromPoint(x, y, width, height):
    # Screenshots are made from left down corner to right top corner
    left = x - width / 2
    top = y - height / 2
    right = x + width / 2
    bottom = y + height / 2
    screenshoot = ImageGrab.grab(
        bbox=(left, top, right, bottom))
    return np.array(screenshoot)

def detect_bite():
    """Detect fish bite using the cast position as detection center"""
    global cast_position
    detection_x, detection_y = cast_position
    img = recordScreenBoxFromPoint(detection_x, detection_y, 70, 70)
    img = imageProcessing(img)
    img = cv2.Canny(img, threshold1=60, threshold2=80)
    averageImg = np.average(img)
    return averageImg, img