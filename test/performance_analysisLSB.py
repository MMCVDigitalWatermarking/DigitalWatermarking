import cv2
import numpy as np

from watermarker import LSBWatermarker


class PerformanceLSB():
    def __init__(self):
        self.msg = 'performance'
        self.out_file = 'result_LSB.png'
        self.in_file = '../media/test.png'
        image = cv2.imread(self.in_file)

        watermarker = LSBWatermarker(image=image, mode='encode-message', message=self.msg,
                                     filename=self.out_file)
        watermarker.run()

    def no_modification(self):
        image = cv2.imread(self.out_file)
        watermarker = LSBWatermarker(image=image, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("no_modification", result)

    def after_rotation_90(self):
        image = cv2.imread(self.out_file)
        image_mod = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE)
        watermarker = LSBWatermarker(image=image_mod, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("after_rotation_90", result)

    def after_rotation_180(self):
        image = cv2.imread(self.out_file)
        image_mod = cv2.rotate(image, cv2.cv2.ROTATE_180)
        watermarker = LSBWatermarker(image=image_mod, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("after_rotation_180", result)

    def after_rotation_90_and_back_to_normal(self):
        image = cv2.imread(self.out_file)
        image_mod = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE)
        image_mod = cv2.rotate(image_mod, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        watermarker = LSBWatermarker(image=image_mod, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("after_rotation_90_and_back_to_normal", result)

    def after_rotation_180_and_back_to_normal(self):
        image = cv2.imread(self.out_file)
        image_mod = cv2.rotate(image, cv2.cv2.ROTATE_180)
        image_mod = cv2.rotate(image_mod, cv2.cv2.ROTATE_180)
        watermarker = LSBWatermarker(image=image_mod, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("after_rotation_180_and_back_to_normal", result)

    def resize_to_150(self):
        image = cv2.imread(self.out_file)
        scale_percent = 150
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        image_mod = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        watermarker = LSBWatermarker(image=image_mod, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("resize_to_150", result)

    def resize_to_50(self):
        image = cv2.imread(self.out_file)
        scale_percent = 50
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        image_mod = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        watermarker = LSBWatermarker(image=image_mod, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("resize_to_50", result)

    def resize_to_50_and_back(self):
        image = cv2.imread(self.out_file)
        scale_percent = 50
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        image_mod = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        scale_percent = 200
        width = int(image_mod.shape[1] * scale_percent / 100)
        height = int(image_mod.shape[0] * scale_percent / 100)
        dim = (width, height)
        image_mod = cv2.resize(image_mod, dim, interpolation=cv2.INTER_AREA)
        watermarker = LSBWatermarker(image=image_mod, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("resize_to_50_and_back", result)

    def normalization(self):
        image = cv2.imread(self.out_file)
        zeros_img = np.zeros((800, 800))
        image_mod = cv2.normalize(image, zeros_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
        watermarker = LSBWatermarker(image=image_mod, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("normalization", result)

    def histograms_equalization(self):
        image = cv2.imread(self.out_file)
        image_mod = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_mod = cv2.equalizeHist(image_mod)
        cv2.imwrite("tmp.png", image_mod)
        image_mod = cv2.imread("tmp.png")
        watermarker = LSBWatermarker(image=image_mod, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("histograms_equalization", result)

    def gauss_noise(self):
        image = cv2.imread(self.out_file)
        row, col, ch = image.shape
        mean = 0
        var = 10
        sigma = var ** 0.5
        gauss = np.random.normal(mean, sigma, (row, col, ch))
        gauss = gauss.reshape(row, col, ch)
        noisy_img = image + gauss
        cv2.imwrite("gauss.png", noisy_img)
        image_mod = cv2.imread("gauss.png")
        watermarker = LSBWatermarker(image=image_mod, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("gauss_noise", result)

    def salt_and_peper(self):
        image = cv2.imread(self.out_file)
        row, col, ch = image.shape
        s_vs_p = 0.5
        amount = 0.004
        out = np.copy(image)
        # Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt))
                  for i in image.shape]
        out[coords] = 1

        # Pepper mode
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in image.shape]
        out[coords] = 0
        cv2.imwrite("sap.png", out)
        watermarker = LSBWatermarker(image=out, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("salt_and_peper", result)

    def jpg_conversion(self):
        image = cv2.imread(self.out_file)
        cv2.imwrite('result_LSB.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        image_jpg = cv2.imread('result_LSB.jpg')
        watermarker = LSBWatermarker(image=image_jpg, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("jpg_conversion", result)

    def jpg_conversion_and_back_to_png(self):
        image = cv2.imread(self.out_file)
        cv2.imwrite('result_LSB.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        image_jpg = cv2.imread('result_LSB.jpg')
        cv2.imwrite('result_LSB.jpg.png', image_jpg, [cv2.IMWRITE_PNG_COMPRESSION])
        image_out = cv2.imread('result_LSB.jpg.png')
        watermarker = LSBWatermarker(image=image_out, mode='decode-message')
        watermarker.run()
        result = watermarker.decoded_msg == self.msg
        self.printResult("jpg_conversion_and_back_to_png", result)

    def printResult(self, fn_name, result):
        pass_fail = "FAIL"
        if result:
            pass_fail = "PASS"
        print(fn_name + " : " + pass_fail)

    def runAllTests(self):
        self.no_modification()
        self.after_rotation_90()
        self.after_rotation_180()
        self.after_rotation_90_and_back_to_normal()
        self.after_rotation_180_and_back_to_normal()
        self.resize_to_150()
        self.resize_to_50()
        self.resize_to_50_and_back()
        self.normalization()
        self.histograms_equalization()
        self.gauss_noise()
        self.salt_and_peper()
        self.jpg_conversion()
        self.jpg_conversion_and_back_to_png()


if __name__ == "__main__":
    PerformanceLSB().runAllTests()
