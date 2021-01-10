#!/usr/bin/env python3
#
# python3 -c "$(curl -fsSL https://raw.github.com/Brunopvh/storeclipy/master/setup.py)"

__version__ = '2021-01-10'

import os, sys
import argparse
from shutil import copytree

_script_installer = os.path.abspath(os.path.realpath(__file__))
dir_of_project = os.path.dirname(_script_installer)

os.chdir(dir_of_project)
from lib import utils 

URL_STORECLIPY='https://github.com/Brunopvh/storeclipy/archive/master.tar.gz'

class InstallStorecliUser(utils.SetUserConfig, utils.PrintText):
	def __init__(self):
		super().__init__(utils.appname)
		self.pkg_storecli = os.path.abspath(os.path.join(self.dir_temp, 'storecli.tar.gz'))
		self.destination_storecli = os.path.abspath(os.path.join(self.dir_bin, 'storeclipy-amd64'))
		self.destination_storecli_link = os.path.abspath(os.path.join(self.dir_bin, 'storeclipy'))
		self.destination_storecli_bin = os.path.abspath(os.path.join(self.destination_storecli, 'storecli.py'))
		self.unpack_files = utils.Unpack(destination=self.dir_unpack, clear_dir=True)

		if os.path.isdir(self.destination_storecli) == True:
			utils.rmdir(self.destination_storecli)

	def install_storecli_online_version_linux(self):
		utils.DownloadFiles().wget_download(URL_STORECLIPY, self.pkg_storecli)
		self.unpack_files.tar(self.pkg_storecli)
		os.chdir(self.dir_unpack)
		dirs = os.listdir(self.dir_unpack)
		for d in dirs:
			if 'storecli' in d:
				storecli_temp_dir = d
				break

		print(f'Copiando arquivos para ... {self.destination_storecli}', end=' ')
		try:
			copytree(storecli_temp_dir, self.destination_storecli)
		except Exception as err:
			self.red('')
			self.sred(err)
			sys.exit(1)
		else:
			print('OK')
		self.create_link_exec()

	def install_storecli_local(self):
		os.chdir(dir_of_project)
		print(f'Copiando ... {dir_of_project}')
		copytree(dir_of_project, self.destination_storecli)
		self.create_link_exec()

	def create_link_exec(self):
		print('Criando atalho para execução.')
		os.chdir(self.destination_storecli)
		os.system(f'chmod -R +x {self.destination_storecli}')
		os.system(f'ln -sf {self.destination_storecli_bin} {self.destination_storecli_link}')

	def run(self, online=False):
		if utils.KERNEL_TYPE == 'Linux':
			if online == False:
				self.install_storecli_local()
			else:
				self.install_storecli_online_version_linux()
			
		elif utils.KERNEL_TYPE == 'Windows':
			pass

'''
parser = argparse.ArgumentParser(
            description='Instala programas em sistemas Linux e FreeBSD.'
            )

parser.add_argument(
    '-v', '--version', 
    action='version', 
    version=(f"%(prog)s {__version__}")
    )

parser.add_argument(
    '-i', '--install',
    action='store_true', 
    dest='install_storecli', # Argumento que não será passado para opção -l/--list.
    help='Instala o script storecli no sistema.'
    )

parser.add_argument(
    '-u', '--uninstall',
    action='store_true', 
    dest='uninstall_storecli', # Argumento que não será passado para opção -l/--list.
    help='Desinstala o script storecli no sistema.'
    )


args = parser.parse_args()
'''

if (len(sys.argv) == 1):
	InstallStorecliUser().run(online=True)
else:
	if (sys.argv[1] == 'install'):
		print('Aguarde')
		InstallStorecliUser().run()
	elif (sys.argv[1] == 'uninstall'):
		pass