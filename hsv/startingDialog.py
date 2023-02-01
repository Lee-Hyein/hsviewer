from PySide6.QtWidgets import *
from PySide6.QtGui import QImage, QPixmap
from PySide6 import QtCore 
from loguru import logger

class StartingDialog(QDialog):
    OTHER = 0
    OPEN_ORIGINAL_PROJECT = 1
    OPEN_PORTABLE_PROJECT = 2

    def __init__(self, appname, version):
        super(StartingDialog, self).__init__()
        self.setWindowTitle(f'{appname} ({version})')
        
        layout_root = QHBoxLayout()

        self.layout_left_vertical = QVBoxLayout()

        self.label_logo = QLabel(self)
        self.label_logo.setScaledContents(True)

        self.label_title = QLabel(f'hyperspectral viewer ({version})')
        title_font = self.label_title.font()
        title_font.setBold(True)
        self.label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.layout_left_vertical.addWidget(self.label_logo)
        self.layout_left_vertical.addWidget(self.label_title)
        self.layout_left_vertical.addStretch()

        self.layout_right_vertical = QVBoxLayout()

        self.pushButton_50bands = QPushButton(self.tr('wavelength(50)'))
        self.pushButton_150bands = QPushButton(self.tr('wavelength(150)'))

        self.layout_right_vertical.addWidget(self.pushButton_50bands)
        self.layout_right_vertical.addWidget(self.pushButton_150bands)
        self.layout_right_vertical.addStretch()

        layout_root.addLayout(self.layout_left_vertical, 1)
        layout_root.addLayout(self.layout_right_vertical, 1)
        self.setLayout(layout_root)

        self.pushButton_50bands.clicked.connect(self.on50bandsPage)
        self.pushButton_50bands.setFlat(True)
        self.pushButton_150bands.clicked.connect(self.on150bandsPage)
        self.pushButton_150bands.setFlat(True)

        logger.info("starting dialog ready")

    def on50bandsPage(self):
        logger.info("Open 50band hyperspectral")
        self.done(self.OPEN_ORIGINAL_PROJECT)

    def on150bandsPage(self):
        logger.info("Open 150band hyperspectral")
        self.done(self.OPEN_PORTABLE_PROJECT)
