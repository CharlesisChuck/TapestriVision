# TapestriVision Main Program page
# MissionBio 10/11/2019
from Bead_Data.TapestriVision.Capture import Capture
from Bead_Data.TapestriVision.Detect import Detect
from Bead_Data.TapestriVision.Infer import Infer
from Bead_Data.TapestriVision.Analyze import Analyse
from Bead_Data.TapestriVision.Helper import Helper

import cv2 as cv


class Main:

    def __init__(self):
        self.path = '../../Data/Output_Files_fail/frame0.jpg'
        self.max_frames = 50  # change this to 0 to read all the frames of the video
        self.pictures_read = 1
        self.data_print = []
        self.picture_print = []
        self.number_pictures = 0
        self.r = ()

        # THIS IS WHAT DATA YOU WISH TO DISPLAY
        self.range_data = [0, 0]
        self.range_pictures = [0, 0]
        self.run_analyze = False
        self.final_collected_data = []

    ######################################################################################
    @staticmethod
    def run_detection(cropped_picture: list):
        # BLOB METHOD
        ##################################
        key_points = Detect.blob_detect(cropped_picture)
        cv.imshow("KeyPoints", Analyse.draw_blobs(cropped_picture, key_points))

        # Use blob data to take individual pictures of blobs and find circles with Hough then format them
        ##################################
        [individual_drop_picture, individual_drop_location, [cal_x, cal_y]] = Detect. \
            find_individual_drops(key_points, cropped_picture)

        circles = Detect(). \
            hough_individual_drops(individual_drop_picture)

        large_beads_location_size = Infer.get_large_bead_location(
            circles, individual_drop_location, cal_x, cal_y)

        # These algorithms infer large and small bead properties from each other and then combine them
        [small_blob_certain, large_blob_with_small_unknown] = Infer. \
            remove_undetected_individual_drops(key_points, individual_drop_location)
        print("small_blob_certain: ", small_blob_certain)
        print("large_blob_with_small_unknown: ", large_blob_with_small_unknown)
        restored_key_points = Infer. \
            restore_key_points_lost_by_hough(key_points, small_blob_certain)
        print("restored_key_points", Helper.readable_key_points(restored_key_points))
        [large_beads_location_size_filtered, small_beads_key_points] = Infer. \
            find_large_beads_infer_small(large_beads_location_size, key_points)
        print("large_beads_location_size_filtered: ", large_beads_location_size_filtered)
        print("small_beads_key_points", Helper.readable_key_points(small_beads_key_points))
        key_point_location_size_removed = Infer. \
            filter_blob_by_location_size(key_points)
        print("key_point_location_size_removed: ", Helper.readable_key_points(key_point_location_size_removed))
        key_points_filtered = Infer. \
            combine_key_point_data_remove_unwanted(restored_key_points,
                                                   small_beads_key_points,
                                                   key_point_location_size_removed)
        print("key_points_filtered: ", Helper.readable_key_points(key_points_filtered))

        print("FINAL DATA: ", large_beads_location_size_filtered, "key: ", Helper.readable_key_points(key_points_filtered))
        return large_beads_location_size_filtered, key_points_filtered

    ######################################################################################
    @staticmethod
    def draw_data(large_beads_location_size, cropped_picture, key_points_filtered):
        # Draw our combined data for visual representation
        Analyse.draw_certain_filtered_hough_circle(large_beads_location_size, cropped_picture)
        final_picture = Analyse.draw_blobs(cropped_picture, key_points_filtered)
        return final_picture


TapestriVision = Main()

path = '../../Data/Output_Files_fail/frame0.jpg'
# Leave original in case you want ot compare
picture_org = Capture.read_image(path)
picture = picture_org.copy()

#r = Capture.crop_image(picture)
r = (449, 379, 273, 186)
detect_picture = picture[int(r[1]):int(r[1] + r[3]),
                  int(r[0]):int(r[0] + r[2])]

large_drops, small_drops = TapestriVision.\
    run_detection(detect_picture)

Image = TapestriVision.draw_data(
    large_drops, detect_picture, small_drops)
cv.imshow("final", Image)
cv.waitKey(0)
