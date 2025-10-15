import cv2

def imageProcessing(image):
    imageprocessing = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # imageprocessing = cv2.Canny(
    #     imageprocessing, threshold1=200, threshold2=300)
    return imageprocessing