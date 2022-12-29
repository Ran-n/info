#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/12/29 01:43:44.566474
#+ Editado:	2022/12/30 00:38:43.083108
# ------------------------------------------------------------------------------
import sys
import ffmpeg
import pathlib
from datetime import datetime
from dateutil import parser
from typing import List, Union

from uteis.imprimir import jprint
# ------------------------------------------------------------------------------
def formato_lingua(lingua: Union[List[str], str]) -> str:
    if (type(lingua) == str): return lingua
    return f'{lingua[1]} [{lingua[0]}]'

def get_lingua(lingua: str) -> str:
    dic_linguas = {
            'eng': ['en', 'Inglés'],
            'ita': ['it', 'Italiano'],
            'spa': ['cas', 'Castelán'],
            'fre': ['fr', 'Francés'],
            'jpn': ['ni', 'Xaponés'],
            'ger': ['de', 'Alemán'],
            'pol': ['pl', 'Polaco'],
            'por': ['po', 'Portugués'],
            'nor': ['no', 'Noruego'],
            'swe': ['sw', 'Sueco'],
            'dut': ['nl', 'Neederlandés'],
            'fin': ['sk', 'Finlandés'],
            'dan': ['da', 'Danés']
    }

    return formato_lingua(dic_linguas.get(lingua, 'ERRO: Engadir lingua'))

def hms2s(tempo: str) -> str:
    h, m, s = tempo.split(':')
    s, ms = str(float(s)).split('.')
    return str(int(h)*60*60+int(m)*60+int(s))+'.'+ms

def get_codec(codec: str) -> Union[str, None]:
    codec_types= {
            'video': 'videos',
            'audio': 'audios',
            'subtitle': 'subtitulos',
    }

    try:
        return codec_types[codec]
    except KeyError as e:
        raise Exception(f'Non existe o codec "{codec}".') from e
# ------------------------------------------------------------------------------
def canle(datos: dict, stream: dict) -> dict:
    nova_canle = {}

    try:
        tags = stream['tags']
    except:
        tags = None

    codec = get_codec(stream['codec_type'])

    # Posición
    if ('index' in stream):
        nova_canle['Posición'] = stream['index'] + 1
    # Codec
    if ('codec_name' in stream):
        nova_canle['Codec'] = stream['codec_name']
    # Índice
    if ('codec_long_name' in stream):
        nova_canle['Codec nome'] = stream['codec_long_name']
    # Nome
    if (tags and 'title' in tags):
        nova_canle['Nome'] = tags['title']
    # Lingua
    if (tags and 'language' in tags):
        nova_canle['Lingua'] = get_lingua(tags['language'])
    # Calidade
    if (('width' in stream) and ('height' in stream)):
        nova_canle['calidade'] = str(stream['width']) + 'x' + str(stream['height'])
    # Ratio aspecto sample
    if ('sample_aspect_ratio' in stream):
        nova_canle['Ratio aspecto sample'] = stream['sample_aspect_ratio']
    # Ratio aspecto display
    if ('display_aspect_ratio' in stream):
        nova_canle['Ratio aspecto display'] = stream['display_aspect_ratio']
    # Formato de pixel
    if ('pix_fmt' in stream):
        nova_canle['Formato de pixel'] = stream['pix_fmt']
    # Frame Rate
    if ((stream['codec_type'] == 'video') and ('avg_frame_rate' in stream)):
        numerador, divisor = [int(ele) for ele in stream['avg_frame_rate'].split('/')]
        if (divisor == 0):
            nova_canle['Frame Rate'] = stream['avg_frame_rate'].split('/')[0] + ' fps'
        else:
            nova_canle['Frame Rate'] = str(round(numerador/divisor, 2)) + ' fps'
    # Canles
    if ('channel_layout' in stream):
        nova_canle['Canles'] = " (".join(stream['channel_layout'].split('('))
    # Número canles
    if ('channels' in stream):
        nova_canle['Número canles'] = stream['channels']
    # Sample Rate
    if ('sample_rate' in stream):
        nova_canle['Sample Rate'] = stream['sample_rate'] + ' Hz'
    # Bit Rate
    if ('bit_rate' in stream):
        nova_canle['Bit Rate'] = stream['bit_rate'] + ' b/s'
    # Tamanho
    if (tags and 'NUMBER_OF_BYTES' in tags):
        nova_canle['Tamanho'] = tags['NUMBER_OF_BYTES'] + ' b'
    # Inicio
    if ('start_time' in stream):
        nova_canle['Inicio'] = str(float(stream['start_time'])) + ' s'
    # Fin
    if (tags and 'DURATION' in tags):
        nova_canle['Fin'] = hms2s(tags['DURATION']) + ' s'
    if ('duration' in stream):
        nova_canle['Fin'] = stream['duration'] + ' s'

    # disposition

    # non existe a lista dos streams crear
    if (codec not in datos):
        datos[codec] = []
    # meter nova canle
    datos[codec].append(nova_canle)

    return datos
# ------------------------------------------------------------------------------
def main(fich: str) -> dict:
    datos = {
            'Data': str(datetime.now()),
    }

    info = ffmpeg.probe(fich)

    try:
        formato = info['format']
    except:
        formato = None
    try:
        tags = formato['tags']
    except:
        tags = None

    # Ficheiro
    if (formato and 'nb_streams' in formato):
        datos['Ficheiro'] = formato['filename']
    # Nome Ficheiro
    if (formato and 'nb_streams' in formato):
        datos['Nome ficheiro'] = pathlib.Path(formato['filename']).stem
    # Extensión
    if (formato and 'nb_streams' in formato):
        datos['Extensión'] = pathlib.Path(formato['filename']).suffix
    # Tamanho
    if (formato and 'nb_streams' in formato):
        datos['Tamanho'] = formato['size'] + ' B'
    # Duración
    if (formato and 'nb_streams' in formato):
        datos['Duración'] = str(float(formato['duration'])) + ' s'
    # Bit Rate
    if (formato and 'nb_streams' in formato):
        datos['Bit Rate'] = formato['bit_rate'] + ' b/s'
    # Título
    if (tags and 'title' in tags):
        datos['Título'] = tags['title']
    # Data creación
    if (tags and 'creation_time' in tags):
        data = parser.parse(tags['creation_time'])
        datos['Data creación'] = data.strftime('%Y-%m-%d %H:%M:') + str(float(data.strftime('%S.%f')))
        del data
    # Cantidade de canles
    if (formato and 'nb_streams' in formato):
        datos['Cantidade de canles'] = formato['nb_streams']

    # streams
    if ('streams' in info):
        for stream in info['streams']:
            datos = canle(datos, stream)

    return datos
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # long or short info

    # backdoor para mostrar o orixinal fácilmente
    if (len(sys.argv) == 3):
        jprint(ffmpeg.probe(sys.argv[1]))
    # comprobar que mete argumento a ler
    elif (len(sys.argv) > 1):
        saida = main(sys.argv[1])
        if (type(saida) == str):
            print(saida)
        else:
            jprint(saida)
    else:
        print('Mete argumento')
# ------------------------------------------------------------------------------
