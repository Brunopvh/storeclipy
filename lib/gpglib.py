#!/usr/bin/env python3
'''
https://www.programcreek.com/python/example/82300/gnupg.GPG
https://files.gpg4win.org/gpg4win-3.1.13.exe
pip3 install python-gnupg --user
'''

import os
import platform
import urllib.request
from subprocess import getstatusoutput
from pathlib import Path

try:
    import gnupg
except Exception as err:
    print(err, '==> Execute - pip3 install gnupg --user')
    import sys
    sys.exit()

if platform.system() == 'FreeBSD':
    DirHome = os.path.abspath(os.path.join('/usr', Path.home()))
else:
    DirHome = os.path.abspath(os.path.join(Path.home()))

DirGpg = os.path.abspath(os.path.join(DirHome, '.gnupg'))
gpg = gnupg.GPG()

def check_binary():
    if platform.system() == 'Windows':
        out = int(getstatusoutput('gpg.exe --help')[0])
    elif (platform.system() == 'Linux') or (platform.system() == 'FreeBSD'):
        out = int(getstatusoutput('gpg --help')[0])

    if out == 0:
        return True
    else:
        return False

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
    if check_binary() != True:
        print('gpg não está instalado no seu sistema.')
        return False

    if url_key != None:
        print(f'Baixando ... {url_key}', end=' ')
        try:
            urllib.request.urlretrieve(url_key, key_file)
        except Exception as err:
            print('\n', err)
            return False
        else:
            print('OK')

    print(f'Importando ... {key_file}') 
    if platform.system() == 'Windows':
        os.system(f'gpg.exe --import {key_file}')
    elif (platform.system() == 'Linux') or (platform.system() == 'FreeBSD'):
        key_data = open(key_file).read()    
        import_result = gpg.import_keys(key_data)
        for k in import_result.results:
            print(k)

def gpg_list():
    public_keys = gpg.list_keys()
    private_keys = gpg.list_keys(True)
    print('public keys:')
    print(public_keys)
    print('private keys:')
    print(private_keys)

def gpg_verify(path_to_signature_file, path_file):
    '''
    https://pythonhosted.org/python-gnupg/#verification
    '''
    print(f'Verificando integridade do arquivo ... {path_file}')
    if platform.system() == 'Windows':
        out = int(getstatusoutput(f'gpg.exe --verify {path_to_signature_file} {path_file}')[0])
        if out == 0:
            return True
        else:
            return False
    else:  
        data = open(path_file, 'rb').read()
        verified = gpg.verify_data(path_to_signature_file, data)
        if verified.status == 'signature valid':
            print('OK')
            return True
        else:
            print('FALHA')
            return False



