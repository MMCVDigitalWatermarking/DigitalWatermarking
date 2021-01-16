import cv2
import numpy as np


class WatermarkDCT:
    def __init__(self, orig_img_path, num_of_co=1000, alpha=0.1):
        self.orig_img = self.load_img(orig_img_path)
        self.watermarked_img = None
        self.num_of_co = num_of_co
        self.alpha = alpha
        self.wm_vec = np.array([])
        self.coeff_ids = np.array([])
        self.orig_dct_coeff = np.array([])
        self.wm_sim = None

    @staticmethod
    def load_img(orig_img_path, color_mode=0):
        return np.float32(cv2.imread(orig_img_path, color_mode))

    @staticmethod
    def save_img(new_path, new_img):
        cv2.imwrite(new_path, new_img)

    def show_orig_img(self):
        self.show_img('original image', self.orig_img)

    def show_watermarked_img(self):
        self.show_img('watermarked image', self.watermarked_img)

    def show_difference_img(self):
        self.show_img('difference image', abs(self.watermarked_img - self.orig_img) * 10)

    def show_watermark_results(self):
        diff = abs(self.watermarked_img - self.orig_img) * 10  # scaled by 10 to better indicate differences
        combined_imgs = np.hstack((self.orig_img, self.watermarked_img, diff))
        self.show_img('watermark results', combined_imgs)

    @staticmethod
    def show_img(label, img):
        try:
            cropped_img = cv2.resize(img, (1800, 1200))
            cv2.imshow(label, np.uint8(cropped_img))
            cv2.waitKey(0)
            cv2.destroyWindow(label)
        except cv2.error:
            print('No image is loaded. Please choose a valid path.')

    def encode_watermark(self):
        dct_img = self.calculate_dct(self.orig_img)
        dct_img = np.array(dct_img)

        dct_vec = dct_img.flatten()
        self.coeff_ids = np.flip(np.argsort(np.absolute(dct_vec)))
        self.coeff_ids = self.coeff_ids[1:self.num_of_co + 1]
        self.orig_dct_coeff = dct_vec[self.coeff_ids]

        self.wm_vec = self.create_n_normal_values(self.num_of_co)

        dct_vec[self.coeff_ids] = self.calculate_dct_watermark()
        dct_wm = np.reshape(dct_vec, dct_img.shape)

        self.watermarked_img = self.calculate_inverse_dct(dct_wm)

    def detect_watermark(self, target_img_path=None, threshold=10):
        if target_img_path is None:
            target_img = self.watermarked_img
        else:
            target_img = self.load_img(target_img_path)

        dct_img = self.calculate_dct(target_img)
        dct_img = np.array(dct_img)
        dct_vec = dct_img.flatten()
        wm_dct_coeff = dct_vec[self.coeff_ids]

        wm_encoded = self.calculate_inverse_dct_watermark(self.orig_dct_coeff, wm_dct_coeff)
        if not wm_encoded.any():
            return False  # This is the case of trying to detect the watermark on the original image
        wm_sim = self.calculate_vec_similarity(wm_encoded, self.wm_vec)

        self.wm_sim = wm_sim
        return wm_sim > threshold

    def decode_watermark(self, target_img_path=None):
        if target_img_path is None:
            target_img = self.watermarked_img
        else:
            target_img = self.load_img(target_img_path)
        dct_img = self.calculate_dct(target_img)
        dct_img = np.array(dct_img)
        dct_vec = dct_img.flatten()
        dct_vec[self.coeff_ids] = self.orig_dct_coeff

        dct_decoded = np.reshape(dct_vec, dct_img.shape)
        self.watermarked_img = self.calculate_inverse_dct(dct_decoded)

    def calculate_dct_watermark(self):
        return self.orig_dct_coeff * (1 + self.alpha * self.wm_vec)

    def calculate_inverse_dct_watermark(self, original_dct_coeff, wm_dct_coeff):
        try:
            inv_dct_watermark = ((wm_dct_coeff / original_dct_coeff) - 1) / self.alpha
        except Exception:
            raise Exception('Couln\'t calculate the inverse dct watermark')
        return inv_dct_watermark

    @staticmethod
    def calculate_vec_similarity(vec1, vec2):
        vec1_row = np.array(vec1).reshape(1, -1)
        vec2_col = np.array(vec2).reshape(-1, 1)
        return (vec1_row @ vec2_col) / np.linalg.norm(vec1_row)

    @staticmethod
    def create_n_normal_values(length):
        return np.random.randn(length)

    @staticmethod
    def calculate_dct(img):
        img = np.float32(img)
        return cv2.dct(img)

    @staticmethod
    def calculate_inverse_dct(img):
        img = np.float32(img)
        return cv2.dct(img, flags=cv2.DCT_INVERSE)
