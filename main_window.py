import os

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


    def init_ui(self):
        align_center = Qt.AlignmentFlag.AlignHCenter \
            | Qt.AlignmentFlag.AlignVCenter

        # open video
        self.open_video_btn = QPushButton("Open video")
        self.open_video_btn.clicked.connect(self.on_open_video_clicked)
        self.open_video_edit = QLineEdit()

        # open folder
        self.open_folder_btn = QPushButton("Select folder")
        self.open_folder_btn.clicked.connect(self.on_open_folder_clicked)
        self.open_folder_edit = QLineEdit()
        
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
        self.start_btn.clicked.connect(self.on_start_clicked)
        self.progress_bar = QProgressBar()
        self.progress_label = QLabel()
        self.progress_label.setAlignment(align_center)

        # quit
        self.quit_btn = QPushButton("Quit")
        self.quit_btn.clicked.connect(self.on_quit_clicked)

        # grid
        layout = QGridLayout()
        
        layout.addWidget(self.open_video_btn, 0, 0)
        layout.addWidget(self.open_video_edit, 0, 1, 1, 3)

        layout.addWidget(self.open_folder_btn, 1, 0)
        layout.addWidget(self.open_folder_edit, 1, 1, 1, 3)

        layout.addWidget(self.step_label1, 2, 0)
        layout.addWidget(self.step_sbox, 2, 1, 1, 2)
        layout.addWidget(self.step_label2, 2, 3)

        layout.addWidget(self.from_label, 3, 0)
        layout.addWidget(self.from_tedit, 3, 1)
        layout.addWidget(self.to_label, 3, 2)
        layout.addWidget(self.to_tedit, 3, 3)

        layout.addWidget(self.start_btn, 4, 0)
        layout.addWidget(self.progress_bar, 4, 1, 1, 3)

        layout.addWidget(self.progress_label, 5, 1)
        layout.addWidget(self.quit_btn, 5, 3)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def on_open_video_clicked(self):       
        filter = "Videos (*.mkv *.mp4 *.avi *.webm)"
        filename, _ = QFileDialog.getOpenFileName(self, filter=filter)
        if filename:
            self.open_video_edit.setText(filename)
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
            if not self.open_folder_edit.text():
                self.open_folder_edit.setText(os.path.dirname(filename))

    def on_open_folder_clicked(self):
        directory = self.open_folder_edit.text() if self.open_folder_edit.text() else os.getcwd()
        folder_path = QFileDialog.getExistingDirectory(self, directory=directory)
        if folder_path:
            self.open_folder_edit.setText(folder_path)

    def set_progress(self, value: int):
        self.progress_label.setText(f"frame {value}")
        self.progress_bar.setValue(value)
        QApplication.processEvents()

    def on_start_clicked(self):
        param = {
            'file_name': self.open_video_edit.text(),
            'folder_name': self.open_folder_edit.text(),
            'step': self.step_sbox.value(),
            'from': QTime(0, 0).msecsTo(self.from_tedit.time()),
            'to': QTime(0, 0).msecsTo(self.to_tedit.time()),
        }
        if not save_frames(param=param, set_progress=self.set_progress):
            self.progress_label.setText("Error")
        else:
            self.progress_label.setText("Done")

    def on_quit_clicked(self):
        QApplication.quit()
