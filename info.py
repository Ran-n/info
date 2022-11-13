#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/11/09 20:59:20.693663
#+ Editado:	2022/11/13 22:23:33.082968
# ------------------------------------------------------------------------------

import sys
import ffmpeg
import pathlib
from datetime import datetime

from uteis.imprimir import jprint

def video(ficheiro):
    info = ffmpeg.probe(ficheiro)

    dic_return = {
            'data': str(datetime.now()),
            'nome fich': pathlib.Path(info['format']['filename']).stem,
            'extension': pathlib.Path(info['format']['filename']).suffix,
            'duracion': str(float(info['format']['duration'])) + ' s',
            'tamanho': info['format']['size'] + ' B',
            'bit rate': info['format']['bit_rate'] + ' b/s',
    }

    streams = []
    for stream in info['streams']:
        stream_dic = {
                'tipo': stream['codec_type'],
                'codec': stream['codec_name'],
        }

        if stream['codec_type'] == 'video':
            if stream.get('width') and stream.get('height'): stream_dic['calidade'] = str(stream['width']) + 'x' + str(stream['height'])
            if stream.get('sample_aspect_ratio'): stream_dic['ratio aspecto'] = stream['sample_aspect_ratio']
            if stream.get('pix_fmt'): stream_dic['formato de pixel'] = stream['pix_fmt']
            if stream.get('avg_frame_rate'): stream_dic['frame rate'] = str(round(eval(stream['avg_frame_rate']), 2)) + ' fps'

        else:
            if stream.get('tags').get('language'): stream_dic['lingua'] = stream['tags']['language']
            if stream['codec_type'] == 'audio':
                if stream.get('bit_rate'): stream_dic['bit rate'] = stream['bit_rate'] + ' b/s'
                if stream.get('sample_rate'): stream_dic['sample rate'] = stream['sample_rate'] + ' Hz'
                if stream.get('channel_layout'): stream_dic['canles'] = stream['channel_layout'].split('(')[0]

            elif stream['codec_type'] == 'subtitle':
                if stream.get('duration'): stream_dic['duracion'] = str(float(stream['duration'])) + ' s'

        streams.append(stream_dic)

    dic_return['streams'] = streams
    return dic_return

def erro_sufixo(ficheiro):
    return f'A extensión do ficheiro "{ficheiro}" non se atopa considerada.'

def main(ficheiro):
    extensions = {
        '.mkv': video,
        '.mp4': video,
    }

    try:
        funcion = extensions[pathlib.Path(ficheiro).suffix]
    except KeyError:
        funcion = erro_sufixo

    return funcion(ficheiro)

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        saida = main(sys.argv[1])
        if (type(saida) == str):
            print(saida)
        else:
            jprint(saida)
    else:
        print('Mete argumento')
