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


class GameCard(QWidget):

    def __init__(self, jogo):
        super().__init__()

        self.jogo = jogo

        self.nome = QLabel(jogo["titulo"])
        self.progresso = QProgressBar()

        self.btn_download = QPushButton("Baixar")

        layout = QVBoxLayout()

        layout.addWidget(self.nome)
        layout.addWidget(self.progresso)
        layout.addWidget(self.btn_download)

        self.setLayout(layout)