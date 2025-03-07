import sys
import os
import wave
import pyaudio
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon

class AudioRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.stream = None

    def initUI(self):
        self.setWindowTitle('Gravador de Áudio')
        self.setGeometry(100, 100, 300, 200)

        self.record_button = QPushButton('Gravar', self)
        self.record_button.clicked.connect(self.toggle_recording)

        layout = QVBoxLayout()
        layout.addWidget(self.record_button)
        self.setLayout(layout)

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.is_recording = True
        self.record_button.setText('Parar')
        self.frames = []
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                     channels=1,
                                     rate=44100,
                                     input=True,
                                     frames_per_buffer=1024)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def update(self):
        if self.is_recording:
            data = self.stream.read(1024, exception_on_overflow=False)
            self.frames.append(data)

    def stop_recording(self):
        self.record_button.setEnabled(False)
        self.is_recording = False
        self.record_button.setText('Gravar')
        self.timer.stop()

        while self.stream.get_read_available() > 0:
            data = self.stream.read(1024, exception_on_overflow=False)
            self.frames.append(data)

        self.stream.stop_stream()
        self.stream.close()

        home_dir = os.path.expanduser("~")
        file_path = os.path.join(home_dir, "gravacao.wav")

        wf = wave.open(file_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        print(f"Gravação salva em {file_path}")
        self.record_button.setEnabled(True)

class TrayIconApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon.fromTheme('audio-card'))

        menu = QMenu()
        make_dictation_action = QAction(QIcon.fromTheme('audio-input-microphone'), 'Make Dictation', self)
        make_dictation_action.triggered.connect(self.show_audio_recorder)
        menu.addAction(make_dictation_action)

        exit_action = QAction(QIcon.fromTheme('application-exit'), 'Exit', self)
        exit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(exit_action)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def show_audio_recorder(self):
        self.recorder = AudioRecorder()
        self.recorder.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tray_app = TrayIconApp()
    sys.exit(app.exec_())
