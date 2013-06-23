#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pygame
import pygame

# Otros
import os

class Record(pygame.sprite.Sprite):
    """
        Sprite para el marcador de puntuación
    """

    # Posición para los puntos
    POS_X = 400
    POS_Y = 30

    # Color del texto
    COLOR = (255, 255, 255) 

    # Tamaño del texto
    TAMANO = 25

    def __init__(self, config, db):

        # Inicializa el ancestro
        pygame.sprite.Sprite.__init__(self)

        # Valores de configuración
        self.config = config

        # Base de datos
        self.db = db

        # Carga el tipo de letra
        self.tipo_letra = pygame.font.Font(os.path.join(self.config.dir_img, 'jet_set.ttf'), self.TAMANO)

        # Renderiza el marcador con 0 puntos
        self.render_record()


    def render_record(self):
        """
            Renderiza la puntuación máxima
        """

        # Recupera la puntuación máxima
        record = self.db.get_record()

        # Título del marcador más puntuación
        self.imagen = self.tipo_letra.render('Record: {0}'.format(record), 1, self.COLOR)

        # Obtiene un rectángulo con las dimensiones y posición de la imagen
        self.rect = self.imagen.get_rect()

        # Establece la posición
        self.rect.centerx = self.POS_X
        self.rect.centery = self.POS_Y

if __name__ == '__main__':
    print u'Módulo no ejecutable.'
