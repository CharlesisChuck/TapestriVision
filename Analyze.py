import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math


class Analyse:

    @staticmethod
    def draw_certain_filtered_hough_circle(large_beads_location_size: list, cropped_picture_org: list) -> list:
        filters_hough_circle_pictures = []

        for j in range(len(large_beads_location_size)):
            circles_picture = cv.circle(cropped_picture_org,
                                        (int(large_beads_location_size[j][0]), int(large_beads_location_size[j][1])),
                                        int(large_beads_location_size[j][2]), (0, 255, 0), 1)
            filters_hough_circle_pictures.append(circles_picture)
        return filters_hough_circle_pictures

    ######################################################################################
    @staticmethod
    def draw_hough_circle_individual(circles: list, individual_drop_picture: list) -> list:
        picture_list = []

        for i in range(len(circles)):
            circles_picture = cv.circle(individual_drop_picture[i], (circles[i][0][0][0], circles[i][0][0][1]),
                                        circles[i][0][0][2], (0, 255, 0), 1)
            picture_list.append(circles_picture)
        return picture_list

    ######################################################################################
    @staticmethod
    def draw_blobs(image: list, key_points: list) -> list:
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_key_points = cv.drawKeypoints(image,
                                              key_points,
                                              np.array([]),
                                              (255, 0, 255),
                                              cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        return im_with_key_points

    ######################################################################################
    @staticmethod
    def global_data(combined_data_all_list: list):
        global_sizes, global_x, global_y = [], [], []

        for i in range(len(combined_data_all_list)):
            for j in range(len(combined_data_all_list[i])):
                global_sizes.append(combined_data_all_list[i][j][1])
                global_x.append(combined_data_all_list[i][j][2])
                global_y.append(combined_data_all_list[i][j][3])
        return [global_sizes, global_x, global_y]

    ######################################################################################
    @staticmethod
    def check_size(data, range_list):
        if range_list[1] != 0 and len(data) < range_list[1]:
            range_list[1] = len(data)
        return range_list

    ######################################################################################
    @staticmethod
    def print_data(data, range_list):
        for i in range(10000)[range_list[0]:range_list[1]]:
            print("Data Print " + str(i) + ":\n")
            print(data[i])
            print("******************************************")

    ######################################################################################
    @staticmethod
    def display_data(data, range_list):
        range_list = Analyse.check_size(data,range_list)
        Analyse.print_data(data,range_list)

    ######################################################################################
    @staticmethod
    def display_pictures(print_pictures, range_list):
        range_list = Analyse.check_size(print_pictures, range_list)

        size_wanted = range_list[1]-range_list[0]

        if size_wanted != 0:
            columns = int(math.sqrt(size_wanted))
            row = math.ceil(size_wanted / columns)

            j = 0
            for i in range(10000)[range_list[0]:range_list[1]]:
                plt.subplot(columns, row, j + 1), plt.imshow(print_pictures[i], 'gray')
                plt.title("Picture" + str(i))
                plt.xticks([]), plt.yticks([])
                j += 1
            plt.show()

    ######################################################################################
    @staticmethod
    def display_scatter(global_sizes, global_x, global_y):
        # This import registers the 3D projection, but is otherwise unused.
        from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(global_sizes, global_x, global_y)
        ax.set_xlabel('Size')
        ax.set_ylabel('X')
        ax.set_zlabel('Y')
        plt.show()
