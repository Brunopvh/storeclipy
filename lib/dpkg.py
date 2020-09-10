#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
import subprocess
from time import sleep

columns = os.get_terminal_size()[0]
line = ('-' * columns)

class ProcessLoop:
	def __init__(self, pid=''):
		self.pid = pid
		self.chars = ('-', '\\', '|', '/')
		self.process_list = []

	def get_process_list(self):
		'''
		Obter uma lista com todos os processos em execução no sistema
		essa lista sera inserida na variável self.process_list
		'''
		self.process_list = [] 
		all_process = subprocess.getstatusoutput('ps aux')[1].split('\n')
		for i in all_process:
			self.process_list.append(i) 

		return self.process_list

	def process_loop(self):
		PROCESS = self.get_process_list()
		for proc in PROCESS:
			proc = proc.split()
			if self.pid in proc[1]:
				is_pid = 'True'
				break
			else:
				is_pid = 'False'

		if is_pid == 'False':
			print(f'O processo com PID ({self.pid}) não está em execução.')
			sleep(0.15)
			return

		num = int('0')
		while True:
			PROCESS = self.get_process_list()
			for proc in PROCESS:
				proc = proc.split()
				if self.pid in proc[1]:
					is_pid = 'True'
					break
				else:
					is_pid = 'False'

			if is_pid == 'False':
				print(f'Aguardando processo com pid ({self.pid}) \033[0;33mfinalizado\033[m [{self.chars[num]}]')
				sleep(0.1)
				break
				return
			else:
				print(f'\033[KAguardando processo com pid ({self.pid}) finalizar [{self.chars[num]}]', end='\r')
				sleep(0.15)

			if num == int('3'):
				num = int('-1')
			num += 1
			

class Dpkg:

	def __init__(self):
		pass
			
	def apt_process_loop(self):
		all_procs = ' '
		
		while True:
			all_procs = ProcessLoop().get_process_list()
			for P in all_procs:
				if ('dpkg --install' in P) or ('dpkg -i' in P) or ('apt install' in P) or ('apt remove' in P):
					pid_dpkg = P.split()[1] # Converter a linha de saída em lista e retornar o segundo item.
					sleep(0.1)
					break
				else:
					pid_dpkg = None

			if pid_dpkg == None:
				break
			else:				
				ProcessLoop(pid_dpkg).process_loop()
				
	def install(self, deb_package):
		self.apt_process_loop() # Verificar se existe outro processo 'apt' em execução no sistema.
		print(line)
		print(f'Executando ... sudo dpkg --install {deb_package}')			
		print(line)
		os.system(f'sudo dpkg --install {deb_package}')

if __name__ == '__main__':
	Dpkg().install(sys.argv[1:])
	


   
        

