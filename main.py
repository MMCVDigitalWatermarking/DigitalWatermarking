import sys
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import (QPushButton, QApplication,
                               QVBoxLayout, QDialog, QFileDialog, QLabel, QGridLayout)


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.setWindowTitle("Watermarking tool")
        self.file_name = ""
        self.label_picture = QLabel(self)
        self.label_picture.setMinimumHeight(614)
        self.label_picture.setMinimumWidth(820)
        self.label = QLabel("Select picture")
        self.picture_button = QPushButton("Choose file")
        # Create layout and add widgets
        picture_layout = QGridLayout()
        buttons_layout = QGridLayout()
        picture_layout.addWidget(self.label_picture)
        buttons_layout.addWidget(self.label)
        buttons_layout.addWidget(self.picture_button)
        # Set layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(picture_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch(1)
        self.setLayout(main_layout)
        # Add button signal to greetings slot
        self.picture_button.clicked.connect(self.open_file)

    def load_picture(self):
        pixmap = QPixmap(self.file_name[0])
        self.label_picture.setPixmap(pixmap)

    def open_file(self):
        self.file_name = QFileDialog.getOpenFileName(self,
                                                     "Open Image", "",
                                                     "Image Files (*.png *.jpg *.bmp)")
        self.load_picture()


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.resize(1024, 768)
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
