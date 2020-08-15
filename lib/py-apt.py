#!/usr/bin/env python3
#
# https://stackoverflow.com/questions/17537390/how-to-install-a-package-using-the-python-apt-api

import apt
import sys
import os

# root
if os.geteuid() != int('0'):
	print('[!] Você precisa ser o "root"')
	sys.exit('1')

columns = os.get_terminal_size(0)[0]
line = ('=' * columns)

#import lsb_release
#print(lsb_release.get_distro_information()['ID'])

class AptGet:
	def __init__(self):
		print(line)
		self.cache = apt.cache.Cache()
		print('Carregando cache aguarde...')
		self.cache.update()
		print('Lendo o cache')
		self.cache.open()

	def install_pkg(self, package):
		pkg = self.cache[package]
		
		if pkg.is_installed:
			print(f"[+] {package} Já está instalado")
		else:
			print(f'Instalando: {package}')
			pkg.mark_install()

			try:
				self.cache.commit()
				print('OK')
			except Exception as e:
				print(line)
				print('[!] Falha na instalação')
				print(e)

	def install(self, apps_list):
		for APP in apps_list:
			self.install_pkg(APP)

if __name__ == '__main__':
	AptGet().install(sys.argv[1:])


