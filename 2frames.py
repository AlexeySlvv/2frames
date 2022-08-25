import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowIcon(QIcon('icon.ico'))
    window.setMinimumSize(640, 320)
    window.show()

    app.exec_()
