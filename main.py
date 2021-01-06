import sys

import cv2
from PySide2 import QtWidgets
from PySide2.QtCore import QThreadPool, QCoreApplication, QRect, QMetaObject

from WatermarkDCT import WatermarkDCT
from gui_fns import *
from watermarker import LSBWatermarker
from worker import Worker
from PySide2.QtGui import QPixmap

from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QDialog, QFileDialog, QLabel, QGridLayout, QMessageBox, QMainWindow,
                               QHBoxLayout, QStatusBar, QMenuBar, QProgressBar, QWidget)

import sys


class Ui_MainWindow(object):

    def __init__(self):
        self.file_name = ""
        self.threadpool = QThreadPool()
        self.num_of_co = 1000
        self.alpha = 0.1

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1024, 768)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 0, 1021, 511))
        self.pictureLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.pictureLayout.setObjectName(u"pictureLayout")
        self.pictureLayout.setContentsMargins(0, 0, 0, 0)
        self.picture_label = QLabel(self.verticalLayoutWidget_2)
        self.picture_label.setObjectName(u"picture_label")

        self.pictureLayout.addWidget(self.picture_label)

        self.picture_button = QPushButton(self.verticalLayoutWidget_2)
        self.picture_button.setObjectName(u"picture_button")

        self.pictureLayout.addWidget(self.picture_button)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 520, 1011, 120))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.DCT_encode = QPushButton(self.horizontalLayoutWidget)
        self.DCT_encode.setObjectName(u"DCT_encode")

        self.verticalLayout_3.addWidget(self.DCT_encode)

        self.DCT_decode = QPushButton(self.horizontalLayoutWidget)
        self.DCT_decode.setObjectName(u"DCT_decode")

        self.verticalLayout_3.addWidget(self.DCT_decode)

        self.label_4 = QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.DCT_masg = QLineEdit(self.horizontalLayoutWidget)
        self.DCT_masg.setObjectName(u"DCT_masg")

        self.verticalLayout_3.addWidget(self.DCT_masg)

        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_3 = QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.LSB_encode = QPushButton(self.horizontalLayoutWidget)
        self.LSB_encode.setObjectName(u"LSB_encode")

        self.verticalLayout.addWidget(self.LSB_encode)

        self.LSB_decode = QPushButton(self.horizontalLayoutWidget)
        self.LSB_decode.setObjectName(u"LSB_decode")

        self.verticalLayout.addWidget(self.LSB_decode)

        self.lsb_encode_msg = QLabel(self.horizontalLayoutWidget)
        self.lsb_encode_msg.setObjectName(u"lsb_encode_msg")

        self.verticalLayout.addWidget(self.lsb_encode_msg)

        self.LSB_msg = QLineEdit(self.horizontalLayoutWidget)
        self.LSB_msg.setObjectName(u"LSB_msg")

        self.verticalLayout.addWidget(self.LSB_msg)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayoutWidget_3 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(20, 650, 981, 51))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.verticalLayoutWidget_3)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.progressBar = QProgressBar(self.verticalLayoutWidget_3)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout_2.addWidget(self.progressBar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1024, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        # bind functions
        self.picture_button.clicked.connect(self.open_file)
        self.LSB_encode.clicked.connect(self.call_lsb_encode)
        self.LSB_decode.clicked.connect(self.call_lsb_decode)
        self.DCT_encode.clicked.connect(self.call_dct_encode)
        self.DCT_decode.clicked.connect(self.call_dct_decode)
        # end bind functions()
        self.hide_progress_bar()
        self.disable_Methods(True)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Watermarking tool", None))
        # self.picture_label.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.picture_button.setText(QCoreApplication.translate("MainWindow", u"Select picture", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"DCT", None))
        self.DCT_encode.setText(QCoreApplication.translate("MainWindow", u"encode", None))
        self.DCT_decode.setText(QCoreApplication.translate("MainWindow", u"decode", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"coeficient:", None))
        self.DCT_masg.setText(QCoreApplication.translate("MainWindow", u"1000, 0.1", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"LSB", None))
        self.LSB_encode.setText(QCoreApplication.translate("MainWindow", u"encode", None))
        self.LSB_decode.setText(QCoreApplication.translate("MainWindow", u"decode", None))
        self.lsb_encode_msg.setText(QCoreApplication.translate("MainWindow", u"LSB msg:", None))
        self.LSB_msg.setText(QCoreApplication.translate("MainWindow", u"secret", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Work in progress:", None))

    # retranslateUi

    # def bindFunctions(self):

    def load_picture(self):
        pixmap = QPixmap(self.file_name[0])
        if pixmap.width() > pixmap.height():
            self.picture_label.setPixmap(pixmap.scaledToWidth(self.picture_label.width()))
        else:
            self.picture_label.setPixmap(pixmap.scaledToHeight(self.picture_label.height()))

    def open_file(self):
        self.hide_progress_bar()
        self.file_name = QFileDialog.getOpenFileName(None,
                                                     "Open Image", "",
                                                     "Image Files (*.png *.jpg *.bmp)")
        self.load_picture()
        self.disable_Methods(False)

    def method_LSB_encode(self, progress_callback):
        self.disable_Methods(True)
        progress_callback.emit(10)
        msg = self.LSB_msg.text()
        image = cv2.imread(self.file_name[0])
        watermarker = LSBWatermarker(image=image, mode='encode-message', message=msg, filename='result.png')
        progress_callback.emit(50)
        self.file_name = ["result.png", ""]
        watermarker.run()
        progress_callback.emit(90)
        self.load_picture()
        self.disable_Methods(False)
        progress_callback.emit(100)

    def method_LSB_decode(self, progress_callback):
        self.disable_Methods(True)
        self.LSB_msg.setText("")
        progress_callback.emit(10)
        image = cv2.imread(self.file_name[0])
        watermarker = LSBWatermarker(image=image, mode='decode-message')
        progress_callback.emit(50)
        watermarker.run()
        self.disable_Methods(False)
        progress_callback.emit(90)
        # self.show_decoded_msg(watermarker.decoded_msg)
        self.LSB_msg.setText("Decoded: " + watermarker.decoded_msg)
        progress_callback.emit(100)

    def method_DCT_encode(self, progress_callback):
        self.disable_Methods(True)
        progress_callback.emit(10)
        msg = self.DCT_masg.text().split(",")
        try:
            self.num_of_co = int(msg[0])
            self.alpha = float(msg[1])
            watermarker = WatermarkDCT(self.file_name[0], num_of_co=self.num_of_co, alpha=self.alpha)
            progress_callback.emit(50)
            watermarker.encode_watermark()
            self.DCT_masg.setText("Picture is watermarked?:" + str(watermarker.detect_watermark()))
        except Exception as e:
            print(e)
            self.DCT_masg.setText("Error: wrong parameters: example 1000, 0.1")
        finally:
            progress_callback.emit(90)
            self.load_picture()
            self.disable_Methods(False)
            progress_callback.emit(100)

    def method_DCT_decode(self, progress_callback):
        self.disable_Methods(True)
        progress_callback.emit(10)
        try:
            watermarker = WatermarkDCT(self.file_name[0], num_of_co=self.num_of_co, alpha=self.alpha)
            progress_callback.emit(50)
            self.DCT_masg.setText("Picture is watermarked?:" + str(watermarker.detect_watermark(self.file_name[0])))
        except Exception as e:
            print(e)
            self.DCT_masg.setText("Error: Unable to check the picture.")
        finally:
            progress_callback.emit(90)

            self.load_picture()
            self.disable_Methods(False)
            progress_callback.emit(100)

    def show_decoded_msg(self, msg):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Decoded message:")
        msgBox.setText(msg)
        msgBox.exec_()

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def progress_fn(self, n):
        self.progressBar.setValue(n)

    def print_output(self, s):
        print(s)

    def call_lsb_encode(self):
        self.show_progress_bar()
        self.call_function(self.method_LSB_encode)

    def call_lsb_decode(self):
        self.show_progress_bar()
        self.call_function(self.method_LSB_decode)

    def call_dct_encode(self):
        self.show_progress_bar()
        self.call_function(self.method_DCT_encode)

    def call_dct_decode(self):
        self.show_progress_bar()
        self.call_function(self.method_DCT_decode)

    def call_function(self, fn):
        worker = Worker(fn)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

    def hide_progress_bar(self):
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)
        self.label_6.setVisible(False)

    def show_progress_bar(self):
        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)
        self.label_6.setVisible(True)

    def disable_Methods(self, disable):
        self.LSB_encode.setDisabled(disable)
        self.LSB_decode.setDisabled(disable)
        self.DCT_decode.setDisabled(disable)
        self.DCT_encode.setDisabled(disable)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    w = QtWidgets.QMainWindow()
    ex.setupUi(w)
    w.show()
    sys.exit(app.exec_())
