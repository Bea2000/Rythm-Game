import sys
from PyQt5.QtWidgets import QApplication
import parametros as p
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_juego import VentanaJuego, Flecha
from frontend.ventana_ranking import VentanaRanking
from backend.ventana_inicio import Inicio
from backend.ventana_juego import Juego
from frontend.ventana_resumen import VentanaResumen

def hook(type_error, traceback):
    print(type_error)
    print(traceback)

if __name__ == '__main__':
    sys.__excepthook__ = hook
    app = QApplication(sys.argv)
    ventana_inicio = VentanaInicio()
    ventana_ranking = VentanaRanking()
    ventana_juego = VentanaJuego()
    logica_inicio = Inicio()
    logica_juego = Juego()
    ventana_resumen = VentanaResumen()
    ventana_inicio.senal_validar_nombre.connect(logica_inicio.validar_nombre)
    logica_inicio.senal_resultado_validacion.connect(ventana_inicio.resultado_validacion)
    ventana_inicio.senal_ventana_ranking.connect(ventana_ranking.senal_ventana_ranking)
    ventana_ranking.senal_volver.connect(ventana_inicio.senal_volver)
    ventana_inicio.senal_ventana_juego.connect(ventana_juego.senal_ventana_juego)
    ventana_juego.senal_ventana_inicio.connect(ventana_inicio.senal_ventana_inicio)
    ventana_juego.senal_validar_inicio.connect(logica_juego.validar_inicio)
    logica_juego.senal_resultado_validacion_juego.connect(ventana_juego.resultado_validacion)
    ventana_juego.senal_ventana_resumen.connect(ventana_resumen.senal_ventana_resumen)
    ventana_resumen.senal_volver.connect(ventana_juego.senal_volver)
    ventana_juego.senal_datos.connect(ventana_resumen.cambiar_labels)
    ventana_resumen.senal_inicio.connect(ventana_inicio.senal_inicio)
    ventana_inicio.show()
    app.exec()