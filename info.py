#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/12/29 01:44:18.799717
#+ Editado:	2022/12/29 16:20:25.029319
# ------------------------------------------------------------------------------

#+ Creado: 	2022/12/29 01:43:44.566474
#+ Editado:	2022/12/29 16:20:25.029319
# ------------------------------------------------------------------------------
import sys
import ffmpeg
import pathlib
from datetime import datetime

from uteis.imprimir import jprint
# ------------------------------------------------------------------------------
def erro_sufixo(fich):
    return f'A extensión do ficheiro "{fich}" non se atopa considerada.'
# ------------------------------------------------------------------------------
def main(fich):
    info = ffmpeg.probe(fich)

    return info
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # comprobar que mete argumento a ler
    if (len(sys.argv) > 1):
        saida = main(sys.argv[1])
        if (type(saida) == str):
            print(saida)
        else:
            jprint(saida)
    else:
        print('Mete argumento')
# ------------------------------------------------------------------------------
