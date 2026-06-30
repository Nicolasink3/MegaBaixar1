
try:
    from PyQt5.QtWidgets import (
        QWidget,
        QLabel,
        QPushButton,
        QVBoxLayout,
        QProgressBar
    )
except ImportError:
    from PySide2.QtWidgets import (
        QWidget,
        QLabel,
        QPushButton,
        QVBoxLayout,
        QProgressBar
    )

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Game Downloader")
        self.resize(1000, 700)

        self.busca = QLineEdit()
        self.busca.setPlaceholderText("Pesquisar jogo")

        self.btn_buscar = QPushButton("Buscar")

        top = QHBoxLayout()
        top.addWidget(self.busca)
        top.addWidget(self.btn_buscar)

        self.lista = QVBoxLayout()

        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addLayout(self.lista)

        self.setLayout(layout)