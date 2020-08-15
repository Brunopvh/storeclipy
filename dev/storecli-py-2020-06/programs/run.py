#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil

from programs.downloadonly_files import DownloadOnlyFiles
from programs.wireless import WirelessTools
from programs.web import WebTools

#================================================================#
# Instalação dos programas
#================================================================#
class RunInstaller:

	def is_executable(self, executable):
		e = int(subprocess.getstatusoutput(f'which {executable} 2> /dev/null')[0])

		if e == int('0'):
			return 'True' # Existe
		else: 
			return 'False' # Não existe

	def wifiphisher(self):
		'''
		https://github.com/wifiphisher/wifiphisher
		'''
		WirelessTools().wifiphisher()

	def fluxion(self):
		'''
		https://github.com/FluxionNetwork/fluxion
		https://www.tutorialspoint.com/python3/os_chmod.htm
		'''
		WirelessTools().fluxion()
		

	def theHarvester(self):
		'''
		https://github.com/laramies/theHarvester
		https://github.com/laramies/theHarvester/wiki/Installation
		'''
		WebTools().theHarvester()

	def searx(self):
		'''
		https://github.com/th3sha10wbr04rs/SearX_easy_Installer
		https://github.com/asciimoo/searx
		'''
		WebTools().searx()
