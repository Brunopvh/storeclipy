#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import argparse
import platform 

__version__ = '2020-09-17'

if platform.system() != 'Linux':
    print('Seu sistema não é suportado. Execute apenas em sistemas Linux.')
    sys.exit()

# Diretório onde o terminal está aberto.
dir_run = os.getcwd()    

# Endereço deste script no disco.
dir_root = os.path.dirname(os.path.realpath(__file__)) 

# Diretórios contento módulos locais.
dir_lib = os.path.abspath(os.path.join(dir_root, 'lib'))

# Inserir o diretório do script no PATH do python - print(sys.path)                          
sys.path.insert(0, dir_lib)

# Nome do script/app
app_name = os.path.basename(__file__)

from lib.print_text import PrintText  
from lib.libstorecli import *

# root
if os.geteuid() == int('0'):
    PrintText().red('Usuário não pode ser o root saindo')
    sys.exit('1')

parser = argparse.ArgumentParser(
            description='Instala programas em sistemas Linux e FreeBSD.'
            )

parser.add_argument(
    '-v', '--version', 
    action='version', 
    version=(f"%(prog)s {__version__}")
    )

parser.add_argument(
    '-l', '--list',
    action='store_true', 
    dest='list_all_apps', # Argumento que não será passado para opção -l/--list.
    help='Mostra programas disponíveis para instalação'
    )
    
parser.add_argument(
    '-i', '--install', 
    action='store',
    nargs='*', 
    dest='pkg_for_install',
    type=str,
    help='Instalar um pacote'
    )

parser.add_argument(
    '-r', '--remove', 
    nargs='*',
    action='store', 
    dest='pkg_for_remove',
    type=str,
    help='Desisntala um pacote'
    )

parser.add_argument(
    '-d', '--download', 
    action='store', 
    dest='pkg_for_download',
    type=str,
    help='Somente baixa um pacote'
    )

parser.add_argument(
    '-D', '--dir', 
    action='store', 
    dest='dir_download',
    type=str,
    help='Diretório para download'
    )

args = parser.parse_args()

#----------------------------------------------------------#
# Execução
#----------------------------------------------------------#
# Lista de aplicativos disponíveis para instalação.
apps_acessory = (
    'etcher',
    'veracrypt',
    )

apps_development = (
    'intellij-idea',
    'pycharm',
    )

apps_office = (
    'fontes-ms',
    )

apps_browser = (
    'google-chrome',
    'opera-stable',
    )

apps_internet = (
    'youtube-dl-gui',
    )

apps_preferences = (
    'papirus',
)

if args.list_all_apps: # Listar os aplicativos disponiveis para instalação.
    print()
    print(' Acessorios:')
    for app in apps_acessory:
        print('   ', app)

    print()
    print(' Desenvolvimento:')
    for app in apps_development:
        print('   ', app)

    print()
    print(' Escritório:')
    for app in apps_office:
        print('   ', app)

    print()
    print(' Navegadores:')
    for app in apps_browser:
        print('   ', app)

    print()
    print(' Internet:')
    for app in apps_internet:
        print('   ', app)

    print()
    print(' Preferências:')
    for app in apps_preferences:
        print('   ', app)

elif args.pkg_for_install:          # Instalar um programa
    for pkg in args.pkg_for_install:
        if pkg == 'etcher':
            Etcher().install()
        elif pkg == 'veracrypt':
            Veracrypt().install()
        elif pkg == 'google-chrome':
            Browser().google_chrome()
        elif pkg == 'java':
            Java().install()
        elif pkg == 'intellij-idea':
            Idea().install()
        elif pkg == 'pycharm':
            Pycharm().install()
        elif pkg == 'papirus':
            Papirus().install()
        elif pkg == 'searx':
            RunInstaller().searx()
        elif pkg == 'fontes-ms':
            MsFonts().install()
        elif pkg == 'torbrowser':
            Browser().torbrowser()
        elif pkg == 'youtube-dl':
            YoutubeDl().install()
        elif pkg == 'youtube-dl-gui':
            YoutubeDlGui().install()
        elif pkg == 'youtube-dl':
            youtube_dl()
        elif pkg == 'wine':
            Wine().install()
        else:
            print(f'Programa indisponível: {pkg}')

elif args.pkg_for_remove:          # Desinstalar um programa
	for pkg in args.pkg_for_remove:
	    if pkg == 'etcher':
	        Etcher().remove()
	    elif pkg == 'veracrypt':
	        Veracrypt().remove()
	    elif pkg == 'pycharm':
	        Pycharm().remove()
	    elif pkg == 'intellij-idea':
	        Idea().remove()
	    else:
	        print(f'[!] Não foi possivel remover {pkg}')
        
        
        
        
        
