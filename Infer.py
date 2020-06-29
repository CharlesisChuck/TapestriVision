from Bead_Data.TapestriVision.Helper import Helper


class Infer:

    @staticmethod
    def get_large_bead_location(circles: list, bead_location_return: list, cal_x: int, cal_y: int) -> list:
        reformatted_circle_info_hough = Helper.reformat_individual_circle_data(circles)
        large_beads_location_size = []

        for j in range(len(reformatted_circle_info_hough)):
            final_x = reformatted_circle_info_hough[j][0] + bead_location_return[j][0] - cal_x
            final_y = reformatted_circle_info_hough[j][1] + bead_location_return[j][1] - cal_y
            large_beads_location_size.append(
                [round(final_x, 2), round(final_y, 2), reformatted_circle_info_hough[j][2]])
        large_beads_location_size = sorted(large_beads_location_size, key=lambda x: x[1], reverse=False)
        return large_beads_location_size

    ######################################################################################
    @staticmethod
    def remove_undetected_individual_drops(key_points: list, individual_drop_location: list):
        # Remove all large blob data from original blob detect and create list off large blobs
        readable_key_points = Helper.readable_key_points(key_points)
        small_blob_certain = readable_key_points.copy()
        large_blob_with_small_unknown = []
        removed_increment = 0

        for j in range(len(readable_key_points)):
            for k in range(len(individual_drop_location)):
                if readable_key_points[j][1] == individual_drop_location[k][0]:
                    large_blob_with_small_unknown.append(readable_key_points[j])
                    small_blob_certain.remove(small_blob_certain[j - removed_increment])
                    removed_increment += 1
                    break
        return [small_blob_certain, large_blob_with_small_unknown]

    ######################################################################################
    @staticmethod
    def restore_key_points_lost_by_hough(key_points: list, small_blob_certain: list) -> list:
        restored_key_points = []

        for x in range(len(key_points)):
            lost_data_key_points_from_hough = \
                [round(key_points[x].size, 2), round(key_points[x].pt[0], 2), round(key_points[x].pt[1], 2)]
            for y in range(len(small_blob_certain)):
                if lost_data_key_points_from_hough[1] == small_blob_certain[y][1]:
                    restored_key_points.append(key_points[x])
        return restored_key_points

    ######################################################################################
    @staticmethod
    def find_large_beads_infer_small(large_beads_location_size: list, key_points: list) -> list:
        length_list = len(large_beads_location_size)
        list_index = 0
        removed = 0
        small_beads_key_points = []

        while list_index < length_list - removed:
            if list_index + 1 == length_list - removed:  # stop the loop before we go beyond the index
                break
            if (large_beads_location_size[list_index + 1][0] + 4) >= \
                    large_beads_location_size[list_index][0] >= \
                    (large_beads_location_size[list_index + 1][0] - 4):
                removed += 1
                large_beads_location_size.remove(large_beads_location_size[list_index])
                list_index -= 1  # run the loop again to check for more than 2 repeated values
                small_beads_key_points.append(key_points[list_index])
            list_index += 1
        return [large_beads_location_size, small_beads_key_points]

    ######################################################################################
    @staticmethod
    def filter_blob_by_location_size(key_points: list) -> list:
        key_point_location_removed = []
        range_size = [1, 6]
        range_x = [3, 300]
        range_y = [20, 120]

        readable_key_points = Helper.readable_key_points(key_points)
        removed_blob_location_index = Infer. \
            filter_blobs_location_return_index(
                readable_key_points, range_size, range_x, range_y)
        if removed_blob_location_index:
            for h in range(len(removed_blob_location_index)):
                key_point_location_removed.append(key_points[removed_blob_location_index[h]])
        return key_point_location_removed

    ######################################################################################
    @staticmethod
    def filter_blobs_location_return_index(readable_key_points: list, range_size: [int, int],
                                           range_x: [int, int], range_y: [int, int]) -> list:
        i = 0
        removed = []

        while i < len(readable_key_points):
            if readable_key_points[i][0] < range_size[0] or readable_key_points[i][0] > range_size[1]:
                removed.append(i)
            if readable_key_points[i][1] < range_x[0] or readable_key_points[i][1] > range_x[1]:
                removed.append(i)
            if readable_key_points[i][2] < range_y[0] or readable_key_points[i][2] > range_y[1]:
                removed.append(i)
            i += 1
        return removed

    ######################################################################################
    # TODO fix the fact that we are not using small_beads_key_points (THIS IS NEEDED)
    @staticmethod
    def combine_key_point_data_remove_unwanted(
            restored_key_points: list, small_beads_key_points: list, key_point_location_size_removed: list) -> list:
        key_points = []

        for z in range(len(small_beads_key_points)):
            key_points.append(small_beads_key_points[z])
        for z in range(len(restored_key_points)):
            key_points.append(restored_key_points[z])
        for t in range(len(restored_key_points)):
            key_points.append(restored_key_points[t])
        x = 0
        while x < len(key_points):
            for u in range(len(key_point_location_size_removed)):
                if key_points[x] == key_point_location_size_removed[u]:
                    key_points.remove(key_points[x])
                    x += 1
                    break
            x += 1
        return key_points

    ######################################################################################
