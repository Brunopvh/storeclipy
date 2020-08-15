#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import wget
from time import sleep
from os import remove, path
from lib.colors import PrintText as p, SetColor

s = SetColor()

class PyWget:

	def __init__(self):
		self.url = ''
		self.file = ''

	def bar_custom(self, current, total, width=80):
		# https://pt.stackoverflow.com/questions/207887/como-imprimir-texto-na-mesma-linha-em-python
		
		current = current / 1048576        # Converter bytes para MB
		total = total / 1048576            # Converter bytes para MB
		progress = (current / total) * 100 # Percentual
		

		current = '{:.2f}'.format(current)
		total = '{:.2f}'.format(total)
		progress = '{:.2f}'.format(progress)
		
		if progress == '100':
			print(f'\033[K[>] Progresso: [{progress}%] [{current}/{total}]MB', end='\r')

		print(f'\033[K[>] Progresso: [{progress}%] [{current}/{total}]MB', end='\r')

	def run_download(self, url, file=''):
		'''
		wget.download(url, out=None, bar=<function bar_adaptive at 0x7f7fdfed9d30>)
		wget.download(url, out=None, bar=bar_adaptive(current, total, width=80))
		'''
		self.url = url
		self.file = file

		if path.isfile(self.file):
			p.yellow(f'Arquivo encontrado: {self.file}')
			return

		p.yellow(f'Obtendo informações do servidor aguarde.')
		response = requests.get(url, stream=True)
		total_length = response.headers.get('content-length')

		p.yellow(f'Baixando: {self.url}')
		# O servidor não informou o tamanho total do arquivo
		# baixar sem barra de progresso com 'requests'
		if total_length is None:
			try:
				wget.download(self.url, self.file)
				print(' OK')
			except(KeyboardInterrupt):
				print()
				p.red('Interrompido com Ctrl c') 
				sleep(0.2)
				if path.isfile(self.file): 
					remove(self.file)
					exit()
			except:
				print()
				p.red('Falha no download')
				if path.isfile(self.file):
					remove(self.file)

		else:
			# O servidor informou o tamanho do arquivo para download
			# baixar com wget.download()
			try:
				wget.download(self.url, self.file, bar=self.bar_custom)
				print('OK ')
			except(KeyboardInterrupt):
				print()
				p.red('Interrompido com Ctrl c') 
				sleep(0.2)
				if path.isfile(self.file): 
					remove(self.file)
					exit()
			except:
				print()
				p.red('Falha no download')
				if path.isfile(self.file):
					remove(self.file)

		


