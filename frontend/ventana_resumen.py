import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMessageBox)
from PyQt5.QtCore import pyqtSignal

window_name, base_class = uic.loadUiType("VentanaResumen.ui")

class VentanaResumen(window_name, base_class):

    senal_ventana_resumen = pyqtSignal()
    senal_volver = pyqtSignal()
    senal_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.senal_ventana_resumen.connect(self.show)
        self.aprueba = None
        self.boton_volver.clicked.connect(self.volver)

    def cambiar_labels(self, pte, pteA, combo, pasos_fallados, aprob, nivel):
        self.dato1.setText(f'{pte}')
        self.dato2.setText(f'{pteA}')
        self.dato3.setText(f'{combo}')
        self.dato4.setText(f'{pasos_fallados}')
        self.dato5.setText(f'{aprob}')
        self.aprueba = self.revisar_aprobacion(aprob)
    
    def revisar_aprobacion(self, aprob):
        if aprob == 100:
            return True
        else:
            return False

    def volver(self):
        self.hide()
        if self.aprueba == True:
            self.senal_volver.emit()
        elif self.aprueba == False:
            self.senal_inicio.emit()