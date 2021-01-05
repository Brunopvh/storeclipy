#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import utils # Módulo local
import pkgmanager # Módulo local
from time import sleep

REQUERIMENTS_CLI_LINUX = ['curl', 'gpg', 'git', 'xterm',]
REQUERIMENTS_CLI_DEBIAN = ['dirmngr', 'apt-transport-https', 'python3-pip', 'python3-setuptools']

class ConfigureCliRequeriments(utils.PrintText):
	def __init__(self):
		super().__init__()
		self.user_config = utils.SetUserConfig(utils.appname)
		self.obj_file_config = utils.ReadFile(self.user_config.file_config)
		self.os_release = utils.ReleaseInfo().get('ALL')

	def install_requeriments(self):
		if self.os_release['ID'] == 'debian':
			pkgmanager.AptGet().install(REQUERIMENTS_CLI_LINUX)
			pkgmanager.AptGet().install(REQUERIMENTS_CLI_DEBIAN)
			pass
		elif (self.os_release['ID'] == 'ubuntu') or (self.os_release['ID'] == 'linuxmint'):
			pass
		elif self.os_release['ID'] == 'fedora':
			pass
		elif self.os_release['ID'] == 'arch':
			pass
		elif self.os_release['ID'] == 'FreeBSD':
			pass

		self.user_config.config_bashrc()
		
		# Gravar 'requeriments=OK' no arquivo de configuração
		content = self.obj_file_config.string_in_file('requeriments=OK')
		if (content != []) and (content[0] == 'requeriments=OK'):
			return True
	
		content = self.obj_file_config.read_file()
		content.append('requeriments=OK')
		self.obj_file_config.write_file(content)

	def check_all_requeriments(self):
		'''
		Verificar dependências e instalar se nescessário.
		'''
		if os.path.isfile(self.user_config.file_config) == True:
			content = self.obj_file_config.string_in_file('requeriments=OK')
			if (content != []) and (content[0] == 'requeriments=OK'):
				return True

		self.install_requeriments()
