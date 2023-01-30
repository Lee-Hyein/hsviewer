import argparse
import sys

from loguru import logger

from PySide6 import QtWidgets, _git_pyside_version
import qdarktheme

from app import MainWindow

__appname__ = "hsviewer"
__version__ = "0.0.2"

if __name__ == "__main__": 
    logger.info(f"{__appname__}-{__version__}")
    logger.info(f"PySide version : "\
        f"{_git_pyside_version.major_version}."\
        f"{_git_pyside_version.minor_version}")
    
    qApp = QtWidgets.QApplication(sys.argv)
    qApp.setStyleSheet(qdarktheme.load_stylesheet('dark'))
    qApp.setApplicationName(__appname__)

    window = MainWindow(
        qApp, 
        __appname__
    )
    window.setWindowTitle(__appname__)

    window.show()

    sys.exit(qApp.exec())