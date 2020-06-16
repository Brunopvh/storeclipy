#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil
import getpass

from lib.colors import PrintText as p, SetColor
from lib.yesno import YesNo
from lib.unpack_files import UnpackFiles
from lib.gitclone import GitClone
from lib.os_info import OsInfo
from lib.managers import PkgManager
from programs.downloadonly_files import DownloadOnlyFiles
from programs.wireless import WirelessTools

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
# Instalação dos programas voltados a WEB.
#================================================================#
class WebTools:
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

	def theHarvester(self):
		'''
		https://github.com/laramies/theHarvester
		https://github.com/laramies/theHarvester/wiki/Installation
		'''
		repo = 'https://github.com/laramies/theHarvester.git'
		self.gitclone.clone_repo(repo)
		os.chdir(f'{self.download_dir}/theHarvester')
		os.system('python3 -m pip install -U pipenv')
		os.system('python3 -m pip install -U -r requirements/base.txt')
		os.system('sudo python3 ./setup.py install')

		if self.is_executable('theHarvester') == 'True':
			p.green('theHarvester instalado com sucesso.')
		else:
			p.red('Falha ao tentar instalar theHarvester.')

	def searx(self):
		'''
		https://github.com/th3sha10wbr04rs/SearX_easy_Installer
		https://github.com/asciimoo/searx
		'''

		requirements_debian = [
			'git',
			'build-essential', 
			'libxslt-dev', 'python-dev', 
			'python-virtualenv', 
			'python-babel', 
			'zlib1g-dev', 
			'libffi-dev', 
			'libssl-dev',
		]
		
		repo = 'https://github.com/asciimoo/searx.git'
		self.gitclone.clone_repo(repo)
		if os.path.isdir('/opt/searx') == True:
			os.system('sudo rm -rf /opt/searx')

		os.chdir(self.download_dir)
		os.chmod('searx', 0o755)
		os.system('sed -i -e "s/ultrasecretkey/`openssl rand -hex 16`/g" searx/searx/settings.yml')
		os.system(f'sudo cp -R {self.download_dir}/searx /opt/searx')
		os.chdir('/opt/searx')
		os.system('python3 -m pip install --user --upgrade pip')
		os.system('python3 -m pip install --user --upgrade setuptools')
		os.system('python3 -m pip install -U -r requirements.txt')
		os.system('./manage.sh update_packages')

		# Criar um script para startar o searx em /usr/local/bin/searx
		with open(tempFile, 'w') as f:
			f.write('#!/bin/sh \n')
			f.write('cd /opt/searx/searx \n')
			f.write('./webapp.py "$@"\n')

		os.system(f'sudo mv {tempFile} /usr/local/bin/searx')
		os.system('sudo chmod a+x /usr/local/bin/searx')

