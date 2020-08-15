#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#----------------------------------------------------------#
# Requerimentos
#----------------------------------------------------------#
# requests - (python3.7+)
# wget -     (python3.7+) $ pip3 install wget
# python -   (3.7+)
#
#

import os
import sys
import argparse

__version__ = '2020-06-15'

# Endereço deste script no disco.
dir_root = os.path.dirname(os.path.realpath(__file__)) 

 # Diretório onde o terminal está aberto.
dir_run = os.getcwd()                                 

# Inserir o diretório do script no PATH do python - print(sys.path)                          
sys.path.insert(0, dir_root)

from programs.run import RunInstaller, DownloadOnlyFiles
from lib.colors import PrintText as p, SetColor
from lib.os_info import OsInfo

if os.geteuid() == int('0'):
	p.red('NÂO execute como root.')
	sys.exit('1')

parser = argparse.ArgumentParser(
			description='Instala programas para penteste em sistemas Linux.'
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
os_id = OsInfo().get_os_id()
os_version = OsInfo().get_os_version_id()
os_kernel = OsInfo().get_os_kernel()

p.yellow(f'{os.path.basename(os.path.realpath(__file__))} V{__version__} - {os_kernel} {os_id} {os_version}')

if args.list_all_apps:
	print()
	p.green('WIRELESS: ')
	p.green('fluxion')
	p.green('wifiphisher')
	print()

	p.green('WEB: ')
	p.green('searx')
	p.green('theharvester')
	print()

elif args.pkg_for_download:         # Realizar somente download do programa informado.
	if not args.dir_download:
		p.red('Você precisa informar um diretório para baixar os arquivos em --dir')
		exit()

	if os.path.isdir(args.dir_download) == False:
		p.red(f'O diretório informado não existe: {args.dir_download}')
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
	elif args.pkg_for_install == 'searx':
		RunInstaller().searx()
	elif args.pkg_for_install == 'theharvester':
		RunInstaller().theHarvester()

