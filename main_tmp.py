import sys

import cv2
from PySide2 import QtWidgets
from PySide2.QtCore import QThreadPool

from watermarker import LSBWatermarker
from worker import Worker
from PySide2.QtGui import QPixmap

from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QDialog, QFileDialog, QLabel, QGridLayout, QMessageBox, QMainWindow,
                               QHBoxLayout)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Create widgets

        self.setGeometry(0, 0, 1024, 768)
        self.threadpool = QThreadPool()
        self.setWindowTitle("Watermarking tool")
        self.file_name = ""
        self.label_picture = QLabel(self)
        self.label_picture.setMinimumHeight(614)
        self.label_picture.setMinimumWidth(820)
        self.label = QLabel("Select picture:")
        self.picture_button = QPushButton("Choose file")
        self.label_methods = QLabel("Available methods:")
        self.methodLSB_en_button = QPushButton("LSB encode")
        self.methodLSB_de_button = QPushButton("LSB decode")
        self.disable_buttons(True)
        self.msg_label = QLabel("Message to code (optional)")
        self.msq_to_put = QLineEdit(self)
        self.msq_to_put.setText("secret")
        # Create layout and add widgets
        buttons_layout = QHBoxLayout()
        picture_layout = QGridLayout()
        # buttons_layout = QGridLayout()
        msg_layout = QGridLayout()
        picture_layout.addWidget(self.label_picture)
        buttons_layout.addWidget(self.label)
        buttons_layout.addWidget(self.picture_button)
        buttons_layout.addWidget(self.label_methods)
        buttons_layout.addWidget(self.methodLSB_en_button)
        buttons_layout.addWidget(self.methodLSB_de_button)
        msg_layout.addWidget(self.msg_label)
        msg_layout.addWidget(self.msq_to_put)
        # Set layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(picture_layout)
        main_layout.addLayout(buttons_layout)
        # main_layout.addLayout(msg_layout)
        # main_layout.addStretch(1)
        # self.setCentralWidget(self)
        # self.centralWidget(self).setLayout(buttons_layout)
        # Add button signal to greetings slot
        self.picture_button.clicked.connect(self.open_file)
        self.methodLSB_en_button.clicked.connect(self.oh_no)
        self.methodLSB_de_button.clicked.connect(self.method_LSB_decode)

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


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    window = Window()
    # Window.resize(1024, 768)
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
