#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/11/09 20:59:20.693663
#+ Editado:	2022/11/09 22:52:04.315289
# ------------------------------------------------------------------------------

import sys
import ffmpeg
from datetime import datetime

from uteis.imprimir import jprint

def video(info):
    duracion_s, duracion_ms = str(info['format']['duration']).split('.')
    dic_return = {
            'data': str(datetime.now()),
            'nome fich': info['format']['filename'].split('/')[-1],
            'duracion': duracion_s + duracion_ms.rstrip('0'),
            'tamanho': info['format']['size'],
            'bit rate': info['format']['bit_rate'],
    }

    streams = []
    for stream in info['streams']:
        stream_dic = {
                'tipo': stream['codec_type'],
                'codec': stream['codec_name'],
        }

        if stream['codec_type'] == 'video':
            stream_dic['calidade'] = str(stream['width']) + 'x' + str(stream['height'])
            stream_dic['ratio aspecto'] = stream['sample_aspect_ratio']
            stream_dic['formato de pixel'] = stream['pix_fmt']
            stream_dic['frame rate'] = round(eval(stream['avg_frame_rate']), 2)

        else:
            stream_dic['lingua'] = stream['tags']['language']
            if stream['codec_type'] == 'audio':
                stream_dic['sample rate'] = stream['sample_rate']
                stream_dic['bit rate'] = stream['bit_rate']
                stream_dic['canles'] = stream['channel_layout'].split('(')[0]

            elif stream['codec_type'] == 'subtitle':
                stream_dic['duracion'] = stream['duration_ts']

        streams.append(stream_dic)

    dic_return['streams'] = streams
    return dic_return

def main(ficheiro):
    try:
        info = ffmpeg.probe(ficheiro)
    except Exception as e:
        print(e)
        print('Non é un video')

    return video(info)

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        jprint(main(sys.argv[1]))
    else:
        print('Mete argumento')
