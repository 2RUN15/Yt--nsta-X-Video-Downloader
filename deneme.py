import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication

class BildirimEkrani(QWidget):
    def __init__(self, mesaj):
        super().__init__()
        
        # Pencere çerçevesini kaldırıp, her zaman en üstte durmasını sağlıyoruz
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.ToolTip)
        
        # Basit bir tasarım (koyu arka plan, beyaz yazı)
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
                border-radius: 8px;
                border: 1px solid #555;
            }
            QPushButton {
                background-color: #444;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)

        # Arayüz elemanları
        layout = QVBoxLayout()
        self.etiket = QLabel(mesaj)
        layout.addWidget(self.etiket)

        buton_layout = QHBoxLayout()
        self.evet_buton = QPushButton("Evet")
        self.hayir_buton = QPushButton("Hayır")

        buton_layout.addWidget(self.evet_buton)
        buton_layout.addWidget(self.hayir_buton)
        layout.addLayout(buton_layout)
        
        self.setLayout(layout)

        # Buton tıklama olayları
        self.evet_buton.clicked.connect(self.kabul_edildi)
        self.hayir_buton.clicked.connect(self.reddedildi)

        self.ekranda_konumlandir()

    def ekranda_konumlandir(self):
        # Ekran boyutunu alıp pencereyi sağ alt köşeye hizalıyoruz
        ekran = QGuiApplication.primaryScreen().availableGeometry()
        pencere_boyutu = self.sizeHint()
        
        x = ekran.width() - pencere_boyutu.width() - 20  # Sağdan 20 piksel boşluk
        y = ekran.height() - pencere_boyutu.height() - 20 # Alttan 20 piksel boşluk
        
        self.move(x, y)

    def kabul_edildi(self):
        print("İndirme işlemi arka planda başlatıldı...")
        self.close()

    def reddedildi(self):
        print("İndirme iptal edildi.")
        self.close()

# Test etmek için ana uygulama
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Bildirim penceresini doğrudan çağırıyoruz
    bildirim = BildirimEkrani("Bu videoyu indirmek istiyor musunuz?")
    bildirim.show()
    
    sys.exit(app.exec())