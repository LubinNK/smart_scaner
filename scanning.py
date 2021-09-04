def scanner(pathImage, temp):
    import cv2
    import numpy as np
    import utilit
    import time


    #cap = cv2.VideoCapture(1)
    #cap.set(10, 160)

    # utilit.initializeTrackbars()
    count = 0
    counter = 0

    img = cv2.imread(pathImage)

    while True:

        # img = cv2.imread(pathImage)
        height_Image, width_Image, z = img.shape
        imgBlank = np.zeros((height_Image, width_Image, 3), np.uint8)
        #img = cv2.resize(img, (480, 640))

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        # thres = utilit.valTrackbars()
        imgThreshold = cv2.Canny(imgBlur, 151, 35)
        # print(thres[0], thres[1])
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

            imageArray = [[img, imgWarpGray, imgAdaptiveThre],
                      [imgContours, imgThreshold, imgWarpColored]]

        # LABLES FOR DISPLAY
        lables = [["Orig", "Gray", "Threshold", "Contours"],
                  ["Biggest Contour", "Warp Perspective", "Warp Grey", "Adaptive Threshold"]]
        #stackedImage = utilit.stackImages(imageArray, 0.2)
        #cv2.imshow("Result", stackedImage)

        counter += 1

        # print(counter)
        paths = []

        if counter > 100:
            time.sleep(1)
            cv2.imwrite("Received/scannedGray_" + str(temp) + ".jpg", imgWarpGray)
            paths.append("Received/scannedGray_" + str(temp) + ".jpg")
            time.sleep(1)
            cv2.imwrite("Received/scannedColored_"+str(temp)+".jpg", imgWarpColored)
            paths.append("Received/scannedColored_"+str(temp)+".jpg")
            time.sleep(1)
            cv2.imwrite("Received/scannedThre_"+str(temp)+".jpg", imgAdaptiveThre)
            saved = "Received/scannedThre_" + str(temp) + ".jpg"
            paths.append("Received/scannedThre_" + str(temp) + ".jpg")
            time.sleep(1)
            cv2.waitKey(300)
            count += 1

            return saved, paths
        #cv2.imshow("img", imgBlur)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break