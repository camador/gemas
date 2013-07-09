#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PyQt
from PyQt4 import uic, QtGui, QtCore

# Juego
from lib.db import DB

# Otros
import sys

class GUI(QtGui.QWidget):
    """
        Herramienta de configuración
    """

    def __init__(self):

        # Antes de nada crea el objeto 'aplicación' de Qt
        self.app = QtGui.QApplication(sys.argv)

        # Inicicializa el ancestro
        QtGui.QWidget.__init__(self)

        # Fija el nombre de la aplicación
        self.app.setApplicationName('Gemas - Configuración')
        
        # Lee el fichero que contiene la interfaz gráfica
        self.ui = uic.loadUi('lib/gui.ui')

        # Resolución
        self.combobox_resolucion = self.ui.findChild(QtGui.QComboBox, 'cbbResolucion')

        # FPS
        self.spinbox_fps = self.ui.findChild(QtGui.QSpinBox, 'spbFPS')

        # Jugador
#        self.radiobutton_jugador = [
#                                    self.builder.get_object('radiobuttonJugador1'),
#                                    self.builder.get_object('radiobuttonJugador2'),
#                                    self.builder.get_object('radiobuttonJugador3'),
#                                    self.builder.get_object('radiobuttonJugador4'),
#                                    self.builder.get_object('radiobuttonJugador5')
#                                   ]

        # Gemas Máx. Activas
        self.spinbox_gemas_max_activas = self.ui.findChild(QtGui.QSpinBox, 'spbGemasMaxActivas')

        # Gemas Respawn
        self.spinbox_gemas_respawn = self.ui.findChild(QtGui.QSpinBox, 'spbGemasRespawn')

        # Enemigos Respawn
        self.spinbox_enemigos_respawn = self.ui.findChild(QtGui.QSpinBox, 'spbEnemigosRespawn')

        # Guarda y salir
        self.pushbutton_guardar = self.ui.findChild(QtGui.QPushButton, "pbtGuardar")

        # Conecta las señales
        self.pushbutton_guardar.clicked.connect(self.on_guardar)

        # Gestor de base de datos
        self.db = DB()

    ##
    ## MAIN
    ##
    def main(self):
        """
            Método de inicio
        """

        # Muestra la ventana principal
        self.ui.show()

        #
        # Lee de la base de datos la información para cada widget
        #

        # Resoluciones
        resolucion_id = 0
        resoluciones = self.db.get_resoluciones()
        for resolucion in resoluciones:
            self.combobox_resolucion.addItem(resolucion['descripcion'], int(resolucion['id']))

            # Comprueba si se trata de la resolución actual
           # if resolucion['ancho'] == self.db.get_config('VENTANA_ANCHO') and resolucion['alto'] == self.db.get_config('VENTANA_ALTO'):
           #     resolucion_actual = resolucion_id

           # resolucion_id += 1

        # Seleccion la resolución actual
        #self.combobox_resolucion.set_active(resolucion_actual) 

        # FPS
        framerate = int(self.db.get_config('FRAMERATE'))
        self.spinbox_fps.setValue(framerate)

        # Jugador
        jugador_tipo = int(self.db.get_config('JUGADOR_TIPO'))
        #self.radiobutton_jugador[jugador_tipo].set_active(True)

        # Gemas Máx. Activas 
        gemas_max_activas = int(self.db.get_config('GEMA_MAX_ACTIVAS'))
        self.spinbox_gemas_max_activas.setValue(gemas_max_activas)

        # Gemas Respawn
        gemas_respawn = int(self.db.get_config('GEMA_RESPAWN'))
        self.spinbox_gemas_respawn.setValue(gemas_respawn)

        # Enemigos Respawn
        enemigos_respawn = int(self.db.get_config('ENEMIGO_RESPAWN'))
        self.spinbox_enemigos_respawn.setValue(enemigos_respawn)

        # A la espera de evento
        self.app.exec_()
    
    ##
    ## VENTANA PRINCIPAL
    ##
    def window_main_destroy(self, *args):
        """
            Termina la ejecución del programa
        """

        # Cierra la conexión con la base de datos
        self.db.close()

        # Saliendo
        sys.exit()

    ##
    ## GUARDAR
    ##
    def on_guardar(self, *args):
        """
            Guarda en la base de datos los valores de los widgets
        """

        # 
        # Resoluciones
        # 

        # Resolución seleccionada
        #item = self.combo_box_Resoluciones.get_active() 

        # Lista de resoluciones del combobox
        #resoluciones = self.combo_box_Resoluciones.get_model()
        
        # Recupera el registro correspondiente a la resolución seleccionada
        #resolucion = self.db.get_resolucion(resoluciones[item][0])

        # Actualiza la configuración
        #self.db.set_config('VENTANA_ANCHO', resolucion['ancho'])
        #self.db.set_config('VENTANA_ALTO', resolucion['alto'])

        # 
        # FPS
        # 
        self.db.set_config('FRAMERATE', self.spinbox_fps.value())
    
        #
        # JUGADOR
        #

        # Recorre los radiobuttons para localizar el seleccionado
        jugador_seleccionado = 0
        #for radio in self.radiobutton_jugador:

            # Cuando encuentra el activo sale del bucle
        #    if radio.get_active():
        #        break;
            
            # Si no es el activo incrementa el índice
        #    jugador_seleccionado += 1

        # Actualiza la base de datos
        #self.db.set_config('JUGADOR_TIPO', jugador_seleccionado)

        #
        # GEMAS
        #

        # Gemas Máx. Activas 
        self.db.set_config('GEMA_MAX_ACTIVAS', self.spinbox_gemas_max_activas.value())
        self.db.set_config('GEMA_RESPAWN', self.spinbox_gemas_respawn.value())

        #
        # ENEMIGOS
        #
        self.db.set_config('ENEMIGO_RESPAWN', self.spinbox_enemigos_respawn.value())

        # Sale
        self.window_main_destroy()
    

if __name__ == '__main__':
    print u'Módulo no ejecutable.'
