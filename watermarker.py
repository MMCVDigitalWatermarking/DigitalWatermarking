import cv2


class NotSupportedModeException(Exception):
    pass


class Watermarker():
    def __init__(self, image):
        self.image = image

    def encode_message(self, message):
        pass

    def decode_message(self):
        pass


class LSBWatermarker(Watermarker):

    MESSAGE_DELIMITER = "$MMCV$"

    def __init__(self, image, mode, message=None, picture=None, filename=None):
        super().__init__(image)
        self.mode = mode
        self.message = message
        self.picture = picture
        self.filename = filename

    def run(self):
        if self.mode == 'encode-message' and self.message and self.filename:
            self.encode_message(self.message)
            self.save_image_to_file()
        elif self.mode == 'decode-message':
            self.decode_message()
        else:
            raise NotSupportedModeException("Mode not supported!")

    def save_image_to_file(self):
        cv2.imwrite(self.filename, self.image)

    def get_max_bytes_to_encode(self):
        return self.image.shape[0] * self.image.shape[1] * 3 / 8

    @staticmethod
    def get_binary_message(message):
        return ''.join([format(ord(char), "08b") for char in message])

    @staticmethod
    def get_binary_array(message):
        return [format(i, "08b") for i in message]

    @staticmethod
    def get_binary_int(array):
        return format(array, "08b")

    @staticmethod
    def get_data_from_lsb(rgb_array):
        data = ""
        for color in rgb_array:
            data += color[-1]
        return data

    def hide_data_in_lsb(self, row_column, binary_message, index):
        rgb_array = self.get_binary_array(row_column)
        for number, colour in enumerate(rgb_array):
            if index < len(binary_message):
                row_column[number] = int(colour[:-1] + binary_message[index], 2)
                index += 1
            if index >= len(binary_message):
                break
        return row_column, index

    def decode_bytes(self, message_bytes):
        message = ""
        for byte in message_bytes:
            message += chr(int(byte, 2))
            if message[-6:] == self.MESSAGE_DELIMITER:
                break
        return message[:-6]

    def encode_message(self, message):
        if len(message) > self.get_max_bytes_to_encode():
            raise ValueError("Too little image or too big secret message.")
        message += self.MESSAGE_DELIMITER
        binary_message = self.get_binary_message(message)
        index = 0
        for rows in self.image:
            for row_column in rows:
                row_column, index = self.hide_data_in_lsb(row_column, binary_message, index)

    def decode_message(self):
        binary_data = ""
        for rows in self.image:
            for row_column in rows:
                rgb_array = self.get_binary_array(row_column)
                binary_data += self.get_data_from_lsb(rgb_array)
        message_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
        message = self.decode_bytes(message_bytes)
        print("Decoded message is: '{}'".format(message))

    def encode_picture(self, picture):
        pass

    def decode_picture(self):
        pass
