#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

import sys

class DB():
    """
        Gestiona las operaciones con la base de datos
    """

    # Datos de conexión
    BASEDATOS = 'lib/gemas.db'

    def __init__(self):
        """
            Crea la conexión con la base de datos y el cursor para operar con ella.

            Si la base de datos no existe la crea con la estructura necesaria para 
            la ejecución del juego
        """

        try:

            # Conexión a la base de datos
            self.db = sqlite3.connect(self.BASEDATOS)

            # Permite acceder por nombre de campo los datos devueltos por el cursor
            self.db.row_factory = sqlite3.Row

            # Creación del cursor
            self.cursor = self.db.cursor()

        except Exception, e:
            print '\n'
            print u'Error de base de datos: '
            print '\n\t', e, '\n'

            # Termina la ejecución
            sys.exit(0)


    ##
    ## CONFIG
    ##
    def get_config(self, clave):
        """
            Devuelve el valor de configuración correspondiente a la clave recibida por parámetros
        """

        consulta = 'select valor from config where clave = "{0}";'.format(clave)

        self.cursor.execute(consulta)
        registro = self.cursor.fetchone()

        return registro['valor']

    def set_config(self, clave, valor):
        """
            Actualiza el valor de configuración de la clave recibida por parámetros
        """

        update = 'update config set valor = "{0}" where clave = "{1}";'.format(valor, clave)
    
        self.cursor.execute(update)
        self.db.commit()

    ##
    ## RESOLUCIONES
    ##
    def get_resoluciones(self):
        """
            Recupera los registros de la tabla 'resoluciones'
        """

        consulta = 'select * from resoluciones;'

        self.cursor.execute(consulta)
        registros = self.cursor.fetchall()
        
        return registros

    def get_resolucion(self, resolucion = ''):
        """
            Recupera de la tabla resoluciones el registro cuyo campo 'descripcion'
            es igual al parámetro 'resolucion'
        """

        consulta = 'select * from resoluciones where descripcion = "{0}";'.format(resolucion)

        self.cursor.execute(consulta)
        registro = self.cursor.fetchone()
        
        return registro

    ##
    ## JUGADOR
    ##
    def get_jugador(self, tipo = 0):
        """
            Recupera el registro de la tabla 'jugadores' correspondiente a 'tipo'
        """

        consulta = 'select * from jugadores where tipo = {0};'.format(tipo)

        self.cursor.execute(consulta)
        registro = self.cursor.fetchone()
        
        return registro
       
    ##
    ## GEMAS
    ##
    def get_gemas(self):
        """
            Recupera los registros de la tabla 'gemas'
        """

        consulta = 'select * from gemas;'

        self.cursor.execute(consulta)
        registros = self.cursor.fetchall()
        
        return registros

    ##
    ## ENEMIGOS
    ##
    def get_enemigos(self):
        """
            Recupera los registros de la tabla 'enemigos'
        """

        consulta = 'select * from enemigos;'

        self.cursor.execute(consulta)
        registros = self.cursor.fetchall()
        
        return registros

    ##
    ## PUNTUACION
    ##
    def guarda_puntuacion(self, puntos = 0):
        """
            Guarda una puntuación
        """

        insert = "insert into puntuaciones (nombre, puntos, fecha) values ('Jugador', {0}, now());".format(puntos)

        self.cursor.execute(insert)
        self.db.commit()

    def get_record(self):
        """
            Devuelve la puntuación más alta
        """
        
        # Valor a devolver si todavía no hay puntuaciones registradas
        record = 0

        consulta = 'select max(puntos) as record from puntuaciones;'

        self.cursor.execute(consulta)
        registro = self.cursor.fetchone()

        if registro['record']:
            record = int(registro['record'])

        return record


    ##
    ## COMUNES
    ##
    def get_probabilidad(self, tabla = 'gemas'):
        """
            Devuelve una lista con las probabilidades de las gemas
        """

        consulta = 'select probabilidad from {0} order by tipo;'.format(tabla)

        self.cursor.execute(consulta)
        registros = self.cursor.fetchall()
        
        # Genera la lista tomando el valor de cada registro
        probabilidades = []
        for registro in registros:
            probabilidades.append(int(registro['probabilidad']))

        return probabilidades

    ##
    ## CLOSE
    ##
    def close(self):
        """
            Cierra el cursor y la conexión
        """

        # Cierra cursor y conexión de la base de datos
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    print u'Módulo no ejecutable.'
