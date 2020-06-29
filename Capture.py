import cv2 as cv


class Capture:

    @staticmethod
    def read_image(path):
        image = cv.imread(path)
        return image

    ######################################################################################
    @staticmethod
    def gray_image(image: list) -> list:
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        return gray_image

    ######################################################################################
    @staticmethod
    def crop_image(image: list) -> list:
        r = cv.selectROI(image)
        return r

    ######################################################################################
    @staticmethod
    def generate_pictures(video: str, frames: int) -> int:
        cap = cv.VideoCapture(video)
        count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            cv.imwrite("../Output_Files/frame%d.jpg" % count, frame)
            count = count + 1
            if count >= frames != 0:
                break
            if cv.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv.destroyAllWindows()  # destroy all the opened windows
        return count
