#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import platform
import re
import getpass
import shutil
import tempfile
import tarfile
import urllib.request
import subprocess
import progressbar # Externo
from pathlib import Path
from bs4 import BeautifulSoup # Externo

# Default
CRed = '\033[0;31m'
CGreen = '\033[0;32m'
CYellow = '\033[0;33m'
CBlue = '\033[0;34m'
CWhite = '\033[0;37m'
CReset = '\033[m'

# Strong
CSRed = '\033[1;31m'
CSGreen = '\033[1;32m'
CSYellow = '\033[1;33m'
CSBlue = '\033[1;34m'
CSWhite = '\033[1;37m'

KERNEL_TYPE = platform.system()
appname = 'storecli-python'

user_agents = [
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
]

if KERNEL_TYPE == 'Windows':
	user_agent = user_agents[0]
elif KERNEL_TYPE == 'Linux':
	user_agent = user_agents[1]
else:
	user_agent = user_agents[2]

try:
	COLUMNS = int(os.get_terminal_size()[0])
except:
	COLUMNS = int(45)

class PrintText:
	def __init__(self):
		pass

	def print_line(self, char='-'):
		print(char * COLUMNS)

	def msg(self, text=''):
		self.print_line()
		print(text.center(COLUMNS))
		self.print_line()

	def printf(self, text=''):
		print(f'{text}')

	def red(self, text=''):
		print(f'{CRed}[!] {text}{CReset}')

	def green(self, text=''):
		print(f'{CGreen}{text}{CReset}')

	def yellow(self, text=''):
		print(f'{CYellow}{text}{CReset}')

	def blue(self, text=''):
		print(f'{CBlue}{text}{CReset}')

	def white(self, text=''):
		print(f'{CWhite}{text}{CReset}')

	# Strong
	def sred(self, text=''):
		print(f'{CSRed}{text}{CReset}')

	def sgreen(self, text=''):
		print(f'{CSGreen}{text}{CReset}')

	def syellow(self, text=''):
		print(f'{CSYellow}{text}{CReset}')

	def sblue(self, text=''):
		print(f'{CSBlue}{text}{CReset}')

	def swhite(self, text=''):
		print(f'{CSWhite}{text}{CReset}')

	# Dark
	def dred(self, text=''):
		print(f'{CDRed}{text}{CReset}')

	def dgreen(self, text=''):
		print(f'{CDGreen}{text}{CReset}')

	def dyellow(self, text=''):
		print(f'{CDYellow}{text}{CReset}')

	def dblue(self, text=''):
		print(f'{CDBlue}{text}{CReset}')

	def dwhite(self, text=''):
		print(f'{CDWhite}{text}{CReset}')

#=====================================================#

def mkdir(path):
	if path == '':
		return False

	if os.path.exists(path):
		print(f'mkdir: Arquivo ou diretório já existe ... {path}')
		if os.path.isdir(path):
			return True
		else:
			return False

	print(f'Criando diretório ... {path}', end=' ')
	try:
		os.makedirs(path)
	except:
		print('{}Erro{}'.format(CRed, CReset))
		return False
	else:		
		if not os.access(path, os.W_OK):
			print()
			print("mkdir: Você não tem permissão de escrita em ... {}".format(path))
			return False

	print('OK')
	return True 

#=====================================================#

def rmdir(path):
	if os.path.exists(path) == False:
		return False

	print(f'Apagando ... {path}', end=' ')
	try:
		shutil.rmtree(path)
	except:
		print(f'{CRed}Erro{CReset}')
		return False
	else:
		print('OK')
		return True

#=====================================================#

def is_executable(app_executable: str) -> bool:
	OutPut = subprocess.getstatusoutput(f'command -v {app_executable}')
	if OutPut[0] == int(0):
		return True
	else:
		return False

#=====================================================#

class ReadFile(PrintText):
	def __init__(self, file: str):
		self.file = file

	def read_file(self) -> list:
		'''
		Ler um arquivo e retornar as linhas em forma de lista.
		'''
		if os.path.isfile(self.file) == False:
			self.red(f'read_file: Erro arquivo não encontrado.')
			return None

		try:
			with open(self.file, 'rt') as f:
				lines = f.read().split('\n')
		except:
			print(f'read_file: Erro na leitura do arquivo {self.file}')
			return []
		else:
			return lines

	def write_file(self, content: list) -> bool:
		'''
		Recebe uma lista é grava o contéudo da lista
		no arquivo que será aberto em MODO 'w'. 
		
		OBS: 
	       - Quebras de linha são adicionadas ao fim de cada elemento da lista.
	       - Se o arquivo 'file' já existir a função será encerrada.
		'''
		print(f'write_file: gravando dados no arquivo ... {self.file}', end=' ')
		try:
			with open(self.file, 'w') as f:
				for L in content:
					if L != '':
						f.write(f'{L}\n')
		except:
			self.red(f'Erro')
			return False
		else:
			print('OK')
			return True

	def string_in_file(self, string: str, case_sensitive=True) -> list:
		'''
		Verifica se uma string existe em um arquivo de texto e retorna as ocorrências
		encontradas no arquivo, se a string não existir nas linhas do arquivo, retorna
		uma lista vazia [].
		'''
		if os.path.isfile(self.file) == False:
			self.red(f'string_in_file: Erro arquivo não existe {self.file}')
			return []

		try:
			content = self.read_file()
		except:
			self.red(f'{__class__.__name__} string_in_file: Erro na leitura do arquivo {self.file}')
			return []
		else:
			if content == False:
				self.red(f'string_in_file: erro na leitura do arquivo ... {file}')
				return []

		ContentMath = []
		if case_sensitive == False: 
			string = string.lower()

		RegExp = re.compile(r'{}'.format(string))
		for line in content:
			if case_sensitive == False:
				NewLine = line.lower()
			else:
				NewLine = line

			if (RegExp.findall(NewLine) != []):
				ContentMath.append(NewLine)
		return ContentMath
			
#=====================================================#

class SetUserConfig:

	def __init__(self, appname, create_dirs=True):
		self.kernel_type = KERNEL_TYPE
		self.appname = appname
		if self.kernel_type == 'FreeBSD':
			self.dir_home = os.path.abspath(os.path.join('/usr', Path.home()))
		else:
			self.dir_home = Path.home()

		if (self.kernel_type == 'Linux') or (self.kernel_type == 'FreeBSD'):
			self.dir_bin = os.path.abspath(os.path.join(self.dir_home, '.local', 'bin'))
			self.dir_desktop_links = os.path.abspath(os.path.join(self.dir_home, '.local', 'share', 'applications'))
			self.dir_cache = os.path.abspath(os.path.join(self.dir_home, '.cache', self.appname))
			self.dir_config = os.path.abspath(os.path.join(self.dir_home, '.config', self.appname))
			self.file_config = os.path.abspath(os.path.join(self.dir_config, f'{self.appname}.conf'))
		elif self.kernel_type == 'Windows':
			self.dir_bin = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'Local', 'Programs', self.appname))
			self.dir_desktop_links = ''
			self.dir_cache = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'LocalLow', self.appname))
			self.dir_config = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'Roaming', self.appname))
			self.file_config = os.path.abspath(os.path.join(self.dir_config, f'{self.appname}.conf'))	
				
		self.file_temp = tempfile.NamedTemporaryFile(delete=True).name
		# self.dir_temp = tempfile.TemporaryDirectory().name
		if (self.kernel_type == 'Linux') or (self.kernel_type == 'FreeBSD'):
			self.dir_temp = os.path.abspath(os.path.join('/tmp', f'{self.appname}-{getpass.getuser()}'))
		elif self.kernel_type == 'Windows':
			self.dir_temp = os.path.abspath(os.path.join('C:', f'{self.appname}-{getpass.getuser()}'))

		self.user_info = {
			'home': self.dir_home,
			'cache': self.dir_cache,
			'config': self.dir_config,
			'bin': self.dir_bin,
			'desktop_links': self.dir_desktop_links,
			'dir_temp': self.dir_temp,
			}

		if create_dirs == True:
			for key in self.user_info:
				d = self.user_info[key]
				if os.path.isdir(d) == False:
					mkdir(d)
		
	def get_user_info(self):
		return self.user_info

	def config_bashrc(self):
		'''
		Configurar o arquivo .bashrc do usuário para inserir o diretório ~/.local/bin
		na variável de ambiente $PATH. Essa configuração será abortada caso ~/.local/bin já 
		exista em ~/.bashrc.
		'''
		if self.kernel_type != 'Linux':
			self.red(f'Seu sistema não é Linux.')
			return False

		# Verificar se ~/.local/bin já está no PATH do usuário atual.
		user_local_path = os.environ['PATH']
		if self.dir_bin in user_local_path:
			pass #return True

		file_bashrc = os.path.abspath(os.path.join(self.dir_home, '.bashrc'))
		file_bashrc_backup = os.path.abspath(os.path.join(self.dir_home, f'.bashrc.pre-{self.appname}'))
		if os.path.isfile(file_bashrc_backup) == False:
			shutil.copyfile(file_bashrc, file_bashrc_backup)

		obj_bashrc = ReadFile(file_bashrc)
		content_bashrc = obj_bashrc.string_in_file('^export PATH=')

		if (content_bashrc != []) and (self.dir_bin in content_bashrc[0]):
			return True

		content_bashrc = obj_bashrc.read_file()
		RegExp = re.compile(r'^export PATH=')
		num = 0
		for line in content_bashrc:
			if (RegExp.findall(line) != []):
				line = f'# {line}'
				content_bashrc[num] = line
			num += 1
				
		NewUserPath = f'export PATH={self.dir_bin}:{user_local_path}'
		content_bashrc.append(NewUserPath)
		os.remove(file_bashrc)
		obj_bashrc.write_file(content_bashrc)

#=====================================================#

class ReleaseInfo(object):
	def __init__(self):
		if os.path.isfile('/etc/os-release') == True:
			release_file = '/etc/os-release'
		elif os.path.isfile('/usr/lib/os-release') == True:
			release_file = '/usr/lib/os-release'
		elif os.path.isfile('/usr/local/etc/os-release') == True:
		    release_file = '/usr/local/etc/os-release'
		else:
			print(f'{__class__}: arquivo release não encontrado.')
			return False

		self.obj_reslease_file = ReadFile(release_file) 
		self.release_os_info = {}

	def get_info(self):
		'''
		Obter as informações do sistema contidas no arquivo /etc/os-release.
		'''
		lines = self.obj_reslease_file.read_file()

		for LINE in lines:
			if LINE[0:12] == 'PRETTY_NAME=':
				LINE = LINE.replace('PRETTY_NAME=', '')
				self.release_os_info.update({'PRETTY_NAME': LINE})

			elif LINE[0:5] == 'NAME=':
				LINE = LINE.replace('NAME=', '')
				self.release_os_info.update({'NAME': LINE})

			elif LINE[0:11] == 'VERSION_ID=':
				LINE = LINE.replace('VERSION_ID=', '')
				self.release_os_info.update({'VERSION_ID': LINE})

			elif LINE[0:8] == 'VERSION=':
				LINE = LINE.replace('VERSION=', '')
				self.release_os_info.update({'VERSION': LINE})

			elif LINE[0:17] == 'VERSION_CODENAME=':
				LINE = LINE.replace('VERSION_CODENAME=', '')
				self.release_os_info.update({'VERSION_CODENAME': LINE})

			elif LINE[0:3] == 'ID=':
				LINE = LINE.replace('ID=', '')
				self.release_os_info.update({'ID': LINE})

		return self.release_os_info

	def show_all(self):
		'''
		Mostra todas as informações do sitema contidas no arquivo /etc/os-release.
		'''
		self.release_os_info = self.get_info()
		for key in self.release_os_info:
			print(key, '=>', self.release_os_info[key])

	def info(self, type_info: str) -> dict:
		self.release_os_info = self.get_info()

		if type_info == 'ALL':
			return self.release_os_info

		if type_info in self.release_os_info.keys():
			return str(self.release_os_info[type_info]) 
		else:
			return {}

#=====================================================#

class Unpack(PrintText):
	def __init__(self, destination=os.getcwd()):
		super().__init__()
		self.destination = destination

	def check_destination(self):
		if os.access(self.destination, os.W_OK) == True:
			return True
		else:
			self.red(f'[!] Falha você não tem permissão de escrita em ... {self.destination}')
			return False

	def clear_dir_unpack(self):
		if self.check_destination() != True:
			return False
		
		os.chdir(self.destination)
		files = os.listdir(self.destination)

		for f in files:
			rmdir(f)    

	def tar(self, file):
		# Verificar se o arquivo e do tipo tar
		if not tarfile.is_tarfile(file):
			self.red(f'O arquivo {file} NÃO é do tipo ".tar"')
			return False
			
		self.clear_dir_unpack()
		print(f'Descomprimindo ... {os.path.basename(file)}', end=' ')
		os.chdir(self.destination)
		try:
			tar = tarfile.open(file)
			tar.extractall()
			tar.close()
		except(KeyboardInterrupt):
			print('Cancelado com Ctrl c')
			sys.exit()
		except Exception as err:
			self.red('Erro')
			self.red(err)
			sys.exit(1)
		else:
			print('OK')

	def zip(self, file):
		# Verificar se o arquivo e do tipo zip
		if not is_zipfile(file):
			self.red(f'O arquivo {file} NÃO é do tipo (.zip)')
			return

		self.clear_dir_unpack()
		print(f'Descomprimindo ... {os.path.basename(file)}', end= ' ')
		os.chdir(self.destination)
		try:
			with ZipFile(file, 'r') as zip: 
				# printing all the contents of the zip file 
				# zip.printdir()  
				zip.extractall()
		except:
			self.red('Falha')
			sys.exit('1')
		else:
			print('OK')

	def deb(self, file):
		self.clear_dir_unpack()
		os.chdir(self.destination)

		print(f'Descomprimindo ... {os.path.basename(file)}', end=' ')
		#os.system(f'ar -x {file} --output={DirUnpack} 1> /dev/null 2>&1')
		if os.path.isfile('/etc/debian_version'):
			out = subprocess.getstatusoutput('ar -x {}'.format(file))
		else:
			out = subprocess.getstatusoutput('ar -x {} --output={}'.format(file, self.destination))

		if out[0] == int(0):
			print('OK')
		else:
			self.red('Falha')
			sys.exit(1)
		

#=====================================================#

def get_html_lines(url: str) -> list:
	'''
	Baixa o html de uma página e retorna o contéudo em forma de lista.
	'''
	RegExp = re.compile(r'^http:|^ftp:|^https|^www')
	if RegExp.findall(url) == []:
		print(f'Erro: url inválida.')
		return False

	print(f'Conectando ... {url}')
	try: 
		req = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent})
		html = urllib.request.urlopen(req)
	except:
		self.red('get_html_lines: Erro')
		return []
	else:
		return (html.read().decode('utf-8').split('\n'))

def get_html_page(url: str) -> list:
	'''
	Baixa o html de uma página e retorna o contéudo em forma de lista.
	'''
	RegExp = re.compile(r'^http:|^ftp:|^https|^www')
	if RegExp.findall(url) == []:
		print(f'Erro: url inválida.')
		return False

	print(f'Conectando ... {url}')
	try: 
		req = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent})
		html = urllib.request.urlopen(req)
	except:
		self.red('get_html_lines: Erro')
		return []
	else:
		return (html.read().decode('utf-8'))

def get_html_links(url: str) -> list:
	'''
	Retornar uma lista com todos os links encontrados em um url/html.
	Requer o módulo bs4.
	'''
	links = []
	html = get_html_page(url)
	if html == []:
		return []

	soup = BeautifulSoup(html, 'html.parser')
	for link in soup.findAll('a'):
		link = link.get('href')
		links.append(link)
	return links

class DowProgressBar():
	'''
	https://stackoverflow.com/questions/37748105/how-to-use-progressbar-module-with-urlretrieve
	'''
	def __init__(self):
		self.pbar = None

	def __call__(self, block_num, block_size, total_size):
		if not self.pbar:
			self.pbar = progressbar.ProgressBar(maxval=total_size)
			self.pbar.start()

		downloaded = block_num * block_size
		if downloaded < total_size:
			self.pbar.update(downloaded)
		else:
			self.pbar.finish()

def downloader(url: str, output_file: str) -> bool:
	'''
	Retorna True se o download for executado com suscesso, ou False caso o download falhe.
	'''
	# https://homepages.inf.ed.ac.uk/imurray2/code/hacks/urlsize
	# https://stackoverflow.com/questions/37748105/how-to-use-progressbar-module-with-urlretrieve
	# https://www.programmersought.com/article/80002135225/
	# curl -i HEAD url

	if os.path.isfile(output_file) == True:
		print(' + Arquivo encontrado ... {}'.format(output_file))
		return True

	RegExp = re.compile(r'^http|ftp|www')
	if (RegExp.findall(url) == []):
		print(f'downloader: Falha informe um url válido')
		return

	print_line()
	print(f'Conectando ... {url}')
	req = urllib.request.Request(
	    		url, 
	    		data=None, 
	    		headers={
					'User-Agent': user_agent 
					}	
				)
	try:
		response = urllib.request.urlopen(req)
	except:
		print(f'downloader: Falha')
		return False
	else:	
		file_online_info = response.info()
		type_file = file_online_info.get('content-type')
		num_bytes = int(file_online_info.get('content-length'))
		num_kbytes = float(num_bytes / 1024)
		num_megabytes = float(num_bytes / 1048576)	
		num_gbytes = float(num_bytes / 1073741824)

		if 1024 > num_bytes:
			num_total_length = num_bytes
			unid = 'B'
		elif 1024 > num_kbytes:
			num_total_length = num_kbytes
			unid = 'KB'
		elif 1024 > num_megabytes:
			num_total_length = num_megabytes
			unid = 'MB'
		else:
			num_total_length = num_gbytes
			unid = 'GB'

		if num_bytes and type_file:
			print('{:.2f}{} | {}'.format(num_total_length, unid, type_file))
		print(f'Salvando em ... {output_file}')
		urllib.request.urlretrieve(url, output_file, DowProgressBar())
		return True




