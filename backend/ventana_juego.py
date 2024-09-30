import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMessageBox)
from PyQt5.QtCore import pyqtSignal, QObject

class Juego(QObject):
    senal_validar_inicio = pyqtSignal()
    senal_resultado_validacion_juego = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        
    def validar_inicio(self, movido):
        if movido == True:
            self.senal_resultado_validacion_juego.emit(True)
        else:
            self.senal_resultado_validacion_juego.emit(False)