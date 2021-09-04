import cv2
import numpy as np
import utilit

def super_scan(pathImage):

    width_Image = 480
    height_Image = 640
    #cap = cv2.VideoCapture(1)
    #cap.set(10, 160)
    while True:
        img = cv2.imread(pathImage)
        img = cv2.resize(img, (480, 640))

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        thres = utilit.valTrackbars()
        imgThreshold = cv2.Canny(imgBlur, thres[0], thres[1])
        kernel = np.ones((5, 5))
        imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)
        imgThreshold = cv2.erode(imgDial, kernel, iterations=1)

        # FIND CONTOURS

        imgContours = img.copy()
        imgBigContour = img.copy()
        contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)

        # FIND THE BIGGEST CONTOUR

        biggest, maxArea = utilit.biggestContour(contours)
        imageArray = [[]]
        if biggest.size != 0:
            biggest = utilit.reorder(biggest)
            cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)  # draw the biggest contour
            imgBigContour = utilit.drawRectangle(imgBigContour, biggest, 2)
            pts1 = np.float32(biggest)  # prepare points for warp
            pts2 = np.float32([[0, 0], [width_Image, 0],
                               [0, height_Image], [width_Image, height_Image]])  # prepare points for warp
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (width_Image, height_Image))

            # APPLY ADAPTIVE THRESHOLD
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgAdaptiveThre = cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
            imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
            imgAdaptiveThre = cv2.medianBlur(imgAdaptiveThre, 3)
        if cv2.waitKey(1):
            cv2.imwrite("Received/1.jpg", imgWarpGray)
            cv2.imwrite("Received/2.jpg", imgWarpColored)
            cv2.imwrite("Received/3.jpg", imgAdaptiveThre)
            break

