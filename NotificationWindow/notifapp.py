from NotificationWindow.frontend import Ui_Form
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QGuiApplication

class NotificationWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.ToolTip)
        
        self.locate_screen()
        
        self.ui.yesButton.clicked.connect(self.yes_button)
        self.ui.noButton.clicked.connect(self.no_button)
        
        
    def locate_screen(self):
        screen = QGuiApplication.primaryScreen().availableGeometry()
        screen_size = self.sizeHint()
        
        x = screen.width() - screen_size.width() - 20
        y = screen.height() - screen_size.height() - 20
        
        self.move(x, y)
    
    def yes_button(self):
        self.close()
    
    def no_button(self):
        self.close()
        
    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key.Key_Return or a0.key() == Qt.Key.Key_Enter:
            self.yes_button()
        elif a0.key() == Qt.Key.Key_Escape:
            self.no_button()