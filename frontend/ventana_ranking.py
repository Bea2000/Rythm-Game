import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMessageBox)
from PyQt5.QtCore import pyqtSignal

window_name, base_class = uic.loadUiType("VentanaPuntajes.ui")

class VentanaRanking(window_name, base_class):

    senal_ventana_ranking = pyqtSignal()
    senal_volver = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.senal_ventana_ranking.connect(self.show)
        self.botonvolver.clicked.connect(self.volver_inicio)
    
    def volver_inicio(self):
        self.hide()
        self.senal_volver.emit()