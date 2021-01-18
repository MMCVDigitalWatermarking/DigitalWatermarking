import cv2
import numpy as np
from WatermarkDCT import WatermarkDCT


class PerformanceDCT:
    def __init__(self, num_of_co=1000, alpha=0.1):
        self.msg = 'performance'
        self.out_file = 'result_DCT.png'
        self.in_file = '../../media/test.png'
        self.num_of_co = num_of_co
        self.alpha = alpha

        self.dct_wm = WatermarkDCT(self.in_file, num_of_co=self.num_of_co, alpha=self.alpha)
        self.dct_wm.encode_watermark()

    @staticmethod
    def rotate_image(image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result

    @staticmethod
    def scale_img(img, scale_percent):
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)

        return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    @staticmethod
    def load_img(orig_img_path, color_mode=0):
        return np.float32(cv2.imread(orig_img_path, color_mode))

    @staticmethod
    def save_img(new_path, new_img):
        cv2.imwrite(new_path, new_img)

    @staticmethod
    def show_img(label, img):
        try:
            cropped_img = cv2.resize(img, (1800, 1200))
            cv2.imshow(label, np.uint8(cropped_img))
            cv2.waitKey(0)
            cv2.destroyWindow(label)
        except cv2.error:
            print('No image is loaded. Please choose a valid path.')

    def no_modification(self):
        self.save_img('dct_output.png', self.dct_wm.watermarked_img)
        self.print_result(
            'no_modification',
            self.dct_wm.detect_watermark(),
            self.dct_wm.wm_sim
        )

    def after_rotation_90(self):
        rotated_img = cv2.rotate(self.load_img(self.out_file), cv2.cv2.ROTATE_90_CLOCKWISE)
        self.save_img('rot_90.png', rotated_img)

        self.print_result(
            'after_rotation_90',
            self.dct_wm.detect_watermark('rot_90.png'),
            self.dct_wm.wm_sim
        )

    def after_rotation_90_and_back_to_normal(self):
        rotated_img = cv2.rotate(self.load_img(self.out_file), cv2.cv2.ROTATE_90_CLOCKWISE)
        normal_img = cv2.rotate(rotated_img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.save_img('rot_90_and_back.png', normal_img)

        self.print_result(
            'after_rotation_90_and_back_to_normal',
            self.dct_wm.detect_watermark('rot_90_and_back.png'),
            self.dct_wm.wm_sim
        )

    def after_multiple_scalings(self):
        scaled_img = self.scale_img(self.load_img(self.out_file), 100)
        scaled_img = self.scale_img(scaled_img, 20)
        scaled_img = self.scale_img(scaled_img, 300)
        scaled_img = self.scale_img(scaled_img, 10)
        self.save_img('scaled.png', scaled_img)

        self.print_result(
            'after_multiple_scalings',
            self.dct_wm.detect_watermark('scaled.png'),
            self.dct_wm.wm_sim
        )

    def normalization(self):
        zeros_img = np.zeros((800, 800))
        normalized_img = cv2.normalize(self.load_img(self.out_file), zeros_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        self.save_img('normalized.png', normalized_img)

        self.print_result(
            'normalization',
            self.dct_wm.detect_watermark('normalized.png'),
            self.dct_wm.wm_sim
        )

    def histograms_equalization(self):
        img = cv2.imread(self.out_file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist_eq_img = cv2.equalizeHist(img)
        self.save_img('hist_eq.png', hist_eq_img)

        self.print_result(
            'histograms_equalization',
            self.dct_wm.detect_watermark('hist_eq.png'),
            self.dct_wm.wm_sim
        )

    def gauss_noise(self):
        image = self.load_img(self.out_file)
        row, col = image.shape
        mean = 0
        var = 10
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col))
        gauss = gauss.reshape(row, col)
        gauss_img = image + gauss
        self.save_img('gauss.png', gauss_img)

        self.print_result(
            'gauss_noise',
            self.dct_wm.detect_watermark('gauss.png'),
            self.dct_wm.wm_sim
        )

    def salt_and_peper(self):
        image = self.load_img(self.out_file)
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)

        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in image.shape]
        out[tuple(coords)] = 1

        # Pepper mode
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in image.shape]
        out[tuple(coords)] = 0

        self.save_img('salt_and_pepper.png', out)
        self.print_result(
            'salt_and_peper',
            self.dct_wm.detect_watermark('salt_and_pepper.png'),
            self.dct_wm.wm_sim
        )

    def jpg_conversion(self):
        image = self.load_img(self.out_file)
        cv2.imwrite('jpg_test.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

        self.print_result(
            'jpg_conversion',
            self.dct_wm.detect_watermark('jpg_test.jpg'),
            self.dct_wm.wm_sim
        )

    def jpg_conversion_and_back_to_png(self):
        image = self.load_img(self.out_file)
        cv2.imwrite('jpg_test.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        jpg_img = self.load_img('jpg_test.jpg')
        cv2.imwrite('jpg_and_back.png', jpg_img, [cv2.IMWRITE_PNG_COMPRESSION])

        self.print_result(
            'jpg_conversion_and_back_to_png',
            self.dct_wm.detect_watermark('jpg_and_back.png'),
            self.dct_wm.wm_sim
        )

    @staticmethod
    def print_result(fn_name, result, similarity):
        pass_fail = "FAIL"
        if result:
            pass_fail = "PASS"
        print(fn_name + " : " + str(similarity) + " : " + pass_fail)

    def run_all_tests(self):
        self.no_modification()
        self.after_rotation_90()
        self.after_rotation_90_and_back_to_normal()
        self.after_multiple_scalings()
        self.normalization()
        self.histograms_equalization()
        self.gauss_noise()
        self.salt_and_peper()
        self.jpg_conversion()
        self.jpg_conversion_and_back_to_png()


if __name__ == "__main__":
    PerformanceDCT().run_all_tests()
