#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import utils # Módulo local
import pkgmanager # Módulo local
from time import sleep
from shutil import which, copytree

REQUERIMENTS_CLI_LINUX = ['curl', 'gpg', 'git', 'xterm',]
REQUERIMENTS_CLI_DEBIAN = ['dirmngr', 'apt-transport-https', 'python3-pip', 'python3-setuptools']

class ConfigureCliRequeriments(utils.SetUserConfig, utils.PrintText):
	def __init__(self):
		super().__init__(utils.appname)
		self.obj_file_config = utils.ReadFile(self.file_config)
		self.os_release = utils.ReleaseInfo().get('ALL')
		self.unpack_files = utils.Unpack(self.dir_unpack, clear_dir=True)

	def check_all_requeriments(self):
		'''
		Verificar dependências e instalar se nescessário.
		'''
		for r in REQUERIMENTS_CLI_LINUX:
			print(r, end=' ')
			if (which(r) == None):
				self.red('')
				self.print_line()
				self.install_requeriments()
				break
			else:
				self.green('')

		if os.path.isfile(self.file_config) == True:
			content = self.obj_file_config.string_in_file('requeriments=OK')
			if (content != []) and (content[0] == 'requeriments=OK'):
				return True

		self.install_requeriments()

	def configure_win64(self):
		url_download_curl_win64 = 'https://curl.se/windows/dl-7.74.0_2/curl-7.74.0_2-win64-mingw.zip'
		pkg_name = os.path.basename(url_download_curl_win64)
		path_curl_zipfile = os.path.abspath(os.path.join(self.dir_cache, pkg_name))
		utils.DownloadFiles().downloader(url_download_curl_win64, path_curl_zipfile)
		self.unpack_files.zip(path_curl_zipfile)
		RegexDir = re.compile(r'^curl-.*win64')
		dirs = os.listdir(self.dir_unpack)
		for d in dirs:
			if RegexDir.findall(d) != []:
				dir_temp_curl = d
				break

		destination_curl = os.path.abspath(os.path.join(self.dir_bin, 'curl-win64'))
		print(f'Instalando curl em ... {destination_curl}', end=' ')
		try:
			copytree(dir_temp_curl, destination_curl, symlinks=True, ignore=None)
		except:
			self.red('')
			return False
		else:
			print('OK')

	def install_requeriments(self):
		if utils.KERNEL_TYPE == 'Linux':
			if self.os_release['ID'] == 'debian':
				self.configure_win64(); return
				pkgmanager.AptGet().update()
				pkgmanager.AptGet().install(REQUERIMENTS_CLI_LINUX)
				pkgmanager.AptGet().install(REQUERIMENTS_CLI_DEBIAN)
			elif (self.os_release['ID'] == 'ubuntu') or (self.os_release['ID'] == 'linuxmint'):
				pass
			elif self.os_release['ID'] == 'fedora':
				pass
			elif self.os_release['ID'] == 'arch':
				pass

			self.config_bashrc()
		elif utils.KERNEL_TYPE == 'FreeBSD':
				pass
		elif util.KERNEL_TYPE == 'Windows':
			self.configure_win64()

		# Gravar 'requeriments=OK' no arquivo de configuração.
		content = self.obj_file_config.string_in_file('requeriments=OK')
		if (content != []) and (content[0] == 'requeriments=OK'):
			return True
	
		content = self.obj_file_config.read_file()
		content.append('requeriments=OK')
		self.obj_file_config.write_file(content)
		return True

	
