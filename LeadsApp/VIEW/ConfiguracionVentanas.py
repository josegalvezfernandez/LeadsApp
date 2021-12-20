# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 12:02:11 2021

@author: Usuario
"""

TAMAÑO_BOTON = 25
PADX = 5
PADY = 5
BORDERWIDTH = 4
    
def get_filename_from_IOWrapper(IOwrapper):
    print(f"······ {str(IOwrapper)}")
    strIO = str(IOwrapper).split("'")
    return strIO[1]