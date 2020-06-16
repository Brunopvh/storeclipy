#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path

from lib.colors import PrintText as p, SetColor
from lib.yesno import YesNo
from lib.downloader import PyWget
from lib.gitclone import GitClone

s = SetColor()


#================================================================#
# Download dos programas
#================================================================#
class DownloadOnlyFiles:
	'''
	Classe para fazer somente o download dos arquivos '--downloadonly'
	DownloadOnlyFiles(dir).program()
	DownloadOnlyFiles().fluxion()

	O destino padrão de downloads e o diretório temporário da variável DownloadDir em /tmp
	Se você deseja baixar em um destino/caminho diferente informa um diretório já existente
	DownloadOnlyFiles(dir)
	'''
	def __init__(self, download_dir=f'{Path.home()}/.cache/downloads'):
		self.download_dir = download_dir

	def check_dir(self):
		if os.path.isdir(self.download_dir) == False:
			try: 
				os.makedirs(self.download_dir)
			except:
				p.red(f'Falha ao tentar criar o diretório: {self.download_dir}')
				return 'False'

		if os.access(self.download_dir, os.W_OK) == True:
			return 'True'
		else:
			p.red(f'Falha você não tem permissão de escrita em: {self.download_dir}')
			return 'False'

	def fluxion(self):
		if self.check_dir() == 'False':
			return

		url = 'https://github.com/FluxionNetwork/fluxion/archive/master.zip'
		destinationFile = f'{self.download_dir}/fluxion.zip'
		p.blue(f'fluxion github: https://github.com/FluxionNetwork/fluxion')
		PyWget().run_download(url, destinationFile)

	def searx(self):
		if self.check_dir() == 'False':
			return

		url = 'https://github.com/asciimoo/searx/archive/master.zip'
		destinationFile = f'{self.download_dir}/searx.zip'
		p.blue(f'searx github: https://github.com/asciimoo/searx')
		PyWget().run_download(url, destinationFile)

	def theHarvester(self):
		if self.check_dir() == 'False':
			return

		url = 'https://github.com/laramies/theHarvester/archive/master.zip'
		destinationFile = f'{self.download_dir}/theHarvester.zip'
		p.blue(f'theHarvester github: https://github.com/laramies/theHarvester')
		PyWget().run_download(url, destinationFile)


	def wifiphisher(self):
		if self.check_dir() == 'False':
			return

		url = 'https://github.com/wifiphisher/wifiphisher/archive/master.zip'
		destinationFile = f'{self.download_dir}/wifiphisher.zip'
		p.blue(f'wifiphisher github: https://github.com/wifiphisher/wifiphisher')
		PyWget().run_download(url, destinationFile)
