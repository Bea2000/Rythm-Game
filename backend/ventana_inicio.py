import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMessageBox)
from PyQt5.QtCore import pyqtSignal, QObject

class Inicio(QObject):
    senal_resultado_validacion = pyqtSignal(bool)
    senal_validar_nombre = pyqtSignal()

    def __init__(self):
        super().__init__()

    def validar_nombre(self, nombre):
        if nombre.isalnum() == False:
            self.senal_resultado_validacion.emit(False)
        else:
            self.senal_resultado_validacion.emit(True)
