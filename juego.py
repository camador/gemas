#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Base de datos
from lib.db import DB

# Juego
from lib.config import Config
from lib.jugador import Jugador
from lib.enemigo import Enemigo
from lib.gema import Gema
from lib.marcador import Marcador
from lib.record import Record
from lib.gameover import GameOver

# Pygame
import pygame
from pygame.locals import *

# Otros
import os
import sys
from random import randint

##
## MAIN
##
def main():

    try :

        #
        # CONFIGURACIÓN
        #

        # Gestor de base de datos
        db = DB()

        # Carga los valores de configuración
        config = Config(db)

        # Listas de probabilidades de aparación
        probabilidad_enemigos = db.get_probabilidad('enemigos')
        probabilidad_gemas = db.get_probabilidad('gemas')

        # Instancia un reloj para controlar el tiempo
        reloj = pygame.time.Clock()

        #
        # VENTANA
        #

        # Crea la ventana
        ventana = pygame.display.set_mode((config.ventana_ancho, config.ventana_alto))

        # Título de la ventana
        pygame.display.set_caption('Gemas')

        # Carga el fondo (convirtiéndolo al formato usado en SDL para mejorar la eficiencia)
        fondo = pygame.image.load(os.path.join(config.dir_img, 'fondo.jpg')).convert()

        # Inicia partidas hasta que el usuario decide terminar la ejecución del programa
        salir = False
        while not salir:

            #
            # SPRITES
            #

            # Diccionario de sprites activos en cada momento
            sprites_activos = {}

            # Instancia al jugador y lo añade a la lista de sprites activos
            jugador = Jugador(config)
            sprites_activos['jugador'] = jugador

            # Instancia dos enemigos y los añade a la lista de sprites activos
            sprites_activos['enemigo'] = [Enemigo(config, 0), Enemigo(config, 1)]

            # Indica el momento en el que se generó el último enemigo
            ultimo_enemigo_respawn = pygame.time.get_ticks()

            # Instancia las gemas y las añade a la lista de sprites activos
            #
            # Hay varios tipos de gemas, cada una con una probabilidad distinta de ser
            # generada. La generación de las gemas es aleatoria pero teniendo en cuenta
            # dicha probabilidad
            sprites_activos['gema'] = []
            for i in range(1, config.gema_max_activas + 1):
                tipo_gema = get_tipo(probabilidad_gemas)
                gema = Gema(config, tipo_gema, sprites_activos)
                sprites_activos['gema'].append(gema)

            # Indica el momento en que ha de generarse una nueva gema (0 = no se genera ninguna)
            proximo_respawn_gema = 0

            # Marcador
            marcador = Marcador(config)
            sprites_activos['marcador'] = marcador

            # Puntuación máxima
            record = Record(config, db)
            sprites_activos['record'] = record
            
            # Fin de partida
            gameover = GameOver(config)


            #
            # BUCLE DE EVENTOS
            #

            # El programa permanece funcionando hasta que se cierra la ventana
            # Cada iteración del bucle es un frame
            fin_partida = False
            while not fin_partida:

                # Averigua el tiempo (en milisegundos) transcurrido por cada frame
                # Además, al usar FRAMERATE en la llamada, se fija el número de frames por segundo
                # independientemente del hardware de la máquina
                tiempo = reloj.tick(config.framerate)

                # Obtiene y recorre la lista de eventos que están teniendo lugar
                for evento in pygame.event.get():

                    # Si encuentra el evento QUIT termina la ejecución
                    if evento.type == QUIT:
                        fin_partida = True
                        salir = True

                    # La tecla ESC termina la ejecución
                    elif evento.type == KEYDOWN:
                        if evento.key == K_ESCAPE:
                            salir = True
                            fin_partida = True

                #
                # CALCULO DEL MOVIMIENTO Y PUNTUACIÓN
                #

                jugador.mover(tiempo, sprites_activos)
                marcador.render_puntos(jugador.puntos)
                for enemigo in sprites_activos['enemigo']:
                    enemigo.mover(tiempo, sprites_activos)

                #
                # ACTUALIZACIÓN DE POSICIONES EN PANTALLA
                #

                # Situa el fondo en el primer pixel de la ventana
                ventana.blit(fondo, (0, 0))

                # Actualiza la posición de los sprites
                for nombre in sprites_activos.keys():
                    # Si se trata de una lista de sprites la recorre y
                    # procesa cada elemento
                    if isinstance(sprites_activos[nombre], list):
                        for elemento in sprites_activos[nombre]:

                            # Si el sprite es una gema sin vida la elimina de los sprites activos
                            if nombre == 'gema' and elemento.vida <= 0:
                                sprites_activos[nombre].remove(elemento)
                            else:
                                ventana.blit(elemento.imagen, elemento.rect)
                    else:
                        ventana.blit(sprites_activos[nombre].imagen, sprites_activos[nombre].rect)

                #
                # ACTUALIZACIÓN DE LA PANTALLA
                #

                # Dibuja la escena
                pygame.display.flip()

                #
                # EVALUACIÓN DEL ESTADO DE LOS SPRITES
                #

                # Comprueba si el jugador sigue vivo
                if not jugador.vivo:

                    # Guarda la puntución
                    db.guarda_puntuacion(jugador.puntos)

                    # Pequeña pausa para que el mensaje de game over no salte brúscamente
                    pygame.time.delay(1000)

                    # Avisa al jugador
                    ventana.blit(gameover.imagen, gameover.rect)
                    pygame.draw.rect(ventana, (255, 255, 255), gameover.rect.inflate(7, 5), 2)

                    # Actualiza la pantalla
                    pygame.display.flip()

                    # y finaliza la partida
                    fin_partida = True

                else:

                    # Si el jugador sigue vivo:
                    # - Genera nuevas gemas si es necesario
                    # - Genera nuevos enemigos según aumenta el tiempo de juego

                    #
                    # Generación de gemas
                    #

                    # Las gemas se generan siempre que haya menos del máximo permitido y 
                    # siempre después de pasado cierto tiempo (config.gema_respawn) desde la
                    # desaparición de una gema o desde la generación de una nueva, lo que ocurra
                    # antes. Es decir, mientras haya menos gemas de las permitidas se genera una
                    # nueva cada 'config.gema_respawn' milisegundos

                    # Si hay menos gemas activas del máximo permitido es necesario generar una nueva
                    if len(sprites_activos['gema']) < config.gema_max_activas:

                        # Calcula el momento para la creación de la gema, pero sólo si dicho momento no 
                        # ha sido todavía calculado para evitar que a cada iteración del bucle (cada frame)
                        # se recalcule y la gema no llegue a generarse nunca
                        if proximo_respawn_gema == 0:

                            # La gema se generará después del momento actual más el tiempo de espera
                            # para la generación de gemas
                            proximo_respawn_gema = pygame.time.get_ticks() + config.gema_respawn

                        # Comprueba si ha pasado suficiente tiempo como para generar la gema
                        if proximo_respawn_gema <= pygame.time.get_ticks():

                            # Ya se puede crear la gema y añadirla a la lista de sprites activos
                            tipo_gema = get_tipo(probabilidad_gemas)
                            gema = Gema(config, tipo_gema, sprites_activos)
                            sprites_activos['gema'].append(gema)

                            # Resetea el momento para la creación de la siguiente gema
                            proximo_respawn_gema = 0

                    #
                    # Generación de enemigos 
                    #

                    # Cada cierto tiempo se genera un enemigo nuevo. El tipo es aleatorio pero
                    # sujeto a la probabilidad de generación de cada enemigo
                    if (pygame.time.get_ticks() - ultimo_enemigo_respawn) / config.enemigo_respawn > 0:
                        tipo_enemigo = get_tipo(probabilidad_enemigos)
                        sprites_activos['enemigo'].append(Enemigo(config, tipo_enemigo))

                        # Anota el momento en el que se ha generado el último enemigo
                        ultimo_enemigo_respawn = pygame.time.get_ticks()


            #
            # FIN DE LA PARTIDA
            #
            if fin_partida:

                #
                # CONTROL PARA JUGAR UNA NUEVA PARTIDA O TERMINAR EL PROGRAMA
                # 

                while not salir and fin_partida: 

                    # Obtiene y recorre la lista de eventos que están teniendo lugar
                    for evento in pygame.event.get():

                        # Si encuentra el evento QUIT termina la ejecución
                        if evento.type == QUIT:
                            salir = True

                        # Pulsaciones de teclas
                        elif evento.type == KEYDOWN:

                            # La tecla ESC termina la ejecución
                            if evento.key == K_ESCAPE:
                                salir = True

                            # La tecla RETURN inicia una nueva partida
                            elif evento.key == K_RETURN:
                                fin_partida = False

        #
        # FIN DE LA EJECUCIÓN DEL PROGRAMA
        #

        # Cierra la conexión con la base de datos
        db.close()
        
        # Termina la ejecución
        sys.exit(0)

    except pygame.error, e:
        print '\n'
        print u'Error en Pygame: '
        print '\n\t' , e, '\n'

##
## FUNCIONES AUXILIARES
##
def get_tipo(pesos):
    """
        Genera aleatoriamente un índice de la lista recibida pero teniendo en cuenta
        el peso (la probabilidad) de cada uno de los elementos.

        El valor de cada elemento de la lista es el peso de dicho elemento.
    """
    
    # Genera un número aleatorio entre 1 y la suma total de los pesos
    num_aleatorio = randint(1, sum(pesos))

    # Recorre la lista de pesos buscando el elemento al que pertenece el número aleatorio:
    #
    # Si el número es menor que el peso del primer item, el índice a devolver será el de dicho item,
    # si no lo es suma el valor del primer item y del segundo y repite la comparación. Si el número
    # es menor que la suma devuelve el índice del segundo item, si no, suma el valor del tercero, y 
    # así hasta que encuentre el item correcto

    suma_pesos = 0
    for indice in range(0, len(pesos)):

        # Añade el peso del elemento a la suma de pesos
        suma_pesos += pesos[indice]
        
        # Comprueba si el número aleatorio 'pertenece' al elemento actual
        if num_aleatorio <= suma_pesos:

            # Item encontrado
            return indice

if __name__ == '__main__':

    try:
        
        # Inicializa Pygame
        pygame.init()

        # Empezando...
        main()
        
    except Exception, e:
        print '\n'
        print u'Error inesperado: '
        print '\n\t', e, '\n'
