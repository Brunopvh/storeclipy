#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from os import system
from lib.sys_process import ShowProcessLoop
from lib.colors import PrintText as p

class PkgManager:

	def __init__(self, pkgs='False'):
		self.pkgs = pkgs
			
	def pkg_is_list(self):
		if isinstance(self.pkgs, list): 
			return 'True'
		else:
			p.red('Falha o(s) pacotes para instalação precisam ser passados em forma de uma lista.') 
			print(__class__)
			return 'False'

	def pacman(self, argument):
		if self.pkg_is_list() != 'True':
			return

		if argument == '-S':
			for i in self.pkgs:
				yellow(f'Instalando: {i}')
				system(f'sudo pacman -S --needed --noconfirm {i}')

	def apt(self, argument):
		if self.pkg_is_list() != 'True':
			return

		ShowProcessLoop('apt').apt_process_loop()

		if argument == 'install':
			for i in self.pkgs:
				p.yellow(f'Instalando: {i}')
				system(f'sudo apt install -y {i}')
		elif argument == '--no-install-recommends':
			for i in self.pkgs:
				p.yellow(f'Instalando: {i}')
				system(f'sudo apt install -y --no-install-recommends {i}')
		elif argument == 'remove':
			for i in self.pkgs:
				system(f'sudo apt remove {i}')

	def dnf(self, argument):
		if self.pkg_is_list() != 'True':
			return

		if argument == 'install':
			for i in self.pkgs:
				p.yellow(f'Instalando: {i}')
				system(f'sudo dnf install -y {i}')




