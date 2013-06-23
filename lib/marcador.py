#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pygame
import pygame

# Otros
import os

class Marcador(pygame.sprite.Sprite):
    """
        Sprite para el marcador de puntuación
    """

    # Posición para los puntos
    POS_X = 100
    POS_Y = 30

    # Color del texto
    COLOR = (255, 255, 255) 

    # Tamaño del texto
    TAMANO = 25

    def __init__(self, config):

        # Inicializa el ancestro
        pygame.sprite.Sprite.__init__(self)

        # Valores de configuración
        self.config = config

        # Carga el tipo de letra
        self.tipo_letra = pygame.font.Font(os.path.join(self.config.dir_img, 'jet_set.ttf'), self.TAMANO)

        # Renderiza el marcador con 0 puntos
        self.render_puntos(0)


    def render_puntos(self, puntos = 0):
        """
            Renderiza el texto recibido
        """

        # Título del marcador más puntuación
        self.imagen = self.tipo_letra.render('Puntos: {0}'.format(puntos), 1, self.COLOR)

        # Obtiene un rectángulo con las dimensiones y posición de la imagen
        self.rect = self.imagen.get_rect()

        # Establece la posición
        self.rect.centerx = self.POS_X
        self.rect.centery = self.POS_Y

if __name__ == '__main__':
    print u'Módulo no ejecutable.'
