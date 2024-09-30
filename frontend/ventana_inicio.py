import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMessageBox)
from PyQt5.QtCore import pyqtSignal

window_name, base_class = uic.loadUiType("VentanaInicio.ui")

class VentanaInicio(window_name, base_class):

    senal_ventana_ranking = pyqtSignal()
    senal_volver = pyqtSignal()
    senal_ventana_juego = pyqtSignal()
    senal_validar_nombre = pyqtSignal(str)
    senal_resultado_validacion = pyqtSignal()
    senal_ventana_inicio = pyqtSignal() 
    senal_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.botonranking.clicked.connect(self.abrir_ranking)
        self.botoncomenzar.clicked.connect(self.validar)
        self.senal_volver.connect(self.show)
        self.senal_ventana_inicio.connect(self.show)
        self.senal_inicio.connect(self.show)

    def abrir_ranking(self):
        self.hide()
        self.senal_ventana_ranking.emit()
    
    def validar(self):
        nombre = self.edit.text()
        self.senal_validar_nombre.emit(nombre)
    
    def resultado_validacion(self, validacion):
        if validacion == True:
            self.hide()
            self.edit.setText('')
            self.senal_ventana_juego.emit()
        else:
            self.alerta = QMessageBox()
            self.alerta.setText("Recuerda que el nombre debe ser alfanumérico")
            self.alerta.show()


if __name__ == '__main__':
    app = QApplication([])
    form = VentanaInicio()
    form.show()
    sys.exit(app.exec_())