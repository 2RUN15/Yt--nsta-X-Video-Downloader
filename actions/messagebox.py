from PyQt6.QtWidgets import QMessageBox
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STYLE_PATH = os.path.join(BASE_DIR, "..","MainWindow","dialogstyle.qss")

with open(STYLE_PATH,"r",encoding="utf-8") as s:
    dialogstyle = s.read()

class FileChosErr(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WARNING!")
        self.setText("The File is not choosed")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Warning)
        self.setStyleSheet(dialogstyle)

class FolderPathErr(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WARNING!")
        self.setText("The folder path is not choosed")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Warning)
        self.setStyleSheet(dialogstyle)
        
class ReturnErr(QMessageBox):
    def __init__(self,error):
        self.error = error
        super().__init__()
        self.setWindowTitle("ERROR!")
        self.setText(f"{self.error}")
        self.setStandardButtons(self.StandardButton.Ok)
        self.setIcon(self.Icon.Critical)
        self.setStyleSheet(dialogstyle)
