import cv2 as cv
from Bead_Data.TapestriVision.Helper import Helper
import numpy as np


class Detect:

    @staticmethod
    def blob_detect(im: list) -> list:
        # Setup SimpleBlobDetector parameters.
        params = cv.SimpleBlobDetector_Params()

        params.filterByArea = True
        params.filterByCircularity = True
        params.filterByConvexity = True
        params.filterByInertia = False
        params.filterByColor = False

        params.minThreshold = 100
        params.maxThreshold = 255
        params.minArea = 5
        params.maxArea = 35
        params.minCircularity = 0.25
        params.minConvexity = 0.25
        params.minInertiaRatio = 0.00

        # Create a detector with the parameters
        detector = cv.SimpleBlobDetector_create(params)
        # Detect blobs.
        key_points = detector.detect(im)
        return key_points

    ######################################################################################
    @staticmethod
    def find_individual_drops(key_points: list, cropped_picture_org: list):
        individual_drop_pictures = []
        bead_location_return = []
        size_horizontal = 50
        size_vertical = 50
        cal_x = 20
        cal_y = 18

        blob_data = Helper.readable_key_points(key_points)
        for i in range(len(blob_data)):
            loc_x = blob_data[i][1] - cal_x
            loc_y = blob_data[i][2] - cal_y
            r = (loc_x, loc_y, size_horizontal, size_vertical)
            before_test = (cropped_picture_org[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])])
            if before_test.shape[0] > 20 and before_test.shape[1] > 20:
                individual_drop_pictures.append(before_test)
                loc_x += cal_x
                loc_y += cal_y
                r = (loc_x, loc_y, size_horizontal, size_vertical)
                bead_location_return.append(r)
        return [individual_drop_pictures, bead_location_return, [cal_x, cal_y]]

    ######################################################################################
    @staticmethod
    def hough_individual_drops(individual_drop_picture: list) -> list:
        circles = []

        for i in range(len(individual_drop_picture)):
            edges = 0
            edges = cv.Canny(individual_drop_picture[i], 20, 80)
            read_circle = Detect.hough_circles(edges, 1, 20, 50, 8, 8, 12)
            if read_circle[0][0][0] != "BAD READ":
                circles.append(read_circle)
        return circles

    ######################################################################################
    @staticmethod
    def hough_circles(image: list, dp: int, min_dist: int, param1: int,
                      param2: int, min_radius: int, max_radius: int) -> list:
        circles = 0

        try:
            circles = cv.HoughCircles(image, cv.HOUGH_GRADIENT, dp, min_dist,
                                      param1=param1,
                                      param2=param2,
                                      minRadius=min_radius,
                                      maxRadius=max_radius)
            if isinstance(circles, np.ndarray):
                circles = np.uint16(np.around(circles))
            else:
                circles = [[["BAD READ"]]]
        except:  # Hough circles will cause program to crash if it doesn't read anything
            print("no circle found")
        return circles

    ######################################################################################
