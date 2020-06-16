#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tarfile
from zipfile import ZipFile, is_zipfile
import shutil
import sys
from time import sleep

from lib.colors import PrintText as p, SetColor
from lib.yesno import YesNo

s = SetColor()

class UnpackFiles:
	def __init__(self, destination=''):
		self.destination = destination

	def check_destination(self):
		if os.path.isdir(self.destination) == False:
			os.makedirs(self.destination)

		if os.access(self.destination, os.W_OK) == True:
			return 'True'
		else:
			print(f'[!] Falha você não tem permissão de escrita em: {self.destination}')
			return 'False'

	def clear_dir(self):
		os.chdir(self.destination)
		content = os.listdir('.')
		for i in content:
			p.yellow(f'Limpando: {i}')
			try:
				shutil.rmtree(i)
			except:
				p.red(f'Falha ao tentar remover: {i}')
				if YesNo.yesno(f'Deseja remover {i}') == 'True':
					os.system(f'sudo rm -rf {i}')

	def tar(self, file):
		# https://docs.python.org/3.3/library/tarfile.html

		# Verificar se o arquivo e do tipo tar
		if not tarfile.is_tarfile(file):
			p.red(f'O arquivo NÃO é do tipo {s.red}.tar{s.reset}: {file}')
			return

		if self.check_destination() == 'False':
			print('Saindo')
			return

		self.clear_dir()
		print(f'{s.yellow}[+]{s.reset} Descomprimindo: {file}', end= ' ')
		os.chdir(self.destination)
		try:
			tar = tarfile.open(file)
			tar.extractall()
			tar.close()
			p.sblue('OK')
		except:
			print()
			p.red(f'Falha na descompressão de: {file}')
			sys.exit('1')

	def zip(self, file):
		# https://docs.python.org/pt-br/3/library/zipfile.html
		# https://www.geeksforgeeks.org/working-zip-files-python/

		# Verificar se o arquivo e do tipo zip
		if not is_zipfile(file):
			p.red(f'O arquivo NÃO é do tipo {s.red}.zip{s.reset}: {file}')
			return

		if self.check_destination() == 'False':
			print('Saindo')
			return

		self.clear_dir()
		print(f'{s.yellow}[+]{s.reset} Descomprimindo: {file}', end= ' ')
		os.chdir(self.destination)

		try:
			with ZipFile(file, 'r') as zip: 
				# printing all the contents of the zip file 
				# zip.printdir()  
				zip.extractall()
			p.sblue('OK')
		except:
			print()
			p.red(f'Falha na descompressão de: {file}')
			sys.exit('1')
		
			
