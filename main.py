from MainWindow.mainwindowui import Ui_MainWindow
import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from actions.dialogs import chose_file, chose_folder
from actions.process import FileFormatView, DownloadWideo, DownloadAuido
from actions.messagebox import FileChosErr, FolderPathErr, ReturnErr
from packagevalues import vidoe_settings, auido_settings
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STYLE_PATH = os.path.join(BASE_DIR,"MainWindow","style.qss")

class MainMindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #None Values
        self.file_path = None
        self.folder_path = None
        self.file_format = None
        self.file_name = None
        self.file_quality = None
        self.worker_video = None
        self.worker_audio = None
        self.errortext = None
        
        #Buttons
        self.ui.chosfilebutton.clicked.connect(self.file_btn)
        self.ui.chosfoldbuttoon.clicked.connect(self.folder_btn)
        self.ui.startbutton.clicked.connect(self.startbutton)
        self.ui.formatwievbutton.clicked.connect(self.formatbutton)
        self.ui.file_formatbox.currentTextChanged.connect(self.formatboxedited)
        
        #MessageBox
        self.filechoserr = FileChosErr()
        self.foldererr = FolderPathErr()
    
    def startbutton(self):
        try:
            if self.ui.startbutton.text() == "STOP":
                return self.stop_button()

            self.ui.logtext.clear()

            self.file_format = self.ui.file_formatbox.currentText()
            self.file_format = self.file_format.lower()
            self.file_quality = self.ui.file_quailitybox.currentText()
            self.file_path = self.ui.target_url.text()
            self.folder_path = self.ui.target_folder.text()
            self.file_name = self.ui.filename.text()
            
            if self.file_path is None or not self.file_path:
                return self.filechoserr.exec()

            if self.folder_path is None or not self.folder_path:
                return self.foldererr.exec()
            
            if self.file_format == "mp3" or self.file_format == "FLAC" or self.file_format == "WAV":
                return self.auido_download()
            
            values = vidoe_settings(
                video_format=self.file_format,
                video_quality=self.file_quality[:-1],
                file_path=self.folder_path,
                video_url=self.file_path,
                file_name= self.file_name
            )
            
            self.ui.chosfilebutton.setEnabled(False)
            self.ui.chosfoldbuttoon.setEnabled(False)
            self.ui.file_formatbox.setEnabled(False)
            self.ui.file_quailitybox.setEnabled(False)
            self.ui.formatwievbutton.setEnabled(False)
            
            self.worker_video = DownloadWideo(values)
            self.worker_video.start()
            self.ui.startbutton.setText("STOP")
            
            self.worker_video.log_text.connect(lambda text: self.ui.logtext.append(text))
            self.worker_video.error.connect(lambda text: self.ui.logtext.append(text))
            self.worker_video.finished.connect(self.finishedworker)
        except Exception as e:
            returnerr = ReturnErr(e)
            return returnerr.exec()
    
    def finishedworker(self):
        self.ui.startbutton.setText("START")
        self.ui.chosfilebutton.setEnabled(True)
        self.ui.chosfoldbuttoon.setEnabled(True)
        self.ui.file_formatbox.setEnabled(True)
        self.ui.file_quailitybox.setEnabled(True)
        self.ui.formatwievbutton.setEnabled(True)        
    
    def auido_download(self):
        values = auido_settings(
            auido_format=self.file_format,
            file_path=self.folder_path,
            video_url=self.file_path,
            file_name=self.file_name
        )
        self.worker_audio = DownloadAuido(values)
        
        self.worker_audio.start()
        self.ui.startbutton.setText("STOP")
        
        self.worker_audio.log_text.connect(lambda text: self.ui.logtext.append(text))
        self.worker_audio.error.connect(lambda text: self.ui.logtext.append(text))
        self.worker_audio.finished.connect(lambda: self.ui.startbutton.setText("START"))
    
    def stop_button(self):
        try:
            if self.worker_video and self.worker_video.isRunning():
                self.worker_video.stop()
                self.ui.startbutton.setText("START")
            if self.worker_audio and self.worker_audio.isRunning():
                self.worker_audio.stop()
                self.ui.startbutton.setText("START")
        except Exception as e:
            returnerr = ReturnErr(e)
            return returnerr.exec()
            
    def formatbutton(self):
        try:
            self.ui.logtext.clear()
            url = self.ui.target_url.text()
            self.worker_view = FileFormatView(url)
            self.worker_view.start()
            
            self.worker_view.log_text.connect(lambda text: self.ui.logtext.append(text))
        except Exception as e:
            returnerr = ReturnErr(e)
            return returnerr.exec()
    
    def file_btn(self):
        try:
            self.file_path = chose_file(self)
            self.ui.target_url.setText(self.file_path)
        except Exception as e:
            returnerr = ReturnErr(e)
            return returnerr.exec()
    
    def folder_btn(self):
        try:
            self.folder_path = chose_folder(self)
            self.ui.target_folder.setText(self.folder_path)
        except Exception as e:
            returnerr = ReturnErr(e)
            return returnerr.exec()
    
    def formatboxedited(self):
        self.file_format = self.ui.file_formatbox.currentText()
        if self.file_format == "mp3" or self.file_format == "FLAC" or self.file_format == "WAV":
            return self.ui.file_quailitybox.hide()
        return self.ui.file_quailitybox.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open(STYLE_PATH,"r",encoding="utf-8") as f:
        style = f.read()
    window = MainMindow()
    window.setStyleSheet(style)
    window.show()
    sys.exit(app.exec())