import cv2
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMessageBox, QFileDialog

from watermarker import LSBWatermarker
from worker import Worker


def load_picture(self):
    pixmap = QPixmap(self.file_name[0])
    if pixmap.width() > pixmap.height():
        self.label_picture.setPixmap(pixmap.scaledToWidth(self.label_picture.width()))
    else:
        self.label_picture.setPixmap(pixmap.scaledToHeight(self.label_picture.height()))


def open_file(self):
    self.file_name = QFileDialog.getOpenFileName(self,
                                                 "Open Image", "",
                                                 "Image Files (*.png *.jpg *.bmp)")
    self.load_picture()
    self.disable_buttons(False)


def method_LSB_encode(self, progress_callback):
    self.disable_buttons(True)
    progress_callback.emit(10)
    msg = self.msq_to_put.text()
    image = cv2.imread(self.file_name[0])
    watermarker = LSBWatermarker(image=image, mode='encode-message', message=msg, filename='result.png')
    progress_callback.emit(50)
    self.file_name = ["result.png", ""]
    watermarker.run()
    progress_callback.emit(90)
    self.load_picture()
    self.disable_buttons(False)
    progress_callback.emit(100)


def method_LSB_decode(self):
    self.disable_buttons(True)
    image = cv2.imread('result.png')
    watermarker = LSBWatermarker(image=image, mode='decode-message')
    watermarker.run()
    self.disable_buttons(False)
    self.show_decoded_msg(watermarker.decoded_msg)


def show_decoded_msg(self, msg):
    msgBox = QMessageBox()
    msgBox.setWindowTitle("Decoded message:")
    msgBox.setText(msg)
    msgBox.exec_()


def disable_buttons(self, disable):
    self.methodLSB_en_button.setDisabled(disable)
    self.methodLSB_de_button.setDisabled(disable)


def thread_complete(self):
    print("THREAD COMPLETE!")


def progress_fn(self, n):
    print("%d%% done" % n)


def print_output(self, s):
    print(s)


def oh_no(self):
    # Pass the function to execute
    worker = Worker(self.method_LSB_encode)  # Any other args, kwargs are passed to the run function
    worker.signals.result.connect(self.print_output)
    worker.signals.finished.connect(self.thread_complete)
    worker.signals.progress.connect(self.progress_fn)

    # Execute
    self.threadpool.start(worker)