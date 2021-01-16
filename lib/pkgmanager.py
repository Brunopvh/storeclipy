#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import urllib.request
from subprocess import getstatusoutput
from time import sleep
from utils import PrintText, DownloadFiles, is_root # Módulo local.

class ProcessLoop(PrintText):
	def __init__(self, pid=''):
		self.pid = str(pid)
		self.chars = ('-', '\\', '|', '/')
		self.process_list = []

	def get_process_list(self):
		'''
		Obter uma lista com todos os processos em execução no sistema
		essa lista será inserida na variável self.process_list
		'''
		self.process_list = [] # Limpar o conteúdo da variável em cada chamada.
		all_process = getstatusoutput('ps aux')[1].split('\n')
		for i in all_process:
			self.process_list.append(i) 
		return self.process_list

	def process_loop(self):
		'''
		Exibir um loop enquando o processo self.pid existir no sistema operacional.
		'''
		p = self.get_process_list() # Obter a lista de processos.
		for line in p:
			proc = line.split()[1]
			if self.pid == proc:
				is_pid = True
				break
			else:
				is_pid = False
		
		if is_pid == False:
			self.sred(f'O processo com PID ({self.pid}) não está em execução.')
			sleep(0.15)
			return

		num = int(0)
		while True:
			p = self.get_process_list()
			for proc in p:
				proc = proc.split()
				if self.pid in proc[1]:
					is_pid = True
					break
				else:
					is_pid = False

			if is_pid == False:
				print(f'Aguardando processo com pid ({self.pid}) \033[0;33mfinalizado\033[m [{self.chars[num]}]')
				sleep(0.15)
				break
				return
			else:
				print(f'\033[KAguardando processo com pid ({self.pid}) finalizar [{self.chars[num]}]', end='\r')
				sleep(0.15)

			if num == int(3):
				num = int(-1)
			num += 1
			

class AptGet(PrintText):

	def __init__(self):
		super().__init__()

	def apt_process_loop(self):
		'''
		Criar um loop para bloquear a instalação do apt se outro processo apt já estiver
		em execução no sistema.
		'''
		all_procs = ''
		
		while True:
			all_procs = ProcessLoop().get_process_list()
			for P in all_procs:
				if ('apt install' in P) or ('_apt' in P) or ('apt update' in P) or ('apt remove' in P):
					pid_apt = P.split()[1] # Converter a linha de saída em lista e retornar o segundo item.
					sleep(0.15)
					break
				else:
					pid_apt = None

			if pid_apt == None:
				break
			else:				
				ProcessLoop(pid_apt).process_loop()

	def broke(self):
		self.apt_process_loop()
		commands = (
			'sudo dpkg --configure -a',
			'sudo apt clean',
			'sudo apt remove',
			'sudo apt update',
			'sudo apt install -y -f',
			'sudo apt-get --fix-broken install'
			)

		for c in commands:
			print(f'Executando ... {c}')
			os.system(c)

	def remove(self, pkgs):
		self.apt_process_loop() # Verificar se existe outro processo 'apt' em execução no sistema.
		if isinstance(pkgs, list):
			for app in pkgs:
				self.print_line()
				print(f'Removendo ... {app}')
				self.print_line()
				os.system(f'sudo apt remove {app}')
		elif isinstance(pkgs, str):
			self.print_line()
			print(f'Removendo ... {pkgs}')
			self.print_line()
			os.system(f'sudo apt remove {pkgs}')
				
	def install(self, pkgs):
		self.apt_process_loop() # Verificar se existe outro processo 'apt' em execução no sistema.
		if isinstance(pkgs, list):
			for app in pkgs:
				self.print_line()
				print(f'Instalando ... {app}')
				self.print_line()
				os.system(f'sudo apt install {app}')
		elif isinstance(pkgs, str):
			self.print_line()
			print(f'Instalando ... {pkgs}')
			self.print_line()
			os.system(f'sudo apt install {pkgs}')

	def update(self):
		self.apt_process_loop()
		self.print_line()
		print('Executando: sudo apt update')
		os.system('sudo apt update')

	def key_add(self, content_key: str) -> bool:
		'''
		content_key = arquivo ou url de uma chave.
		Recebe um arquivo ou um url contendo uma chave para ser adicionada no sistema.
		'''
		if is_root() == False:
			return False

		if os.path.isfile(content_key) == True:
			os.system(f'sudo apt-key add {content_key}')
		else: 
			RegExp = re.compile(r'^http:|^ftp:|^https|^www')
			if RegExp.findall(content_key) == []:
				print(f'Erro: url inválida.')
				return False

			# Obter key apartir do url.
			import tempfile
			apt_temp_file = tempfile.NamedTemporaryFile(delete=True).name
			try:
				#urllib.request.urlretrieve(content_key, apt_temp_file)
				DownloadFiles().downloader(content_key, apt_temp_file)
			except:
				self.red('Falha')
				return False
			else:
				os.system(f'sudo apt-key add {apt_temp_file}')
				return True

			if os.path.isfile(apt_temp_file) == True:
				utils.rmdir(apt_temp_file)



class Pacman(PrintText):
	def __init__(self):
		super().__init__()
			
	def pkg_is_list(self, pkgs):
		'''
		Verificar se os pacotes foram passados para classe em forma de lista
		'''
		if isinstance(pkgs, list): 
			return 'True'
		else:
			print('\033[0;31mFalha o(s) pacotes para instalação precisam ser passados em forma de uma lista.\033[m') 
			print(__class__)
			return 'False'
	
	def pacman_process_loop(self):
		all_procs = ' '
		
		while True:
			all_procs = ProcessLoop().get_process_list()
			for P in all_procs:
				if ('pacman -S' in P) or ('pacman -U' in P):
					pid_pacman = P.split()[1] # Converter a linha de saída em lista e retornar o segundo item.
					sleep(0.1)
					break
				else:
					pid_pacman = None

			if pid_pacman == None:
				break
			else:				
				ProcessLoop(pid_pacman).process_loop()
				
	def install(self, pkgs):
		self.pacman_process_loop() # Verificar se existe outro processo 'apt' em execução no sistema.
		self.print_line()
		print(f'Instalando: {pkgs}')			
		self.print_line()
		os.system(f'sudo pacman -S --needed {pkgs}')

	def update(self):
		self.pacman_process_loop()
		print('Executando: sudo pacman -Sy')
		os.system('sudo pacman -Sy')
