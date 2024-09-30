import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QWidget, QMainWindow
from PyQt5.QtGui import QPixmap
from time import sleep
from PyQt5.QtCore import QThread, QTimer, pyqtSignal

class Flecha(QThread):

    actualizar = pyqtSignal(QLabel, int, int)

    def __init__(self, parent):
        super().__init__()

        self.flecha = QLabel(parent)
        rutaflecha = os.path.join('sprites', 'flechas', 'right_1.png')
        self.pixmap_flecha = QPixmap(rutaflecha)
        self.flecha.setPixmap(self.pixmap_flecha)
        self.flecha.setScaledContents(True)
        self.flecha.setVisible(True)
        self.flecha.setGeometry(25, 0, 51, 51)
        self.limite_y = 500
        self.__posicion = (25, 0)
        self.posicion = (25, 0)

        self.flecha.show()
        self.start()

    @property
    def posicion(self):
        return self.__posicion

    @posicion.setter
    def posicion(self, valor):
        self.__posicion = valor
        self.actualizar.emit(self.flecha, *self.posicion)

    def run(self):
        while self.posicion[1] < self.limite_y:
            sleep(0.02)
            nuevo_y = self.posicion[1] + 3
            self.posicion = (self.posicion[0], nuevo_y)
            self.flecha.move(*self.posicion)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(300, 100, 100, 500)
        self.setMaximumHeight(500)
        self.setMaximumWidth(100)
        self.setMinimumHeight(500)
        self.setMinimumWidth(100)
        self.show()

        self.label_zona = QLabel('', self)
        self.label_zona.setStyleSheet("QLabel"
                                        "{"
                                     "border : 2px solid black;"
                                        "background : blue;"
                                        "}")
        self.label_zona.setGeometry(20,430,60,60)
        self.label_zona.show()

        self.label_flecha = Flecha(self)
        self.label_flecha.actualizar.connect(self.actualizar_label)

    def actualizar_label(self, label, x, y):
        label.move(x,y)
        if self.revisar_colision(label, self.label_zona) == True:
            self.label_zona.setStyleSheet("QLabel"
                                            "{"
                                        "border : 2px solid black;"
                                            "background : rgb(153,255,255);"
                                            "}")
        else:
            self.label_zona.setStyleSheet("QLabel"
                                            "{"
                                        "border : 2px solid black;"
                                            "background : blue;"
                                            "}")
    
    def revisar_colision(self, label1, label2):
        pos_inf = label2.y() - 60
        pos_sup = label2.y() + 60
        if label1.y() > pos_inf and label1.y() < pos_sup:
            return True


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    ventana = MainWindow()
    ventana.show()
    app.exec()

if __name__ == '__main__':
    app = QApplication([])
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
