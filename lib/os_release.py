#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os, sys
import platform


if platform.system() != 'Linux':
	print('Seu sistema não é Linux - saindo...')
	sys.exit()

if os.path.isfile('/etc/os-release') == True:
	release_file = '/etc/os-release'
elif os.path.isfile('/usr/lib/os-release') == True:
	release_file = '/usr/lib/os-release'
else:
	print('Arquivo os-release não encontrado - saindo...')
	sys.exit()


class ReleaseInfo:
	def __init__(self):
		self.release_file = release_file

	def get_lines(self):
		f = open(self.release_file, 'rt')
		Lines = [] 
		for L in f.readlines():
			L = L.replace('\n', '').replace('"', '')
			Lines.append(L)

		f.close()
		return Lines

	def get_info(self):
		lines = self.get_lines()
		RELEASE_INFO = {'kernel_type': 'Linux'}

		for LINE in lines:
			if LINE[0:12] == 'PRETTY_NAME=':
				LINE = LINE.replace('PRETTY_NAME=', '')
				RELEASE_INFO.update({'PRETTY_NAME': LINE})

			elif LINE[0:5] == 'NAME=':
				LINE = LINE.replace('NAME=', '')
				RELEASE_INFO.update({'NAME': LINE})

			elif LINE[0:11] == 'VERSION_ID=':
				LINE = LINE.replace('VERSION_ID=', '')
				RELEASE_INFO.update({'VERSION_ID': LINE})

			elif LINE[0:8] == 'VERSION=':
				LINE = LINE.replace('VERSION=', '')
				RELEASE_INFO.update({'VERSION': LINE})

			elif LINE[0:17] == 'VERSION_CODENAME=':
				LINE = LINE.replace('VERSION_CODENAME=', '')
				RELEASE_INFO.update({'VERSION_CODENAME': LINE})

			elif LINE[0:3] == 'ID=':
				LINE = LINE.replace('ID=', '')
				RELEASE_INFO.update({'ID': LINE})

		return RELEASE_INFO

	def show_all(self):
		RELEASE_INFO = self.get_info()
		for i in RELEASE_INFO:
			print(i, '=>', RELEASE_INFO[i])

	def info(self, type_info):
		RELEASE_INFO = self.get_info()

		if type_info == 'ALL':
			return RELEASE_INFO

		if type_info in RELEASE_INFO.keys():
			return str(RELEASE_INFO[type_info]) 
		else:
			return 'False'


if __name__ == '__main__':
	# ReleaseInfo().show_all()
	if (len(sys.argv)) >= int('2'):
		for info in sys.argv[1:]:
			i = ReleaseInfo().info(info)
			print(i)
	