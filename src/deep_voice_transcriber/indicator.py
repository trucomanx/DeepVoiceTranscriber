import sys
import os
import signal
import wave
import pyaudio
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSystemTrayIcon, QMenu, QAction, QTextEdit, QLabel, QScrollArea
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import deep_voice_transcriber.lib_funcs

class AudioRecorder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.stream = None

    def initUI(self):
        width=600 
        height=300
        
        self.setWindowTitle('Audio recorder')
        #self.setGeometry(100, 100, 300, 200)
        self.resize(width, height)

        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        
        # Record button
        self.record_button = QPushButton('Record', self)
        self.record_button.clicked.connect(self.toggle_recording)
        layout.addWidget(self.record_button)
        
        
        # transcription
        self.transcription_label = QLabel(f"<b>Transcription:</b>")
        self.transcription_label.setWordWrap(True)
        self.transcription_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.transcription_label)
        
        # Create text view for displaying the message
        self.transcription_text_edit = QTextEdit()
        self.transcription_text_edit.setPlainText("")
        self.transcription_text_edit.setReadOnly(True)
        self.transcription_text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # Add text view to a scroll area
        self.transcription_scroll_area = QScrollArea()
        self.transcription_scroll_area.setWidget(self.transcription_text_edit)
        self.transcription_scroll_area.setWidgetResizable(True)
        layout.addWidget(self.transcription_scroll_area)
        
        self.setLayout(layout)

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.transcription_text_edit.setPlainText("")
        self.is_recording = True
        self.record_button.setText('Stop')
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
        self.record_button.setText('Record')
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
        
        translate=lib_funcs.deep_transcript(file_path)
        self.transcription_text_edit.setPlainText(translate)
        #print(translate)
        
        self.record_button.setEnabled(True)

class ConsultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.stream = None

    def initUI(self):
        width=600 
        height=400
        
        self.setWindowTitle('Consult')
        self.resize(width, height)

        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        
        # Record button
        self.record_button = QPushButton('Record', self)
        self.record_button.clicked.connect(self.toggle_recording)
        layout.addWidget(self.record_button)
        
        
        # transcription
        self.transcription_label = QLabel(f"<b>Transcription:</b>")
        self.transcription_label.setWordWrap(True)
        self.transcription_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.transcription_label)
        
        # Create text view for displaying the transcription
        self.transcription_text_edit = QTextEdit()
        self.transcription_text_edit.setPlainText("")
        self.transcription_text_edit.setReadOnly(True)
        self.transcription_text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # Add text view to a scroll area
        self.transcription_scroll_area = QScrollArea()
        self.transcription_scroll_area.setWidget(self.transcription_text_edit)
        self.transcription_scroll_area.setWidgetResizable(True)
        layout.addWidget(self.transcription_scroll_area)
        
        # response
        self.response_label = QLabel(f"<b>Response:</b>")
        self.response_label.setWordWrap(True)
        self.response_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(self.response_label)
        
        # Create text view for displaying the response
        self.response_text_edit = QTextEdit()
        self.response_text_edit.setPlainText("")
        self.response_text_edit.setReadOnly(True)
        self.response_text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # Add text view to a scroll area
        self.response_scroll_area = QScrollArea()
        self.response_scroll_area.setWidget(self.response_text_edit)
        self.response_scroll_area.setWidgetResizable(True)
        layout.addWidget(self.response_scroll_area)
        
        self.setLayout(layout)

    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.transcription_text_edit.setPlainText("")
        self.response_text_edit.setPlainText("")
        self.is_recording = True
        self.record_button.setText('Stop')
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
        self.record_button.setText('Record')
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
        
        translate = lib_funcs.deep_transcript(file_path)
        self.transcription_text_edit.setPlainText(translate)
        
        # Here you would process the transcription to get a response
        # For now we'll just echo the transcription
        self.response_text_edit.setPlainText("Response to: " + translate)
        
        self.record_button.setEnabled(True)

class TrayIconApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # Get base directory for icons
        base_dir_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir_path, 'icons', 'logo.png')
    
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icon_path))

        menu = QMenu()
        make_dictation_action = QAction(QIcon.fromTheme('audio-input-microphone'), 'Make Dictation', self)
        make_dictation_action.triggered.connect(self.show_audio_recorder)
        menu.addAction(make_dictation_action)
        
        make_consult_action = QAction(QIcon.fromTheme('audio-input-microphone'), 'Make Consult', self)
        make_consult_action.triggered.connect(self.show_consult_window)
        menu.addAction(make_consult_action)

        exit_action = QAction(QIcon.fromTheme('application-exit'), 'Exit', self)
        exit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(exit_action)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

    def show_audio_recorder(self):
        self.recorder = AudioRecorder()
        self.recorder.show()
        
    def show_consult_window(self):
        self.consult = ConsultWindow()
        self.consult.show()

def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL) # Aceita CTRL C para cancelar
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tray_app = TrayIconApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
