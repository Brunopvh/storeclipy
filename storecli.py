#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import argparse
import platform 

__version__ = '2020-08-29'

# Endereço deste script no disco.
dir_root = os.path.dirname(os.path.realpath(__file__)) 

# Nome do script/app
app_name = os.path.basename(__file__)

# Diretório onde o terminal está aberto.
dir_run = os.getcwd()        

# Inserir o diretório do script no PATH do python - print(sys.path)                          
sys.path.insert(0, dir_root)

#from lib.processloop import ProcessLoop
from lib.print_text import PrintText  
from lib.libstorecli import *

# root
if os.geteuid() == int('0'):
    PrintText().red('Usuário não pode ser o root saindo')
    sys.exit('1')

# Linux ou BSD
sys_kernel = str(platform.system())
if (sys_kernel != 'Linux') and (sys_kernel != 'FreeBSD'):
    PrintText().red(f'Execute este program em sistemas Linux ou FreeBSD')
    exit()


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
    dest='pkg_for_install',
    type=str,
    help='Instalar um pacote'
    )

parser.add_argument(
    '-r', '--remove', 
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
apps_list = (
    'veracrypt',
    'pycharm',
    'google-chrome',
    'opera-stable', 
    'youtube-dl-gui',
    'papirus',
)

if args.list_all_apps:
    print()
    for X in apps_list:
        print('   ', X)

elif args.pkg_for_download:         # Realizar somente download do programa informado.
    if not args.dir_download:
        PrintText().red('Você precisa informar um diretório para baixar os arquivos em --dir')
        exit()

    if os.path.isdir(args.dir_download) == False:
        PrintText().red(f'O diretório informado não existe: {args.dir_download}')
        exit()

    if args.pkg_for_download == 'fluxion':
        DownloadOnlyFiles(args.dir_download).fluxion()
    elif args.pkg_for_download == 'theharvester':
        DownloadOnlyFiles(args.dir_download).theHarvester()
    elif args.pkg_for_download == 'searx':
        DownloadOnlyFiles(args.dir_download).searx()
    elif args.pkg_for_download == 'wifiphisher':
        DownloadOnlyFiles(args.dir_download).wifiphisher()
        

elif args.pkg_for_install:          # Instalar um programa

    if args.pkg_for_install == 'wifiphisher':
        RunInstaller().wifiphisher()
    elif args.pkg_for_install == 'fluxion':
        RunInstaller().fluxion()
    elif args.pkg_for_install == 'google-chrome':
        Browser().google_chrome()
    elif args.pkg_for_install == 'java':
        Java().install()
    elif args.pkg_for_install == 'idea':
        Idea().install()
    elif args.pkg_for_install == 'pycharm':
        Pycharm().install()
    elif args.pkg_for_install == 'papirus':
        Papirus().install()
    elif args.pkg_for_install == 'searx':
        RunInstaller().searx()
    elif args.pkg_for_install == 'torbrowser':
        Browser().torbrowser()
    elif args.pkg_for_install == 'theharvester':
        RunInstaller().theHarvester()
    elif args.pkg_for_install == 'youtube-dl-gui':
        YoutubeDlg().install()
    elif args.pkg_for_install == 'veracrypt':
        Veracrypt().install()
    else:
        print(f'Programa indisponível: {args.pkg_for_install}')

elif args.pkg_for_remove:          # Desinstalar um programa
    if args.pkg_for_remove == 'pycharm':
        Pycharm().remove()
    elif args.pkg_for_remove == 'idea':
        Idea().remove()
    else:
        print(f'[!] Não foi possivel remover {args.pkg_for_remove}')
