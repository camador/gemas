#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pygame
import pygame

# Otros
from random import randint
import os

class Enemigo(pygame.sprite.Sprite):
    """
        Sprite para los enemigos
    """

    def __init__(self, config, tipo = 0):

        # Inicializa el ancestro
        pygame.sprite.Sprite.__init__(self)

        # Valores de configuración
        self.config = config

        # Tipo de enemigo
        self.tipo = tipo
        enemigo = config.enemigos[tipo]

        # Carga la imagen (convert_alpha() convierte la imagen con transparencias (per pixel transparency)
        self.imagen = pygame.image.load(os.path.join(self.config.dir_img, enemigo['fichero'])).convert_alpha() 

        # Disminuye el tamaño del sprite para que no se vea demasiado grande
        self.imagen = pygame.transform.smoothscale(self.imagen, (enemigo['tamanio_x'], enemigo['tamanio_y']))

        # Obtiene un rectángulo con las dimensiones y posición de la imagen
        self.rect = self.imagen.get_rect()

        # Disminuye el tamaño del rect para evitar que en las colisiones parezca que los 
        # sprites no se tocan
        self.rect.inflate_ip(-10, -10)

        # Fila la posición de inicio
        self.rect.centerx, self.rect.centery = self.__get_spawn()

        # Velocidad de movimiento en cada eje
        self.velocidad = {
                            self.config.eje_x: self.config.velocidad_base * enemigo['factor_velocidad'],
                            self.config.eje_y: self.config.velocidad_base * enemigo['factor_velocidad']
                         }

    def mover(self, tiempo, sprites_activos):
        """
            Gestiona el movimiento del enemigo: movimiento automático en diagonal con rebote
            en los bordes de la ventana

            El cálculo de la posición del personaje se realiza en función de la velocidad y
            del tiempo (d = v * t, distancia = velocidad * tiempo), o sea, la nueva posición
            será igual a la posición actual más la distancia recorrida en el eje correspondiente

            El tiempo recibido como parámetro es el tiempo transcurrido por cada frame
        """

        # Cálculo de la distancia recorrida en un frame
        distancia_x = self.__get_distancia(self.config.eje_x, tiempo)
        distancia_y = self.__get_distancia(self.config.eje_y, tiempo)

        # Modifica la posición en los dos ejes
        self.rect.centerx += distancia_x
        self.rect.centery += distancia_y

        # Al llegar a un borde de la ventana se invierte el sentido del movimiento en el eje
        # correspondiente y se recalcula la posición

        if self.rect.left <= 0 or self.rect.right >= self.config.ventana_ancho:
            self.__rebote(self.config.eje_x, tiempo)

        if self.rect.top <= 0 or self.rect.bottom >= self.config.ventana_alto:
            self.__rebote(self.config.eje_y, tiempo)

        #
        # Detección de colisiones
        #

        # Jugador
        if pygame.sprite.collide_rect(self, sprites_activos['jugador']):
            sprites_activos['jugador'].muerto()

        # Gemas
        # Comprueba si ha habido colisión con alguna de las gemas activas, si es que
        # hay alguna
        if sprites_activos['gema']:

            # Comprueba si ha habido colisión con alguna de las gemas activas
            for gema in sprites_activos['gema']:
       
                if pygame.sprite.collide_rect(self, gema):

                    # Las gemas hacen que el enemigo rebote
                    if self.rect.left <= gema.rect.right or self.rect.right >= gema.rect.left:
                        self.__rebote(self.config.eje_x, tiempo)


                    if self.rect.top <= gema.rect.bottom or self.rect.bottom >= gema.rect.top:
                        self.__rebote(self.config.eje_y, tiempo)

                    # Las rocas (tipo 1) destruyen las gemas
                    if self.tipo == 1 and not gema.indestructible:
                        gema.romper()


    def __get_spawn(self):
        """
            Selecciona aleatoriamente un punto de spawn de entre los disponibles
        """
        
        return self.config.spawn_points[randint(0, len(self.config.spawn_points) - 1)]

    def __get_distancia(self, eje, tiempo):
        """
            Calcula la distancia recorrida en el eje indicado 
        """

        return self.velocidad[eje] * tiempo

    def __rebote(self, eje, tiempo):
        """
            Invierte el sentido del movimiento en el eje especificado y recalcula la
            posición
        """

        # Invierte el sentido del movimiento
        self.velocidad[eje] *= -1

        # El enemigo de tipo 0 invierte su imagen al rebotar horizontalmente
        if self.tipo == 0 and eje == self.config.eje_x:
            self.imagen = pygame.transform.flip(self.imagen, True, False)

        # Recalcula la distancia recorrida
        distancia = self.__get_distancia(eje, tiempo)

        # Fija la nueva posición
        if eje == self.config.eje_x:
            self.rect.centerx += distancia
        else:
            self.rect.centery += distancia


if __name__ == '__main__':
    print u'Módulo no ejecutable'
