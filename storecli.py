#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import argparse

__version__ = '2021-01-24'

dir_run = os.getcwd()    
_script = os.path.abspath(os.path.realpath(__file__))

# Endereço deste script no disco.
dir_of_executable = os.path.dirname(_script) 
dir_of_project = dir_of_executable

# Diretórios contento módulos locais.
dir_local_libs = os.path.abspath(os.path.join(dir_of_executable, 'lib'))

# Inserir o diretório ./lib no PATH do python - print(sys.path)                          
sys.path.insert(0, dir_local_libs)

# Módulos locais.
import requeriments
import programs
from utils import KERNEL_TYPE
from requeriments import ConfigureCliRequeriments

# root
if KERNEL_TYPE == 'Linux':
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
    '-c', '--configure',
    action='store_true', 
    dest='configure_requeriments', # Argumento que não será passado para opção -l/--list.
    help='Instalar dependências deste programa.'
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


parser.add_argument(
    '-u', '--self-update',
    action='store_true', 
    dest='self_update', # Argumento que não será passado para opção -l/--list.
    help='Instalar a versão mais recente deste programa apartir do github.'
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
    'idea-ic',
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
elif args.configure_requeriments:
    ConfigureCliRequeriments().check_all_requeriments()
elif args.self_update:
    programs.__self_update__(dir_of_project)
elif args.pkg_for_install:          # Instalar um programa
    # Verificar por nova versão uma vez por dia.
    programs.check_update_local(dir_of_project)

    for pkg in args.pkg_for_install:
        if pkg == 'etcher':
            programs.Etcher().install()
        elif pkg == 'veracrypt':
            programs.Veracrypt().install()
        elif pkg == 'google-chrome':
            programs.Browser().google_chrome()
        elif pkg == 'opera-stable':
            programs.Browser().opera_stable()
        elif pkg == 'java':
            Java().install()
        elif pkg == 'idea-ic':
            programs.Idea().install()
        elif pkg == 'pycharm':
            programs.Pycharm().install()
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
	        programs.Etcher().remove()
	    elif pkg == 'veracrypt':
	        programs.Veracrypt().remove()
	    elif pkg == 'pycharm':
	        programs.Pycharm().remove()
	    elif pkg == 'idea-ic':
	        programs.Idea().remove()
	    else:
	        print(f'[!] Não foi possivel remover {pkg}')
        
        
        
        
        
