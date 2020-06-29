

class Helper:

    # use this to turn your key point into a human readable item
    @staticmethod
    def readable_key_points(key_points: list) -> list:
        readable_keypoint = []

        for x in range(len(key_points)):
            readable_keypoint.append(
                [round(key_points[x].size, 2), round(key_points[x].pt[0], 2), round(key_points[x].pt[1], 2)])
        return readable_keypoint

    ######################################################################################

    @staticmethod
    def reformat_individual_circle_data(circles: list) ->list:
        reformatted_circle_info_hough = []

        for m in range(len(circles)):
            reformatted_circle_info_hough.append(
                [round(circles[m][0][0][0], 2), round(circles[m][0][0][1], 2), round(circles[m][0][0][2], 2)])
        return reformatted_circle_info_hough

    ######################################################################################

