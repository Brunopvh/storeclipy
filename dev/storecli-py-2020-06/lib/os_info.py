#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# from os_info import *
# os_id = OsInfo.get_os_id
#
#

import os
import platform

# Versão python 3.6 ou superior
if platform.python_version() < '3.6':
	print('\033[0;31m[!] Necessário ter python 3.6 ou superior instalado em seu sistema\033[m')
	exit()

# Linux ou FreeBSD
if (platform.system() != 'Linux') and (platform.system() != 'FreeBSD'):
	print('Use esse módulo em Linux ou FreeBSD')
	exit()

# Verificar o caminho do arquivo os-release
if os.path.isfile('/usr/lib/os-release'):
	file_release = open('/usr/lib/os-release', 'rt').readlines()
elif os.path.isfile('/usr/local/etc/os-release'):
	file_release = open('/usr/local/etc/os-release', 'rt').readlines()
else:
	print('\033[0;31m[!] Arquivo os-release não encontrado, saindo\033[m')
	exit()

class OsInfo:
	
	def __init__(self, file_release=file_release):
		self.file_release = file_release # Arquivo que content informações do sistema, geralmente '/etc/os-release'
		self.dict_release = dict_release = {} # Dicionario com os dados do arquivo os-release.

		# inserir no dicionário os dados mais relevantes sobre o sistema.
		for x in file_release:
			x = x.replace('\n', '')
			x = str(x)
			x = x.replace('"', '').replace(' ', '')

			# Inserir cada informação relevante no dicionario.
			if x[0:3] == 'ID=':                        # ID
				x = x.replace('ID=', '')
				self.dict_release['os_id'] = x
			elif x[0:11] == 'VERSION_ID=':             # VERSION_ID
				x = x.replace('VERSION_ID=', '')
				self.dict_release['os_version_id'] = x
			elif x[0:8] == 'ID_LIKE=':                 # ID_LIKE
				x = x.replace('ID_LIKE=', '')
				self.dict_release['os_id_like'] = x
			elif x[0:8] == 'VERSION=':                 # VERSION
				x = x.replace('VERSION=', '')  
				self.dict_release['os_version'] = x
			elif x[0:17] == 'VERSION_CODENAME=':       # VERSION_CODENAME
				x = x.replace('VERSION_CODENAME=', '')
				self.dict_release['os_codename'] = x
			elif x[0:5] == 'NAME=':                    # NAME
				x = x.replace('NAME=', '')
				self.dict_release['os_name'] = x

	def get_os_id(self):
		if 'os_id' in self.dict_release:
			os_id = self.dict_release['os_id']
		else:
			os_id = 'NoNe'

		return os_id

	def get_os_codename(self):
		if 'os_codename' in self.dict_release:
			os_codename = self.dict_release['os_codename']
		else:
			os_codename = 'NoNe'

		return os_codename

	def get_os_version_id(self):
		if 'os_version_id' in self.dict_release:
			os_version_id = self.dict_release['os_version_id']
		else:
			os_version_id = 'NoNe'

		return os_version_id

	def get_os_id_like(self):
		if 'os_id_like' in self.dict_release:
			os_id_like = self.dict_release['os_id_like']
		else:
			os_id_like = 'NoNe'

		return os_id_like

	def get_os_version(self):
		if 'os_version' in self.dict_release:
			os_version = self.dict_release['os_version']
		else:
			os_version = 'NoNe'

		return os_version

	def get_os_name(self):
		if 'os_name' in self.dict_release:
			os_name = self.dict_release['os_name']
		else:
			os_name = 'NoNe'

		return os_name

	def get_os_kernel(self):
		return platform.system()



