import sys
from PyQt5.QtWidgets import QApplication

from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setMinimumSize(640, 320)
    window.show()

    app.exec_()
