import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowIcon(QIcon('icon.ico'))
    window.setMinimumSize(640, 320)
    window.show()

    sys.exit(app.exec())
