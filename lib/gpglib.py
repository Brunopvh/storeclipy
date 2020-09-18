#!/usr/bin/env python3

import os
import platform
import urllib.request
from subprocess import getstatusoutput
from pathlib import Path

def gpg_import(key_file, url_key=None):
    '''
    Função para importar chaves gpg. você pode informar apenas o arquivo .asc com os dados
    ou caso preferir pode informar o URL que contém um arquivo com os dados a serem importados
    é um caminho completo onde o arquivo será baixado.

    EX:
       gpg_import(key_file) => irá assumir que o arquivo já existe no local indicado.
       gpg_import(key_file, url) => irá baixar o "URL" no "destino key_file".
    '''

    # Verificar se o gpg está instalado no sistema operacional.
    if url_key != None:
        print(f'Baixando ... {url_key}', end=' ')
        try:
            urllib.request.urlretrieve(url_key, key_file)
        except Exception as err:
            print('\n', err)
            return False
        else:
            print('OK')

    print(f'Importando ... {key_file}', end=' ') 
    out = getstatusoutput(f'gpg --import {key_file}')
    if out[0] == 0:
        print('\033[0;32mOK\033[m')
        return True
    else:
        print('')
        print('\033[0;31mERRO\033[m')
        print(out[1])
        return False

def gpg_verify(path_to_signature_file, path_file):
    print(f'Verificando arquivo ... {path_file}', end=' ')
    out = getstatusoutput(f'gpg --verify {path_to_signature_file} {path_file}')
    if out[0] == 0:
        print('\033[0;32mOK\033[m')
        return True
    else:
        print('')
        print('\033[0;31mERRO\033[m')
        print(out[1])
        return False
    



