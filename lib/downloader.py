#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
import urllib.request
import subprocess

def is_executable(exec):
    if int(subprocess.getstatusoutput(f'command -v {exec}')[0]) == int('0'):
        return True
    else:
        return False
        
def wget_download(url, output_path):
    import wget
    if os.path.isfile(output_path) == True:
        print(f'Arquivo encontrado ... {output_path}')
        return
    
    print(f'Conectando ... {url}')
    info = urllib.request.urlopen(url)
    try:
        length = int(info.getheader('content-length'))
    except:
        pass
    else:
        if length and (length != None):
            if length >= (1024 * 1024):
                lengthMB = float(length / int(1024 * 1024))
                print('Total ... {:.2f}MB'.format(lengthMB))
            else:
                print('Total ... {} Kb'.format(length))

    print(f'Baixando ... {output_path}')
    try:
        wget.download(url, output_path)
    except Exception as erro:
        print(' ')
        print(erro)
    else:
        print(' OK')
        
        
def run_download(url, output_path):
    
    if os.path.isfile(output_path) == True:
        print(f'Arquivo encontrado ... {output_path}')
        return
    
    if is_executable('curl') == True:
        os.system(f'curl -S -L -o {output_path} {url}')
    elif is_executable('wget') == True:
        os.system(f'wget {url} -O {output_path}')
    else:
        
        try:
            import wget
        except:
            print()
            print('Instale o módulo wget: pip3 install wget --user')
            sys.exit()
        else:
            wget_download(url, output_path)




