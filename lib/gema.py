#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pygame
import pygame

# Otros
from random import randint
import os

class Gema(pygame.sprite.Sprite):
    """
        Sprite para las gemas
    """

    def __init__(self, config, tipo = 0, sprites_activos = {}):

        # Inicializa el ancestro
        pygame.sprite.Sprite.__init__(self)

        # Valores de configuración
        self.config = config

        # Tipo de gema 
        self.parametros = config.gemas[tipo]

        # Tamaño original
        self.tamanio_x = self.parametros['tamanio_x']
        self.tamanio_y = self.parametros['tamanio_y']

        # Vida de la gema en segundos
        self.vida = self.parametros['vida']
        self.vida_original = self.vida

        # Indestructibilidad de la gema
        self.indestructible = self.parametros['indestructible']

        # Carga la imagen (convert_alpha() convierte la imagen con transparencias (per pixel transparency)
        self.imagen = pygame.image.load(os.path.join(self.config.dir_img, self.parametros['fichero'])).convert_alpha() 

        # Obtiene un rectángulo con las dimensiones y posición de la imagen
        self.rect = self.imagen.get_rect()

        # Sonido para la gema desaparece o es destruida
        self.sonido_rota = pygame.mixer.Sound(os.path.join(self.config.dir_snd, self.parametros['gemarota']))

        # Sonido para cada tick
        self.sonido_tick = pygame.mixer.Sound(os.path.join(self.config.dir_snd, self.parametros['tick']))

        # Fila la posición de inicio
        self.rect.centerx, self.rect.centery = self.__get_spawn()
        
        #
        # Evita que las gemas aparezcan unas sobre otras
        #

        # Si no hay otras gemas no hay que comprobar si hay colisión
        if sprites_activos['gema']:
            comprobar_colision = True
        else:
            comprobar_colision = False

        # Realiza comprobaciones de colisión hasta que la nueva gema no colisiona con
        # las ya existentes
        while comprobar_colision:
            
            comprobar_colision = False

            # Comprueba si ha habido colisión con alguna de las gemas activas
            for gema in sprites_activos['gema']:
                
                if pygame.sprite.collide_rect(self, gema):
                    
                    # Calcula una nueva posición de inicio y fuerza la comprobación
                    self.rect.centerx, self.rect.centery = self.__get_spawn()
                    comprobar_colision = True


    def tick(self):
        """
            Resta puntos de vida a la gema por cada frame que el jugador pase colisionando con
            ella
        """
        
        # La gema ha de seguir viva
        if self.vida > 0:

            # La cantidad de vida restada por cada frame viene dada por la fórmula:
            #
            # vida_restada_por_frame = 1 / FRAMERATE
            #
            # Como el framerate es el número de frames por segundo (fps) y la vida de la gema
            # viene expresada en segundos, dividiendo un segundo entre el número de frames
            # que tienen lugar en él se obtiene la cantidad de vida que pierde la gema en cada frame.
            vida_perdida = (1.0 / self.config.framerate)
            self.vida -= vida_perdida

            # La gema disminuye su tamaño al llegar a la mitad de su vida
            centro = self.rect.center
            factor_reduccion = 1 
            if self.vida <= (self.vida_original / 2):
                factor_reduccion = 0.66
            self.imagen = pygame.transform.smoothscale(self.imagen, (int(self.tamanio_x * factor_reduccion), int(self.tamanio_y * factor_reduccion)))

            # Reposiciona la nueva imagen usando el centro de la original
            self.rect = self.imagen.get_rect()
            self.rect.center = centro

            # Si no le queda vida la gema es destruida
            if self.vida <= 0:
                self.romper()

            else:
                # Indicación sonora de que la gema está perdiendo vida
                self.sonido_tick.stop()
                self.sonido_tick.play()

        else:
            vida_perdida = 0

        return vida_perdida

    def romper(self):
        """
            Destruye la gema
        """

        self.sonido_rota.play()
        self.vida = 0

    def __get_spawn(self):
        """
            Genera un punto de spawn en cualquier punto de la pantalla excluyendo
            los márgenes
        """
        x = randint(self.config.spawn_margen_x, self.config.ventana_ancho - self.config.spawn_margen_x)  
        y = randint(self.config.spawn_margen_y, self.config.ventana_alto - self.config.spawn_margen_y)  

        return (x, y)

if __name__ == '__main__':
    print u'Módulo no ejecutable'
