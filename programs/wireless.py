#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil
import getpass
from pathlib import Path

from lib.colors import PrintText as p, SetColor
from lib.yesno import YesNo
from lib.downloader import PyWget
from lib.unpack_files import UnpackFiles
from lib.gitclone import GitClone
from lib.os_info import OsInfo
from lib.managers import PkgManager
from programs.downloadonly_files import DownloadOnlyFiles

s = SetColor()
os_id = OsInfo().get_os_id()

TempDir = f'/tmp/storeclipy_{getpass.getuser()}'
UnpackDir = f'{TempDir}/unpack'
tempFile = f'{TempDir}/file.tmp'
dir_scripts = '{}/scripts'.format(os.path.dirname(os.path.realpath(__file__)))
script_addrepo = f'{dir_scripts}/addrepo.py'

if os.path.isdir(TempDir) == False:
	os.makedirs(TempDir)

if os.path.isdir(UnpackDir) == False:
	os.makedirs(UnpackDir)

#================================================================#
# Instalação dos programas
#================================================================#
class WirelessTools:
	'''
	download_dir e o local que será usado para baixar os arquivos
	e também será acessado por esta classe para descomprimir e configurar
	os pacotes antes de suas respectivas instalações.
	'''

	def __init__(self):
		self.download_dir = f'{Path.home()}/.cache/downloads'
		self.unpack = UnpackFiles(UnpackDir) 
		self.gitclone = GitClone(self.download_dir)

	def is_executable(self, executable):
		e = int(subprocess.getstatusoutput(f'which {executable} 2> /dev/null')[0])

		if e == int('0'):
			return 'True' # Existe
		else: 
			return 'False' # Não existe

	def wifiphisher(self):
		'''
		https://github.com/wifiphisher/wifiphisher
		sudo apt-get install libnl-3-dev libnl-genl-3-dev libssl-dev
		sudo dnf install libnl3.x86_64 libnl3-devel.x86_64 openssl-devel.x86_64
		'''
		url = 'https://github.com/wifiphisher/wifiphisher/archive/master.zip'
		repo = 'https://github.com/wifiphisher/wifiphisher.git'
		os.chdir(self.download_dir)
		self.gitclone.clone_repo(repo)
		os.chdir('wifiphisher')
		
		# Instalar dependências para wifiphisher
		if os.path.isfile('/etc/fedora-release'):
			PkgManager(['libnl3.x86_64', 'libnl3-devel.x86_64', 'openssl-devel.x86_64']).dnf('install')
			
		elif os.path.isfile('/etc/debian_version'):
			# Adicionar repositórios main contrib e non-free para kalilinux ou debian.
			if os_id == 'kali':
				os.system(f'sudo {script_addrepo} --repo kalilinux')
			elif os_id == 'debian':
				os.system(f'sudo {script_addrepo} --repo debian')

			PkgManager(['libnl-3-dev', 'libnl-genl-3-dev', 'libssl-dev']).apt('install')
			

		os.system('sudo python3 ./setup.py install')
		if self.is_executable('wifiphisher'):
			p.green('wifiphisher instalado com sucesso')
		else:
			p.red('Falha ao tentar istalar wifiphisher')

	def fluxion(self):
		'''
		https://github.com/FluxionNetwork/fluxion
		https://www.tutorialspoint.com/python3/os_chmod.htm
		'''
		destinationFile = f'{self.download_dir}/fluxion.zip'
		DownloadOnlyFiles().fluxion()
		self.unpack.zip(destinationFile)
		os.chdir(UnpackDir)

		if os.path.isdir('/opt/fluxion') == True:
			os.system('sudo rm -rf /opt/fluxion')

		os.chmod('fluxion-master', 0o755)
		os.system('sudo mv fluxion-master /opt/fluxion')
		os.system('sudo ln -sf /opt/fluxion/fluxion.sh /usr/local/bin/fluxion')
		
		# Lista com dependências para fluxion.
		requeriments_fluxion_linux = [
			'aircrack-ng',
			'bc',
			'gawk',                                  
            'curl',                                   
            'cowpatty',                                                                     
            'hostapd',                                   
            'lighttpd',                                                                    
            'macchanger',                                                                    
            'dsniff',                                                                  
            'nmap',                                   
            'openssl',                                   
            'php-cgi',                                   
            'xterm',                                   
            'rfkill',                                   
            'unzip',                                                                                               
		]

		requeriments_fluxion_fedora = [
			'dhcp',                                 
            'p7zip',
            'mdk4', 
            'mdk3',   
            'wireless-tools',  
            'net-tools',    
            'psmisc',     
		]

		requeriments_fluxion_debian = [
			'isc-dhcp-server',                                 
            'p7zip',
            'mdk4', 
            'mdk3',   
            'wireless-tools',  
            'net-tools',    
            'psmisc',     
		]

		if os.path.isfile('/etc/fedora-release'):     
			PkgManager(requeriments_fluxion_linux).dnf('install')  # Fedora
			PkgManager(requeriments_fluxion_fedora).dnf('install') 
		elif os.path.isfile('/etc/debian_version'):  
			PkgManager(requeriments_fluxion_linux).apt('install')  # Debian e derivados
			PkgManager(requeriments_fluxion_debian).apt('install')

		if self.is_executable('fluxion') == 'True':
			p.yellow('Fluxion instalado com sucesso')
		else:
			p.red('Falha na instalação de fluxion')
		

	

