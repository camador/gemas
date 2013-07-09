#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.gui import GUI

def main():

    # Instancia la clase para la GUI
    gui = GUI()

    # Método de inicio
    gui.main()

    return 0

if __name__ == '__main__':
    
    try:

        main()

    except Exception, e:
        print '\n'
        print u'Error inesperado: '
        print '\n\t', e, '\n'
