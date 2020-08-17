#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
'''
REFERÊNCIAS
  https://www.it-swarm.dev/pt/python/como-posso-obter-links-href-de-html-usando-python/969762638/
  https://www.crummy.com/software/BeautifulSoup/bs4/doc/
  https://pythonhelp.wordpress.com/tag/hashlib/

'''


import os, sys
import subprocess
import tempfile
import tarfile
import shutil
import platform
import urllib.request
import hashlib
from pathlib import Path
from getpass import getuser
from zipfile import ZipFile, is_zipfile
from time import sleep

from lib.print_text import PrintText
from lib.apt_get import AptGet 
from lib.pacman import Pacman
from lib.pkg import Pkg
from lib.unpack_files import UnpackFiles
from lib.os_release import ReleaseInfo
from lib.downloader import *

try:
    from bs4 import BeautifulSoup
except Exception as erro:
    print(erro, ' => execute: pip3 install bs4 --user')
    sys.exit()

app_name = 'storeclipy'

# Diretórios de trabalho
DirHome = Path.home()
DirBin = os.path.abspath(os.path.join(DirHome, '.local', 'bin'))
DirDesktopFiles = os.path.abspath(os.path.join(DirHome, '.local', 'share', 'applications'))
DirCache = os.path.abspath(os.path.join(DirHome, '.cache', 'storecli-ultimate'))
DirConfig = os.path.abspath(os.path.join(DirHome, '.config', app_name))
DirDownloads = os.path.abspath(os.path.join(DirHome, '.cache', app_name, 'downloads'))
#DirTemp = tempfile.mkdtemp()
DirTemp = f'/tmp/{getuser()}_tmp'
DirUnpack = os.path.abspath(os.path.join(DirTemp, 'unpack'))

list_dirs = [
	DirHome,
    DirBin,
	DirCache,
    DirConfig,
	DirDownloads,
	DirTemp,
	DirUnpack,
    DirDesktopFiles
]

def mkdir(path):
        try:
            if not os.path.exists(path):
                os.makedirs(path, 0o700)
                return True
        except Exception as erro:
            print("[!] Não foi possível criar o diretório: {0}".format(path))
            print(erro)
            return False
        if not os.access(path, os.W_OK):
            print("[!] Você não tem permissão de escrita em: {0}".format(path))
            return False
        return True

for DIR in list_dirs:
	mkdir(DIR)

unpack = UnpackFiles(DirUnpack)

def is_executable(exec):
	if int(subprocess.getstatusoutput(f'command -v {exec}')[0]) == int('0'):
		return True
	else:
		return False

def get_html(url):
    try: 
        print(f'Conectando ... {url}')
        html = urllib.request.urlopen(url).read()
    except Exception as erro:
        print(f'Falha: {erro}')
        sys.exit()
    else:
        return html

def get_links(url):
    links = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    for LINK in soup.findAll('a'):
        link = LINK.get('href')
        links.append(link)
    return links

def sha256(file, sum):
    print(f'Caulculando hash do arquivo ... {file}')
    f1 = open(file, 'rb')
    h = hashlib.sha256()
    h.update(file.read())
    hash_file = h.hexdigest() 
    print(hash_file)

    if (hash_file) == sum:
        return True
    else:
        return False
    
class Veracrypt(PrintText):
    def __init__(self):
        if is_executable('veracrypt'):
            self.yellow('veracrypt já está instalado')
        self.msg('Instalando veracrypt')
        self.URL = 'https://www.veracrypt.fr/en/Downloads.html'
        self.veracrypt_sha256sum_txt = 'veracrypt-sha256.txt'
        self.veracrypt_sha256sum_sig = 'veracrypt-sha256.txt.sig'
        self.veracrypt_urls = get_links(self.URL)

    def get_shasum_file(self):
        '''
        Função para baixar o arquivo de texto contendo as hashs e o arquivo ".sig".
        '''
        urls = self.set_systems_urls()
        url_sha256sum_txt = urls['sha256_txt']
        url_sha256sum_sig = urls['sha256_txt_sig']
        
        path_file_sha256sum_txt = '{}/{}'.format(DirTemp, self.veracrypt_sha256sum_txt)
        path_file_sha256sum_sig = '{}/{}'.format(DirTemp, self.veracrypt_sha256sum_sig)
        wget_download(url_sha256sum_txt, path_file_sha256sum_txt)
        wget_download(url_sha256sum_sig, path_file_sha256sum_sig)

    def set_systems_urls(self):
        systems_urls = {'info': 'URL de downloads para diversos sistemas operacionais'}

        for L in self.veracrypt_urls:
            if ('sha256sum.txt' in L) and (not '.sig' in L):
                systems_urls['sha256_txt'] = L
            elif ('sha256sum.txt' in L) and ('.sig' in L):
                systems_urls['sha256_txt_sig'] = L
            elif ('.tar.bz2' in L) and (not 'freebsd' in L) and ('veracrypt' in L):
                systems_urls['linux'] = L
                systems_urls['linux_sig'] = f'{L}.sig'
                

        return systems_urls


    def linux(self):
        # Obter o link de download do pacote ".tar".
        urls = self.set_systems_urls()
        url_veracrypt_linux = urls['linux']

        # Definir o camiho completo do arquivo a ser baixado
        path_file_veracrypt = '{}/{}'.format(DirDownloads, os.path.basename(url_veracrypt_linux))
        
        wget_download(url_veracrypt_linux, path_file_veracrypt)
        self.get_shasum_file()

    def veracrypt_freebsd():
    	'''
    	Requerimentos: FUSE library and tools, device mapper tools
    	
    	'''
    	URL_VERACRYPT_BSD = 'https://launchpadlibrarian.net/492507323/veracrypt-1.24-Update7-freebsd-setup.tar.bz2'
    	path_file = f'{DirDownloads}/veracrypt-1.24-Update7-freebsd-setup.tar.bz2'
    	
    	PrintText().msg('Instalando veracrypt')
    		
    	wget_download(URL_VERACRYPT_BSD, path_file)
    	unpack.tar(path_file)
    	os.chdir(DirUnpack)
    	os.system('chmod +x veracrypt-1.24-Update7-freebsd1164-setup-gui-x64')
    	os.system('./veracrypt-1.24-Update7-freebsd1164-setup-gui-x64')

    def install(self):
        if platform.system() == 'FreeBSD':
            self.freebsd()
        elif platform.system() == 'Linux':
            self.linux()

#-----------------------------------------------------------#
# Internet
#-----------------------------------------------------------#

class YoutubeDlg(PrintText):
    def __init__(self):
        self.URL = 'https://github.com/MrS0m30n3/youtube-dl-gui/archive/master.zip'
        
        if (platform.system() == 'Linux') or (platform.system() == 'FreeBSD'):
            self.path_file_zip = f'{DirDownloads}/youtube-dlg.zip'
            self.destination_ytdlg = f'{DirBin}/youtube_dl_gui'
            self.exec_ytdl = f'{DirBin}/youtube-dl-gui' 
            
    def get_ytdlg(self):
        wget_download(self.URL, self.path_file_zip)
        unpack.zip(self.path_file_zip)
        
    def twodict(self):
        if is_executable('git') == 'False':
            self.red('Instale o git para prosseguir')
            sys.exit('1')
        
        self.yellow('Instalando python twodict')
        os.chdir(DirTemp)
        if os.path.isdir('twodict') == False:
            os.system(f'git clone https://github.com/MrS0m30n3/twodict.git')
            
        os.chdir('twodict')
        
        if is_executable('python2.7') == 'True':
            os.system('sudo python2.7 setup.py install')
        elif is_executable('python2') == 'True':
            os.system('sudo python2 setup.py install')
        elif is_executable('python') == 'True':
            os.system('sudo python setup.py install')
        else:
            self.red('Instale o python2 para prosseguir')
            sys.exit('1')
            
    def compile_ytdlg(self):
        wget_download(self.URL, self.path_file_zip)
        unpack.zip(self.path_file_zip)
        
        self.yellow('Compilando youtube-dl-gui')
        os.chdir(f'{DirUnpack}/youtube-dl-gui-master')
        
        if is_executable('python2.7') == 'True':
            os.system('sudo python2.7 setup.py install')
        elif is_executable('python2') == 'True':
            os.system('sudo python2 setup.py install')
        elif is_executable('python') == 'True':
            os.system('sudo python setup.py install')
        else:
            self.red('Instale o python2 para prosseguir')
            sys.exit('1')
    
    def file_desktop_root(self):
        os.chdir(DirTemp)
        if platform.system() == 'Linux':
            f = '/usr/share/applications/youtube-dl-gui.desktop'
        elif platform.system() == 'FreeBSD':
            f = '/usr/local/share/applications/youtube-dl-gui.desktop'
            
        self.yellow(f'Criando o arquivo ... {f}')
        lines_file_desktop = (
            "[Desktop Entry]",
            "Encoding=UTF-8",
            "Name=Youtube-Dl-Gui",
            "Exec=youtube-dl-gui",
            "Version=1.0",
            "Terminal=false",
            "Icon=youtube-dl-gui",
            "Type=Application",
            "Categories=Internet;Network;",
        )
        
        file = open('youtube-dl-gui.desktop', 'w')
        for line in lines_file_desktop:
            file.write(f'{line}\n')
            
        file.seek(0)
        file.close()
        os.system(f'sudo cp youtube-dl-gui.desktop {f}')
        os.system(f'cp {f} {DirDesktopFiles}/yotube-dl-gui.desktop')
        if is_executable('gtk-update-icon-cache'):
            os.system('gtk-update-icon-cache')
    
    def freebsd(self):    
        self.twodict() # Instalar o python twodict.
        Pkg().install(['py27-wxPython30']) # Instalar dependências
        self.compile_ytdlg() # compilar.
        self.file_desktop_root()
    
    def archlinux(self):
        Pacman().install('python2 python2-pip python2-setuptools python2-wxpython3')
        self.twodict()
        self.compile_ytdlg()
        self.file_desktop_root()

    def install(self):
        if is_executable('youtube-dl-gui'):
            self.yellow('Youtube-dl-gui já está instalado')

        self.msg('Instalando youtube-dl-gui')
        if platform.system() == 'FreeBSD':
            self.freebsd()
        elif platform.system() == 'Linux':
            if ReleaseInfo().info('ID') == 'arch':
                self.archlinux()
        

	
	
