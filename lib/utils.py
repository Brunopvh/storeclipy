#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import getpass
import shutil
import tempfile
import tarfile
import hashlib
import urllib.request
import subprocess
import progressbar # Externo
import platform
from pathlib import Path
from zipfile import ZipFile, is_zipfile
from bs4 import BeautifulSoup # Externo

if float(platform.python_version()[0:3]) < float(3.7):
	print('Erro ... necessário python 3.7 ou superior')
	sys.exit(1)

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
		print(f'{text}', end='')

	def red(self, text=''):
		print(f'{CRed}[!] {CReset}{text}')

	def green(self, text=''):
		print(f'{CGreen}[+] {CReset}{text}')

	def yellow(self, text=''):
		print(f'{CYellow} + {CReset}{text}')

	def blue(self, text=''):
		print(f'{CBlue} > {CReset}{text}')

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
	RegexPath = re.compile("[A-Za-z0-9]+")
	if RegexPath.match(path) == None:
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
		PrintText().red('')
		raise
	else:		
		if not os.access(path, os.W_OK):
			print()
			print("mkdir: Você não tem permissão de escrita em ... {}".format(path))
			return False

		print('OK')
		return True 

def rmdir_old(path, silent=False):
	if os.path.exists(path) == False:
		print(f'Não encontrado ... {path}')
		return False

	print(f'Apagando ... {path}', end=' ')
	try:
		if os.path.isdir(path):
			shutil.rmtree(path)
		else:
			os.remove(path)
	except:
		print(f'{CRed}Erro{CReset}')
		return False
	else:
		print('OK')
		return True

def rmdir(path: str, silent=False):
	'''
	Recebe um arquivo ou diretório para ser deletado.
	Caso a operação falhe será disparada uma exceção.
	'''

	print(f'Apagando ... {path}', end=' ')
	try:
		# Tratar como diretório.
		shutil.rmtree(path)
	except(FileNotFoundError):
		PrintText().red('arquivo ou diretório não existe.')
	except(PermissionError):
		PrintText().red('sem permissão [W]')
	except(NotADirectoryError):
		# Tratar como arquivo.
		try:
			os.remove(path)
		except Exception as ERR:
			print(type(ERR))
			raise
	except Exception as err:
		print(type(err))
		raise
	else:
		print('OK')
		return True

def is_root(text='Autêntitação necessária para prosseguir [%u]: ')-> bool:
	StatusOutput = 0
	if os.geteuid() != 0:
		try:
			StatusOutput = subprocess.check_call(f"sudo -v -p '%s'" % text, shell=True)
		except:
			StatusOutput = int(1)

	if StatusOutput == int(0):
		return True
	else:
		return False

def sha256(file: str, sum: str) -> bool:
	'''
	Função que recebe um arquivo e uma hash em forma de string (respectivamente) e gera
	a hash do arquivo (sha256sum) para comparar com o valor passado no argumento. Se os
	valores forem iguais, a função irá retornar True, se não irá retornar False.
	'''
	len_file = float(os.path.getsize(file))
	len_file = len_file / (1024*1024)
	print('Gerando hash do arquivo ... {} [{:.2f}MB]'.format(os.path.basename(file), len_file))
	f = open(file, 'rb')
	h = hashlib.sha256()
	h.update(f.read())
	hash_file = h.hexdigest() 
	
	print('Comparando valores ...', end=' ')
	if (hash_file) == sum:
		print('OK')
		return True
	else:
		PrintText().red('Falha')
		return False

def is_executable(app_executable: str) -> bool:
	OutPut = subprocess.getstatusoutput(f'command -v {app_executable}')
	if OutPut[0] == int(0):
		return True
	else:
		return False

class ReadFile(PrintText):
	def __init__(self, file: str):
		self.file = file

	def read_file(self) -> list:
		'''
		Ler um arquivo e retornar as linhas em forma de lista.
		'''
		try:
			with open(self.file, 'rt') as f:
				lines = f.read().split('\n')
		except(FileNotFoundError):
			self.red('{} arquivo não encontrado ... {}'.format(__class__.__name__, self.file))
			return []
		except Exception as err:
			print(__class__.__name__, type(err))
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
		if not (isinstance(content, list)):
			self.red(f'{__class__.__name__} o conteúdo a ser escrito precisa ser do  tipo "list".')
			return False

		print('{} escrevendo no arquivo {}'.format(__class__.__name__, self.file), end= ' ')
		try:
			with open(self.file, 'w') as f:
				for L in content:
					if L != '':
						f.write(f'{L}\n')
		except(PermissionError):
			print()
			self.red('{} você não tem permissão de escrita no arquivo.'.format(__class__.__name__))
			return False
		except Exception as err:
			print()
			self.red(type(err))
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
			self.red(f'{__class__.__name__} o arquivo não existe.')
			return []

		try:
			content = self.read_file()
		except Exception as err:
			self.red(f'{__class__.__name__} {type(err)}')
			return []
		else:
			if content == []:
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

class SetRootConfig:
	def __init__(self, appname, create_dirs=True):
		self.kernel_type = KERNEL_TYPE
		self.appname = appname
		self.dir_home = Path.home()

		if (self.kernel_type == 'Linux') or (self.kernel_type == 'FreeBSD'):
			self.dir_bin_root = '/usr/local/bin'
			self.dir_icons_root = '/usr/share/icons/hicolor'
			self.dir_desktop_links_root = '/usr/share/applications'
			self.dir_themes_root = '/usr/share/themes'
			self.dir_cache_root = os.path.abspath(os.path.join('/var/cache', self.appname))
			self.dir_gnupg_root = os.path.abspath(os.path.join(self.dir_home, '.gnupg'))
			self.dir_config_root = os.path.abspath(os.path.join('/etc', self.appname))
			self.file_config_root = os.path.abspath(os.path.join(self.dir_config_root, f'{self.appname}.conf'))
		elif self.kernel_type == 'Windows':
			self.dir_bin_root = ''
			self.dir_icons_root = ''
			self.dir_desktop_links_root = ''
			self.dir_themes_root = ''
			self.dir_cache_root = ''
			self.dir_gnupg_root = ''
			self.dir_config_root = ''
			self.file_config_root = ''
				
		# self.dir_temp = tempfile.TemporaryDirectory().name
		self.file_temp = tempfile.NamedTemporaryFile(delete=True).name
		if (self.kernel_type == 'Linux') or (self.kernel_type == 'FreeBSD'):
			self.dir_temp_root = os.path.abspath(os.path.join('/tmp', f'{self.appname}-{getpass.getuser()}'))
		elif self.kernel_type == 'Windows':
			self.dir_temp_root = os.path.abspath(os.path.join('C:', f'{self.appname}-{getpass.getuser()}'))

		self.dir_unpack_root = os.path.abspath(os.path.join(self.dir_temp_root, 'unpack'))
		self.dir_gitclone_root = os.path.abspath(os.path.join(self.dir_temp_root, 'gitclone'))

		self.root_info = {
			'home': self.dir_home,
			'bin': self.dir_bin_root,
			'cache': self.dir_cache_root,
			'config': self.dir_config_root,
			'icons': self.dir_icons_root,
			'gnupg': self.dir_gnupg_root,
			'dir_temp': self.dir_temp_root,
			'unpack': self.dir_unpack_root,
			'gitclone': self.dir_gitclone_root,
			'desktop_links': self.dir_desktop_links_root,
			}

		if create_dirs == True:
			for key in self.root_info:
				d = self.root_info[key]
				if os.path.isdir(d) == False:
					if os.name == 'nt':
						mkdir(d)
					else:
						os.system(f'sudo mkdir -p {d}')
		
	def get_root_info(self):
		return self.root_info

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
			self.dir_icons = os.path.abspath(os.path.join(self.dir_home, '.local', 'share', 'icons'))
			self.dir_desktop_links = os.path.abspath(os.path.join(self.dir_home, '.local', 'share', 'applications'))
			self.dir_cache = os.path.abspath(os.path.join(self.dir_home, '.cache', self.appname))
			self.dir_gnupg = os.path.abspath(os.path.join(self.dir_home, '.gnupg'))
			self.dir_config = os.path.abspath(os.path.join(self.dir_home, '.config', self.appname))
			self.file_config = os.path.abspath(os.path.join(self.dir_config, f'{self.appname}.conf'))
			self.file_bashrc = os.path.abspath(os.path.join(self.dir_home, '.bashrc'))
			Path(self.file_bashrc).touch()
		elif self.kernel_type == 'Windows':
			self.dir_bin = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'Local', 'Programs', self.appname))
			self.dir_icons = ''
			self.dir_desktop_links = ''
			self.dir_gnupg = os.path.abspath(os.path.join(self.dir_home, '.gnupg'))
			self.dir_cache = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'LocalLow', self.appname))
			self.dir_config = os.path.abspath(os.path.join(self.dir_home, 'AppData', 'Roaming', self.appname))
			self.file_config = os.path.abspath(os.path.join(self.dir_config, f'{self.appname}.conf'))	
				
		# self.dir_temp = tempfile.TemporaryDirectory().name
		self.file_temp = tempfile.NamedTemporaryFile(delete=True).name
		if (self.kernel_type == 'Linux') or (self.kernel_type == 'FreeBSD'):
			self.dir_temp = os.path.abspath(os.path.join('/tmp', f'{self.appname}-{getpass.getuser()}'))
		elif self.kernel_type == 'Windows':
			self.dir_temp = os.path.abspath(os.path.join('C:\\', f'{self.appname}-{getpass.getuser()}'))

		self.dir_unpack = os.path.abspath(os.path.join(self.dir_temp, 'unpack'))
		self.dir_gitclone = os.path.abspath(os.path.join(self.dir_temp, 'gitclone'))

		self.user_info = {
			'home': self.dir_home,
			'cache': self.dir_cache,
			'config': self.dir_config,
			'bin': self.dir_bin,
			'icons': self.dir_icons,
			'gnupg': self.dir_gnupg,
			'dir_temp': self.dir_temp,
			'unpack': self.dir_unpack,
			'gitclone': self.dir_gitclone,
			'desktop_links': self.dir_desktop_links,
			}

		if create_dirs == True:
			for key in self.user_info:
				d = self.user_info[key]
				if (os.path.isdir(d) == False):
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
			return True

		file_bashrc_backup = os.path.join('{}-{}-{}'.format(self.file_bashrc, 'pre', {self.appname}))
		if os.path.isfile(file_bashrc_backup) == False:
			shutil.copyfile(self.file_bashrc, file_bashrc_backup)

		obj_bashrc = ReadFile(self.file_bashrc)
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

class ReleaseInfo(object):
	def __init__(self):
		if os.path.isfile('/etc/os-release') == True:
			release_file = '/etc/os-release'
		elif os.path.isfile('/usr/lib/os-release') == True:
			release_file = '/usr/lib/os-release'
		elif os.path.isfile('/usr/local/etc/os-release') == True:
		    release_file = '/usr/local/etc/os-release'
		else:
			release_file = None

		if (release_file != None) and (os.path.isfile(release_file) == True):
			self.obj_reslease_file = ReadFile(release_file) 
		self.release_os_info = {}

	def get_info(self):
		'''
		Obter as informações do sistema contidas no arquivo /etc/os-release.
		'''
		if KERNEL_TYPE == 'Windows':
			self.release_os_info.update({'BASE_DISTRO': 'windows'})
		else:
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

			if os.path.isfile('/etc/debian_version') == True:
				self.release_os_info.update({'BASE_DISTRO': 'debian'})

		return self.release_os_info

	def show_all(self):
		'''
		Mostra todas as informações do sitema contidas no arquivo /etc/os-release.
		'''
		self.release_os_info = self.get_info()
		for key in self.release_os_info:
			print(key, '=>', self.release_os_info[key])

	def get(self, type_info: str) -> dict:
		'''
		Recebe uma strig com a informação que se deseja obter do sistema e retorna a infomação
		em forma de string. 
		   EX get('ID') -> debian, fedora, ubuntu, linuxmint...
		   get('VERSION_CODENAME') -> buster, focal, tricia...
		   use o metodo show_all para ver todas as informações disponiveis.
		'''
		self.release_os_info = self.get_info()
		if type_info == 'ALL':
			return self.release_os_info

		if type_info in self.release_os_info.keys():
			return str(self.release_os_info[type_info]) 
		else:
			return {}

class Unpack(PrintText):
	def __init__(self, destination=os.getcwd(), clear_dir=False):
		super().__init__()
		self.clear_dir = clear_dir
		self.destination = destination
		if os.path.isdir(self.destination) == False:
			self.red('Unpack: O deretório não existe ... {}'.format(self.destination))
			sys.exit(1)

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
			
		if self.clear_dir == True:
			self.clear_dir_unpack()

		len_file = float(os.path.getsize(file) / (1024*1024))
		os.chdir(self.destination)
		print('Descomprimindo ... {} [{:.2f}MB]'.format(os.path.basename(file), len_file), end=' ')
		try:
			tar = tarfile.open(file)
			tar.extractall()
			tar.close()
		except(KeyboardInterrupt):
			print('Cancelado com Ctrl c')
			sys.exit()
		except Exception as err:
			self.sred('Erro')
			print(err)
			sys.exit(1)
		else:
			print('OK')

	def zip(self, file):
		# Verificar se o arquivo e do tipo zip
		if not is_zipfile(file):
			self.red(f'O arquivo {file} não é do tipo (.zip)')
			return False

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
			return True

	def deb(self, file):
		self.clear_dir_unpack()
		os.chdir(self.destination)

		print(f'Descomprimindo ... {os.path.basename(file)}', end=' ')
		# os.system(f'ar -x {file} --output={DirUnpack} 1> /dev/null 2>&1')
		if os.path.isfile('/etc/debian_version'):
			out = subprocess.getstatusoutput('ar -x {}'.format(file))
		else:
			out = subprocess.getstatusoutput('ar -x {} --output={}'.format(file, self.destination))

		if out[0] == int(0):
			print('OK')
		else:
			self.red('Falha')
			sys.exit(1)

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


def gpg_import(key_file: str, url_key=None) -> bool:
    '''
    Função para importar chaves gpg. você pode informar apenas o arquivo .asc com os dados
    ou caso preferir pode informar o URL que contém um arquivo com os dados a serem importados
    é um caminho completo onde o arquivo será baixado.

    EX:
       gpg_import(key_file) => irá assumir que o arquivo já existe no local indicado.
       gpg_import(key_file, url) => irá baixar o "URL" no "destino key_file".
    '''

    if url_key != None:
        print(f'Baixando ... {url_key}', end=' ')
        try:
            urllib.request.urlretrieve(url_key, key_file)
        except :
            print(f'{CRed}Erro{CReset}')
            return False
        else:
            print('OK')
            return True

    print(f'Importando ... {key_file}', end=' ') 
    out = subprocess.getstatusoutput(f'gpg --import {key_file}')
    if out[0] == 0:
        print(f'{CGreen}OK{CReset}')
        return True
    else:
        print()
        print('\033[0;31mErro\033[m')
        print(out[1])
        return False

def gpg_verify(path_to_signature_file, path_file):
    print(f'Verificando arquivo ... {path_file}', end=' ')
    out = subprocess.getstatusoutput(f'gpg --verify {path_to_signature_file} {path_file}')
    if out[0] == 0:
        print('\033[0;32mOK\033[m')
        return True
    else:
        print()
        print('\033[0;31mFalha\033[m')
        print(out[1])
        return False

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

class DownloadFiles(SetUserConfig, PrintText):
	def __init__(self):
		super().__init__(appname, create_dirs=True)
		# Caminho do executável curl.exe no Windows.
		self.curl_binary_win = os.path.abspath(os.path.join(self.dir_bin, 'curl-win64', 'bin', 'curl.exe'))

	def gitclone(self, repo: str, output_dir: str) -> bool:
		'''Clonar repositórios.'''
		print(f'Entrando no diretório ... {output_dir}')
		os.chdir(output_dir)
		dirs = os.listdir(output_dir)
		dir_repo = os.path.basename(repo).replace('.git', '')
		for d in dirs:
			if os.path.exists(d) == dir_repo:
				yes_no = input(f'Deseja apagar {d} [{CYellow}s{CReset}/{CRed}n{CReset}]?: ').strip().lower()
				if (yes_no == 's') or (yes_no == 'y'):
					rmdir(d)
				else:
					return True

		os.system(f'git clone {repo}')

	def downloader(self, url: str, output_file: str) -> bool:
		'''
		Retorna True se o download for executado com suscesso, ou False caso o download falhe.
		'''
		if os.path.isfile(output_file) == True:
			print('Arquivo encontrado ... {}'.format(output_file))
			return True

		os.chdir(self.dir_temp)
		RegExp = re.compile(r'^http|ftp|www')
		if (RegExp.findall(url) == []):
			print(f'downloader: Falha informe um url válido')
			return False

		print(f'Baixando ... {output_file}')
		print(f'Conectando ... {url}')
		req = urllib.request.Request(url, data=None, headers={'User-Agent': user_agent})
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

			urllib.request.urlretrieve(url, output_file, DowProgressBar())
			return True

	def wget_download(self, url: str, output_file: str) -> bool:
		import wget
		os.chdir(self.dir_temp)
		
		if os.path.isfile(output_file) == True:
			print(f'Arquivo encontrado ... {output_file}')
			return True

		print(f'Baixando ... {output_file}')
		print(f'Conectando ... {url}')
		try:
			wget.download(url, output_file)
		except:
			print()
			self.red('Erro')
			return False
		else:
			print(' OK')
			return True
		
	def curl_download(self, url, output_file: str) -> bool:
		os.chdir(self.dir_temp)
		if os.path.isfile(output_file) == True:
			print(' + Arquivo encontrado ... {}'.format(output_file))
			return True
		
		print(f'Baixando ... {output_file}')
		print('Conectando .... {}'.format(url))
		if os.name == 'nt':
			os.system(f'{self.curl_binary_win} -S -L -o {output_file} {url}')
		elif os.name == 'posix':
			os.system('curl -S -L -o {} {}'.format(output_file, url))
			# os.system(f'wine {self.curl_binary_win} -S -L -o {output_file} {url}') # Execução via wine.
		


