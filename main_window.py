import os
from os import path
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QSpinBox,
    QTimeEdit,
    QProgressBar,
    QStatusBar,
    QGridLayout,
    QFileDialog,
)

from PyQt5.QtCore import Qt, QTime

from opencv_frames import get_video_info, save_frames


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2frames")
        self.init_ui()
        self.init_layout()


    def init_ui(self):
        align_center = Qt.AlignmentFlag.AlignHCenter \
                       | Qt.AlignmentFlag.AlignVCenter

        # open video
        self.open_video_btn = QPushButton("Open video")
        self.open_video_btn.clicked.connect(self.on_open_video_clicked)
        self.open_video_ledit = QLineEdit()
        self.open_video_ledit.setReadOnly(True)
        self.open_video_ledit.textChanged.connect(self.on_text_changed)

        # open folder
        self.open_folder_btn = QPushButton("Select folder")
        self.open_folder_btn.setEnabled(False)
        self.open_folder_btn.clicked.connect(self.on_open_folder_clicked)
        self.open_folder_ledit = QLineEdit()
        self.open_folder_ledit.setReadOnly(True)
        self.open_folder_ledit.textChanged.connect(self.on_text_changed)
        
        # step
        self.step_label1 = QLabel("Save every")
        self.step_label1.setAlignment(align_center)
        self.step_sbox = QSpinBox()
        self.step_sbox.setMinimum(1)
        self.step_sbox.setMaximum(1000)
        self.step_sbox.setValue(2)
        self.step_label2 = QLabel("frame")
        self.step_label2.setAlignment(align_center)

        # from-to
        self.from_label = QLabel("From")
        self.from_label.setAlignment(align_center)
        self.from_tedit = QTimeEdit()
        self.from_tedit.setDisplayFormat("HH:mm:ss.zzz")
        self.to_label = QLabel("to")
        self.to_label.setAlignment(align_center)
        self.to_tedit = QTimeEdit()
        self.to_tedit.setDisplayFormat("HH:mm:ss.zzz")

        # start
        self.start_btn = QPushButton("Start")
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.on_start_clicked)
        self.progress_bar = QProgressBar()
        self.progress_label = QLabel("Hello! Choose a video first")
        self.progress_label.setAlignment(align_center)

        # quit
        self.quit_btn = QPushButton("Quit")
        self.quit_btn.clicked.connect(self.on_quit_clicked)

        # status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("QStatusBar::item {border: None;}")
        self.status_bar.addWidget(self.progress_label)

    def init_layout(self):
        # grid
        layout = QGridLayout()
        
        layout.addWidget(self.open_video_btn, 0, 0)
        layout.addWidget(self.open_video_ledit, 0, 1, 1, 3)

        layout.addWidget(self.open_folder_btn, 1, 0)
        layout.addWidget(self.open_folder_ledit, 1, 1, 1, 3)

        layout.addWidget(self.step_label1, 2, 0)
        layout.addWidget(self.step_sbox, 2, 1, 1, 2)
        layout.addWidget(self.step_label2, 2, 3)

        layout.addWidget(self.from_label, 3, 0)
        layout.addWidget(self.from_tedit, 3, 1)
        layout.addWidget(self.to_label, 3, 2)
        layout.addWidget(self.to_tedit, 3, 3)

        layout.addWidget(self.start_btn, 4, 0)
        layout.addWidget(self.progress_bar, 4, 1, 1, 3)

        layout.addWidget(self.quit_btn, 5, 3)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setStatusBar(self.status_bar)


    def on_open_video_clicked(self):
        filter = "Videos (*.mkv *.mp4 *.avi *.webm)"
        filename, _ = QFileDialog.getOpenFileName(self, filter=filter)
        if filename:
            dirname = path.dirname(filename)
            onlyname = path.splitext(filename)[0]
            self._set_folder_path(folder_path=path.join(dirname, onlyname))
            # from - to
            self.open_video_ledit.setText(filename)
            frame_count, duration = get_video_info(filename)
            self.progress_bar.setMaximum(frame_count)
            dur = int(duration)
            h, m, s = dur // 3600, dur // 60, dur % 60
            ms = (duration * 1000)  % 1000
            max_time = QTime(h, m, s, ms)
            self.from_tedit.setMaximumTime(max_time)
            self.from_tedit.setTime(QTime(0,0))
            self.to_tedit.setMaximumTime(max_time)
            self.to_tedit.setTime(max_time)

    def _set_folder_path(self, folder_path: str()):
        if folder_path:
            self.open_folder_ledit.setText(folder_path)
        
    def on_open_folder_clicked(self):
        directory = self.open_folder_ledit.text() if self.open_folder_ledit.text() else os.getcwd()
        folder_path = QFileDialog.getExistingDirectory(self, directory=directory)
        self._set_folder_path(folder_path=folder_path)

    def set_progress(self, value: int):
        self.progress_label.setText(f"frame {value+1}")
        self.progress_bar.setValue(value)
        QApplication.processEvents()

    def on_start_clicked(self):
        Path(self.open_folder_ledit.text()).mkdir(parents=True, exist_ok=True)
        param = {
            'file_name': self.open_video_ledit.text(),
            'folder_name': self.open_folder_ledit.text(),
            'step': self.step_sbox.value(),
            'from': QTime(0, 0).msecsTo(self.from_tedit.time()),
            'to': QTime(0, 0).msecsTo(self.to_tedit.time()),
        }
        if not save_frames(param=param, set_progress=self.set_progress):
            self.progress_label.setText("Error saving frames")
        else:
            self.progress_label.setText("Done")

    def on_text_changed(self):
        if self.open_video_ledit.text():
            self.progress_label.setText("Choose a folder to save frames or press 'Start' to start process")
        else:
            self.progress_label.setText("Choose a video")
        self.open_folder_btn.setEnabled(bool(self.open_video_ledit.text()))
        self.start_btn.setEnabled(bool(self.open_video_ledit.text()) and bool(self.open_folder_ledit.text()))

    def on_quit_clicked(self):
        QApplication.quit()
