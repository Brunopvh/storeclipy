#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tarfile
from zipfile import ZipFile, is_zipfile
import shutil
import sys
from time import sleep

class UnpackFiles:
	def __init__(self, destination=os.getcwd()):
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
		for DIR in content:
			if (os.path.isdir(DIR) == True) or (os.path.isfile(DIR) == True):
				print(f'Limpando: {DIR}')
				try:
					shutil.rmtree(DIR)
				except:
					print(f'Autenticação nescessária para remover ... {DIR}')
					os.system(f'sudo rm -rf {DIR}')

	def tar(self, file):
		# https://docs.python.org/3.3/library/tarfile.html

		# Verificar se o arquivo e do tipo tar
		if not tarfile.is_tarfile(file):
			print(f'O arquivo NÃO é do tipo {s.red}.tar{s.reset}: {file}')
			return

		if self.check_destination() == 'False':
			print('Saindo')
			return

		self.clear_dir()
		print(f'Descomprimindo: {file}', end= ' ')
		os.chdir(self.destination)
		try:
			tar = tarfile.open(file)
			tar.extractall()
			tar.close()
			print('OK')
		except:
			print()
			print(f'Falha na descompressão de: {file}')
			sys.exit('1')

	def zip(self, file):
		# https://docs.python.org/pt-br/3/library/zipfile.html
		# https://www.geeksforgeeks.org/working-zip-files-python/

		# Verificar se o arquivo e do tipo zip
		if not is_zipfile(file):
			print(f'O arquivo NÃO é do tipo (.zip) ... {file}')
			return

		if self.check_destination() == 'False':
			print('Saindo')
			return

		self.clear_dir()
		print(f'Descomprimindo: {file}', end= ' ')
		os.chdir(self.destination)

		try:
			with ZipFile(file, 'r') as zip: 
				# printing all the contents of the zip file 
				# zip.printdir()  
				zip.extractall()
			print('OK')
		except:
			print()
			print(f'Falha na descompressão de: {file}')
			sys.exit('1')
		
			
