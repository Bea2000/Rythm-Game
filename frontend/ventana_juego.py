import os
import sys
from PyQt5 import uic
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QMessageBox, QComboBox, QProgressBar
from PyQt5.QtCore import pyqtSignal, Qt, QMimeData, QPoint, QPointF, QEvent, QThread, QObject, QTimer, QEventLoop, QTime
from PyQt5.QtGui import QDrag, QPixmap
import parametros as p
import random
from time import sleep

window_name, base_class = uic.loadUiType("VentanaJuego.ui")
window_name1, base_class1 = uic.loadUiType("VentanaResumen.ui")

class VentanaJuego(window_name, base_class):

    senal_ventana_juego = pyqtSignal()
    senal_ventana_inicio = pyqtSignal()
    senal_validar_inicio = pyqtSignal(bool)
    senal_resultado_validacion = pyqtSignal()
    senal_ventana_resumen = pyqtSignal()
    senal_volver = pyqtSignal()
    senal_datos = pyqtSignal(int, int, int, int, int, int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.senal_ventana_juego.connect(self.show)
        self.boton_salir.clicked.connect(self.salir)
        self.senal_volver.connect(self.show)
        self.pin_rojo = Pinguino(self, os.path.join("sprites", "pinguirin_rojo", "rojo_neutro.png"))
        self.pin_rojo.setGeometry(*p.POS_PIN_R, p.ALTO_PIN, p.ANCHO_PIN)
        self.pin_verde = Pinguino(self, os.path.join("sprites", "pinguirin_verde", "verde_neutro.png"))
        self.pin_verde.setGeometry(*p.POS_PIN_V, p.ALTO_PIN, p.ANCHO_PIN)
        self.pin_celeste = Pinguino(self, os.path.join("sprites", "pinguirin_celeste", "celeste_neutro.png"))
        self.pin_celeste.setGeometry(*p.POS_PIN_C, p.ALTO_PIN, p.ANCHO_PIN)
        self.pin_morado = Pinguino(self, os.path.join("sprites", "pinguirin_morado", "morado_neutro.png"))
        self.pin_morado.setGeometry(*p.POS_PIN_M, p.ALTO_PIN, p.ANCHO_PIN)
        self.pin_amarillo = Pinguino(self, os.path.join("sprites", "pinguirin_amarillo", "amarillo_neutro.png"))
        self.pin_amarillo.setGeometry(*p.POS_PIN_A, p.ALTO_PIN, p.ANCHO_PIN)
        self.movido = False
        self.mover = None
        self.movido_rojo = False
        self.movido_celeste = False
        self.movido_amarillo = False
        self.movido_verde = False
        self.movido_morado = False
        self.cumbia_1 = QSound(os.path.join("songs","cancion_1.wav"), self)
        self.cumbia_2 = QSound(os.path.join("songs","cancion_2.wav"), self)
        self.flecha_down = ['down_1.png', 'down_2.png','down_3.png', 'down_5.png']
        self.flecha_up = ['up_1.png', 'up_2.png', 'up_3.png', 'up_5.png']
        self.flecha_izq = ['left_1.png', 'left_2.png','left_3.png', 'left_5.png']
        self.flecha_der = ['right_1.png', 'right_2.png', 'right_3.png', 'right_5.png']
        self.dinero = p.DINERO_INICIAL
        self.actualizar_dinero(self.dinero)
        self.op_flechas = [self.flecha_izq, self.flecha_up, self.flecha_down, self.flecha_der]
        self.pos_flechas = [p.POS_FLECHA_1, p.POS_FLECHA_2, p.POS_FLECHA_3, p.POS_FLECHA_4]
        self.setAcceptDrops(True)
        self.defaultWindowFlags = self.windowFlags()
        self.pinguinos = [self.pin_rojo, self.pin_verde, self.pin_morado, self.pin_amarillo, self.pin_celeste]
        self.juego = False
        self.flechas = []
        self.boton_comenzar.clicked.connect(self.validar_inicio)
        self.nivel = None
        self.hielo_activado = False
        self.timer_hielo = QTime()
        self.puntaje_ronda = 0
        self.timer_partida = QTime()
        self.pasos_realizados = 0
        self.pasos_fallados = 0
        self.porcentaje_aprob = 0
        self.puntaje_acumulado = 0
        self.combo = 0
        self.max_combo = 0


    def sleep(self, segundos):
        loop = QEventLoop()
        QTimer.singleShot(int(segundos*1000), loop.quit)
        loop.exec_()

    def salir(self):
        #se deben incluir puntajes
        self.cumbia_1.stop()
        self.cumbia_2.stop()
        self.hide()
        self.resetear_ventana()
        self.actualizar_valor_pin(p.DINERO_INICIAL)
        self.senal_ventana_inicio.emit()
        self.puntaje_acumulado = 0
    
    def dragEnterEvent(self, e):
        #se debe evitar colisiones tambien
        if self.movido == False or self.dinero >= p.PRECIO_PINGUIRIN:
                    e.accept()
        for pin in self.pinguinos:
            if e.pos().x() >= pin.x() and e.pos().x() <= pin.x() + pin.width():
                if e.pos().y() >= pin.y() and e.pos().y() <= pin.y() + pin.height():
                    self.mover = pin

    def dropEvent(self, e):
        pos = [e.pos().x()-45, e.pos().y()-40] #centrar eje de movimiento
        if pos[0] > p.LIMITE_X_IZQ and pos[0] < p.LIMITE_X_DER:
            if pos[1] > p.LIMITE_Y_UP and pos[1] < p.LIMITE_Y_DOWN:
                e.accept()
                e.setDropAction(Qt.MoveAction)
                print("movere",self.mover)
                self.mover.move(pos[0],pos[1])
                if self.movido == False:
                    self.movido = True
                    self.actualizar_valor_pin(p.PRECIO_PINGUIRIN)
                else:
                    self.dinero = self.dinero - p.PRECIO_PINGUIRIN
                    self.actualizar_dinero(self.dinero)
                if self.mover == self.pin_rojo:
                    self.movido_rojo = True
                elif self.mover == self.pin_amarillo:
                    self.movido_amarillo = True
                elif self.mover == self.pin_celeste:
                    self.movido_celeste = True
                elif self.mover == self.pin_morado:
                    self.movido_morado = True
                elif self.mover == self.pin_verde:
                    self.movido_verde = True
    
    def actualizar_valor_pin(self, valor):
        self.label_valorpin.setText(f'Valor pinguino: ${valor}')
    
    def actualizar_dinero(self, dinero):
        self.label_dinero.setText(f'Dinero ${dinero}')
    
    def validar_inicio(self):
        self.senal_validar_inicio.emit(self.movido)
    
    def resultado_validacion(self, resultado):
        if resultado == True:
            self.comenzar_juego()
        else:
            self.alerta = QMessageBox()
            self.alerta.setText("Debes mover a tu pinguino a la pista de baile")
            self.alerta.show()

    def resetear_ventana(self):
        self.pin_rojo.setGeometry(*p.POS_PIN_R, p.ALTO_PIN, p.ANCHO_PIN)
        self.pin_verde.setGeometry(*p.POS_PIN_V, p.ALTO_PIN, p.ANCHO_PIN)
        self.pin_celeste.setGeometry(*p.POS_PIN_C, p.ALTO_PIN, p.ANCHO_PIN)
        self.pin_morado.setGeometry(*p.POS_PIN_M, p.ALTO_PIN, p.ANCHO_PIN)
        self.pin_amarillo.setGeometry(*p.POS_PIN_A, p.ALTO_PIN, p.ANCHO_PIN)
        self.movido = False
        self.movido_rojo = False
        self.movido_amarillo = False
        self.movido_celeste = False
        self.movido_verde = False
        self.movido_morado = False
        self.pin_inicial = False
        self.dinero = 0
        self.juego = False
        self.boton_comenzar.setEnabled(True)
        self.opcion_songs.setEnabled(True)
        self.opcion_dif.setEnabled(True)
        for flecha in self.flechas:
            flecha.flecha.hide()
        self.flechas = []
        self.pasos_realizados = 0
        self.pasos_fallados = 0
        self.hielo_activado = False
        self.puntaje_ronda = 0
        self.porcentaje_aprob = 0
        self.progreso_apruebo.reset()
        self.progreso_prog.reset()

    def calcular_aprobacion(self):
        pasos_totales = self.pasos_fallados + self.pasos_realizados
        aprobacion = 100 * (self.pasos_realizados - self.pasos_fallados)/pasos_totales
        return aprobacion
    
    def comenzar_juego(self):
        self.juego = True
        self.boton_comenzar.setEnabled(False)
        self.opcion_songs.setEnabled(False)
        self.opcion_dif.setEnabled(False)
        self.poner_musica()
        self.timer = QTimer()
        if self.opcion_dif.currentText() == 'Principiante':
            self.opcion_principiante()
        elif self.opcion_dif.currentText() == 'Aficionado':
            self.opcion_aficionado()
        elif self.opcion_dif.currentText() == 'Maestro Cumbia':
            self.opcion_maestro_cumbia()
        self.juego = False
        self.puntaje_acumulado = self.puntaje_ronda
        self.cumbia_1.stop()
        self.cumbia_2.stop()
        self.hide()
        var = [self.puntaje_ronda, self.puntaje_acumulado, self.max_combo, self.pasos_fallados]
        if self.porcentaje_aprob > 100:
            self.porcentaje_aprob = 100
        var.append(self.porcentaje_aprob)
        var.append(self.nivel)
        self.senal_ventana_resumen.emit()
        self.senal_datos.emit(var[0], var[1], var[2], var[3], var[4], var[5])
        self.puntaje_ronda = 0
        self.resetear_ventana()
    
    def opcion_principiante(self):
        self.nivel = 'principiante'
        duracion = p.DURACION_PRIN
        intervalo_flechas = p.TIEMPO_ENTRE_FLECHAS_PRIN
        self.crear_flechas(intervalo_flechas, duracion)

    def opcion_aficionado(self):
        self.nivel = 'aficionado'
        duracion = p.DURACION_AFI
        intervalo_flechas = p.TIEMPO_ENTRE_FLECHAS_AFI
        self.crear_flechas(intervalo_flechas, duracion)

    def opcion_maestro_cumbia(self):
        self.nivel = 'maestro'
        duracion = p.DURACION_MAES
        intervalo_flechas = p.TIEMPO_ENTRE_FLECHAS_MAES
        self.crear_flechas(intervalo_flechas, duracion)

    def poner_musica(self):
        if self.opcion_songs.currentText() == 'Cumbia 1':
            self.cumbia_1.play()
        elif self.opcion_songs.currentText() == 'Cumbia 2':
            self.cumbia_2.play()
    
    def crear_flechas(self, intervalos, duracion):
        self.timer_partida.start()
        duracion_hielo = duracion*1000*p.POND_DURACION_FLECHA_HIELO
        while self.timer_partida.elapsed() < duracion*1000:
            porcentaje_transcurso = (self.timer_partida.elapsed()*100)/(duracion*1000)
            self.progreso_prog.setValue(int(porcentaje_transcurso))
            self.label_dir.raise_()
            elegir = self.elegir_flecha()
            eleccion = elegir[0]
            posx = self.pos_flechas[elegir[1]]
            posx2 = posx
            posx3 = posx
            if self.hielo_activado == True:
                flecha = Flecha(self, eleccion, posx, 3)
            else:
                flecha = Flecha(self, eleccion, posx, elegir[2])
            flecha.senal_paso_no_efectuado.connect(self.aumentar_fallo)
            flecha.senal_mover_flecha.connect(self.mover_flecha)
            self.flechas.append(flecha)
            triple = self.triple_flecha()
            doble = self.doble_flecha()
            if triple == True:
                while posx == posx2:
                    pos2 = random.randint(0,3)
                    posx2 = self.pos_flechas[pos2]
                    dir_flecha2 = self.op_flechas[pos2]
                    eleccion2 = dir_flecha2[elegir[2]]
                    if self.hielo_activado == True:
                        flecha2 = Flecha(self, eleccion2, posx2, 3)
                    else:
                        flecha2 = Flecha(self, eleccion2, posx2, elegir[2])
                    flecha2.senal_paso_no_efectuado.connect(self.aumentar_fallo)
                    flecha2.senal_mover_flecha.connect(self.mover_flecha)
                    self.flechas.append(flecha2)
                while posx == posx3:
                    pos3 = random.randint(0,3)
                    posx3 = self.pos_flechas[pos3]
                    dir_flecha3 = self.op_flechas[pos3]
                    eleccion3 = dir_flecha3[elegir[2]]
                    if self.hielo_activado == True:
                        flecha3 = Flecha(self, eleccion3, posx3, elegir[2])
                    else:
                        flecha3 = Flecha(self, eleccion3, posx3, 3)
                    flecha3.senal_paso_no_efectuado.connect(self.aumentar_fallo)
                    flecha3.senal_mover_flecha.connect(self.mover_flecha)
                    self.flechas.append(flecha3)
            if triple == False and doble == True:
                while posx == posx2:
                    pos2 = random.randint(0,3)
                    posx2 = self.pos_flechas[pos2]
                    dir_flecha2 = self.op_flechas[pos2]
                    eleccion2 = dir_flecha2[elegir[2]]
                    if self.hielo_activado == True:
                        flecha2 = Flecha(self, eleccion2, posx2, 3)
                    else:
                        flecha2 = Flecha(self, eleccion2, posx2, elegir[2])
                    flecha2.senal_paso_no_efectuado.connect(self.aumentar_fallo)
                    flecha2.senal_mover_flecha.connect(self.mover_flecha)
                    self.flechas.append(flecha2)
            if elegir[2] == 3:
                self.hielo_activado = True
                for flecha in self.flechas:
                    flecha.hielo = True
                self.timer_hielo.start()
            if self.timer_hielo.elapsed() >= duracion_hielo:
                self.hielo_activado = False
                for flecha in self.flechas:
                    flecha.hielo = False
            self.sleep(intervalos)
        for flecha in self.flechas:
            flecha.flecha.hide()
        self.progreso_prog.setValue(100)
    
    def aumentar_fallo(self):
        self.pasos_fallados += 1
        self.combo = 0
        self.label_combo.setText('Combo: x0')

    def doble_flecha(self):
        prob = random.random()
        if prob <= p.PROB_DOS_FLECHAS and self.nivel != 'principiante':
            return True
        else:
            return False

    def triple_flecha(self):
        prob = random.random()
        if prob <= p.PROB_TRES_FLECHAS and self.nivel == 'maestro':
            return True
        else:
            return False
    
    def mover_flecha(self, label, pos):
        label.move(*pos)
    
    def elegir_flecha(self):
        pos = random.randint(0,3)
        dir_flecha = self.op_flechas[pos]
        op = random.random()
        normal = p.P_NORMAL
        gold = normal + p.P_FLECHA_GOLD
        x2 = gold + p.P_FLECHA_X2
        if op >= 0 and op <= p.P_NORMAL:
            eleccion = dir_flecha[0]
            tipo_flecha = 0
        elif op > normal and op <= gold:
            eleccion = dir_flecha[1]
            tipo_flecha = 1
        elif op > gold and op <= x2:
            eleccion = dir_flecha[2]
            tipo_flecha = 2
        elif op > x2 and op <= 1:
            eleccion = dir_flecha[3]
            tipo_flecha = 3
        return [eleccion, pos, tipo_flecha]
    
    def revisar_colision(self, label1, label2):
        pos_inf = label2.y() - label2.height()
        pos_sup = label2.y() + label2.height()
        if label1.y() > pos_inf and label1.y() < pos_sup:
            return True
        else:
            return False

    def keyPressEvent(self, event):
        #falta hacer para casos de dobles y triples
        revisado = False
        if event.text() == 'w' and self.juego == True:
            self.cambiar_color(self.zona_arriba, 'rgb(153,255,255)')
            for flecha in self.flechas:
                if revisado == False:
                    if self.revisar_colision(flecha.flecha, self.zona_arriba) == True:
                        self.aumentar_puntaje(flecha)
                        self.bailar('arriba')
                        revisado = True
                        flecha.paso_hecho = True
                        self.flechas.remove(flecha)
                        self.pasos_realizados += 1
                        self.actualizar_aprobacion()
                    elif self.revisar_colision(flecha.flecha, self.zona_arriba) == False:
                        self.aumentar_fallo()
                        revisado = True

        if event.text() == 'a' and self.juego == True:
            self.cambiar_color(self.zona_izq, 'rgb(153,255,255)')
            for flecha in self.flechas:
                if revisado == False:
                    if self.revisar_colision(flecha.flecha, self.zona_izq) == True:
                        self.aumentar_puntaje(flecha)
                        revisado = True
                        self.bailar('izquierda')
                        flecha.paso_hecho = True
                        self.flechas.remove(flecha)
                        self.pasos_realizados += 1
                        self.actualizar_aprobacion()
                    elif self.revisar_colision(flecha.flecha,self.zona_izq) == False:
                        self.aumentar_fallo()
                        revisado = True

        if event.text() == 'd' and self.juego == True:
            self.cambiar_color(self.zona_der, 'rgb(153,255,255)')
            for flecha in self.flechas:
                if revisado == False:
                    if self.revisar_colision(flecha.flecha, self.zona_der) == True:
                        self.aumentar_puntaje(flecha)
                        self.bailar('derecha')
                        revisado = True
                        flecha.paso_hecho = True
                        self.flechas.remove(flecha)
                        self.pasos_realizados += 1
                        self.actualizar_aprobacion()
                    elif self.revisar_colision(flecha.flecha, self.zona_der) == False:
                        self.aumentar_fallo()
                        revisado = True

        if event.text() == 's' and self.juego == True:
            self.cambiar_color(self.zona_abajo, 'rgb(153,255,255)')
            for flecha in self.flechas:
                if revisado == False:
                    if self.revisar_colision(flecha.flecha, self.zona_abajo) == True:
                        self.aumentar_puntaje(flecha)
                        self.bailar('derecha')
                        revisado = True
                        flecha.paso_hecho = True
                        self.flechas.remove(flecha)
                        self.pasos_realizados += 1
                        self.actualizar_aprobacion()
                    elif self.revisar_colision(flecha.flecha, self.zona_abajo) == False:
                        self.aumentar_fallo()
                        revisado = True 
    
    def actualizar_aprobacion(self):
        if self.nivel == 'principiante':
            aprobacion = p.APROBACION_PRIN
        elif self.nivel == 'aficionado':
            aprobacion = p.APROBACION_AFI
        elif self.nivel == 'maestro':
            aprobacion = p.APROBACION_MAES
        self.porcentaje_aprob = (100 * self.puntaje_ronda)/aprobacion
        self.progreso_apruebo.setValue(int(self.porcentaje_aprob))
        self.actualizar_combo()
    
    def actualizar_combo(self):
        self.combo += 1
        if self.combo > self.max_combo:
            self.max_combo = self.combo
            self.label_mayorcombo.setText(f'Mayor combo: x{self.max_combo}')
        self.label_combo.setText(f'Combo: x{self.combo}')

    def bailar(self, direccion):
        if self.movido_amarillo == True:
            mov = os.path.join("sprites", "pinguirin_amarillo", f"amarillo_{direccion}.png")
            self.pin_amarillo.setPixmap(QPixmap(mov))
            self.pin_amarillo.setScaledContents(True)
            self.pin_amarillo.ruta = mov
        if self.movido_rojo == True:
            mov = os.path.join("sprites", "pinguirin_rojo", f"rojo_{direccion}.png")
            self.pin_rojo.setPixmap(QPixmap(mov))
            self.pin_rojo.setScaledContents(True)
            self.pin_rojo.ruta = mov
        if self.movido_verde == True:
            mov = os.path.join("sprites", "pinguirin_verde", f"verde_{direccion}.png")
            self.pin_verde.ruta = mov
            self.pin_verde.setPixmap(QPixmap(mov))
            self.pin_verde.setScaledContents(True)
        if self.movido_morado == True:
            mov = os.path.join("sprites", "pinguirin_morado", f"morado_{direccion}.png")
            self.pin_morado.ruta = mov
            self.pin_morado.setPixmap(QPixmap(mov))
            self.pin_morado.setScaledContents(True)
        if self.movido_celeste == True:
            mov = os.path.join("sprites", "pinguirin_celeste", f"celeste_{direccion}.png")
            self.pin_celeste.ruta = mov
            self.pin_celeste.setPixmap(QPixmap(mov))
            self.pin_celeste.setScaledContents(True)


    def cambiar_color(self, label, color):
        label.setStyleSheet("QLabel"
                                "{"
                                "border : 2px solid black;"
                                    f"background : {color};"
                                "}")

    def aumentar_puntaje(self, flecha):
        if flecha.tipo_flecha == 0 or flecha.tipo_flecha == 3:
            self.puntaje_ronda += p.PUNTOS_FLECHA
        elif flecha.tipo_flecha == 1:
            self.puntaje_ronda += p.PUNTOS_FLECHA_X2
        elif flecha.tipo_flecha == 2:
            self.puntaje_ronda += p.PUNTOS_FLECHA_DORADA

    def keyReleaseEvent(self, event):
        self.cambiar_color(self.zona_abajo, 'blue')
        self.cambiar_color(self.zona_arriba, 'blue')
        self.cambiar_color(self.zona_izq, 'blue')
        self.cambiar_color(self.zona_der, 'blue')
        self.bailar('neutro')
    
class Pinguino(QLabel, QDrag):
    def __init__(self, parent, ruta):
        super().__init__(parent)
        self.ruta = ruta
        self.setPixmap(QPixmap(self.ruta))
        self.setScaledContents(True)
        self.show()

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().center())
        dropAction = drag.exec_(Qt.MoveAction)

    def mousePressEvent(self, e):
        pass

class Flecha(QThread):

    senal_mover_flecha = pyqtSignal(QLabel, tuple)
    senal_paso_no_efectuado = pyqtSignal()

    def __init__(self, parent, seleccion, posx, tipo_flecha):
        super().__init__()
        self.tipo_flecha = tipo_flecha
        self.flecha = QLabel(parent)
        self.rutaflecha = os.path.join('sprites', 'flechas', seleccion)
        self.pixmap_flecha = QPixmap(self.rutaflecha)
        self.flecha.setPixmap(self.pixmap_flecha)
        self.flecha.setScaledContents(True)
        self.flecha.setVisible(True)
        self.flecha.setGeometry(posx, p.ALTURA_FLECHA_INICIAL, p.ALTO_FLECHA, p.ALTO_FLECHA)
        self.limite_y = p.ALTO_CAPTURA + p.CAPTURA_UP[1]
        self.__posicion = (posx, p.ALTURA_FLECHA_INICIAL)
        self.posicion = (posx, p.ALTURA_FLECHA_INICIAL)
        self.hielo = False
        self.paso_hecho = False

        self.flecha.show()
        self.start()

    @property
    def posicion(self):
        return self.__posicion

    @posicion.setter
    def posicion(self, valor):
        self.__posicion = valor
        self.senal_mover_flecha.emit(self.flecha, self.posicion)

    def run(self):
        while self.posicion[1] < self.limite_y:
            if self.tipo_flecha == 0 and self.hielo == False:
                self.sleep(p.VELOCIDAD_FLECHA)
            elif self.tipo_flecha == 1 and self.hielo == False:
                self.sleep(p.VELOCIDAD_FLECHA_DORADA)
            elif self.tipo_flecha == 2 and self.hielo == False:
                self.sleep(p.VELOCIDAD_FLECHA_X2)
            elif self.tipo_flecha == 3 or self.hielo == True:
                self.sleep(p.VEL_FLECHAS_CON_HIELO)
            nuevo_y = self.posicion[1] + 3
            self.posicion = (self.posicion[0], nuevo_y)
        self.flecha.hide()
        if self.paso_hecho == False:
            self.senal_paso_no_efectuado.emit()
    
    def sleep(self, segundos):
        loop = QEventLoop()
        QTimer.singleShot(int(segundos*1000), loop.quit)
        loop.exec_()