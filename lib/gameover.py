#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pygame
import pygame

# Otros
import os

class GameOver(pygame.sprite.Sprite):
    """
        Sprite con las instrucciones al finalizar una partida
    """

    # Color del texto
    COLOR = (255, 255, 255) 

    # Color de fondo para el texto
    COLOR_FONDO = (0, 0, 0) 

    # Tamaño del texto
    TAMANO = 25

    def __init__(self, config):

        # Inicializa el ancestro
        pygame.sprite.Sprite.__init__(self)

        # Valores de configuración
        self.config = config

        # Carga el tipo de letra
        self.tipo_letra = pygame.font.Font(os.path.join(self.config.dir_img, 'jet_set.ttf'), self.TAMANO)

        # Renderiza el texto con las instrucciones
        self.render_instrucciones()


    def render_instrucciones(self):
        """
            Renderiza el texto con las instrucicones
        """

        instrucciones = 'ENTER para jugar de nuevo - ESCAPE para salir'

        # Título del marcador más puntuación
        self.imagen = self.tipo_letra.render(instrucciones, 1, self.COLOR, self.COLOR_FONDO)

        # Obtiene un rectángulo con las dimensiones y posición de la imagen
        self.rect = self.imagen.get_rect()

        # Establece la posición
        self.rect.centerx = self.config.ventana_ancho / 2
        self.rect.centery = self.config.ventana_alto / 2


if __name__ == '__main__':
    print u'Módulo no ejecutable.'
