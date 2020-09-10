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
from zipfile import ZipFile, is_zipfile

from lib.print_text import PrintText
from lib.downloader import *

if platform.system() != 'Windows':
    from lib.apt_get import AptGet
    from lib.dpkg import Dpkg 
    from lib.pacman import Pacman
    from lib.pkg import Pkg
    from lib.os_release import ReleaseInfo

# Importar bs4 apartir do diretório local.
try:
    from bs4 import BeautifulSoup
except Exception as erro:
    print(erro, ' => execute: pip3 install bs4 --user')
    sys.exit()



columns = os.get_terminal_size()[0]
space_line = ('-' * columns)

# Default
CRed = '\033[0;31m'
CGreen = '\033[0;32m'
CYellow = '\033[0;33m'
CBlue = '\033[0;34m'
CWhite = '\033[0;37m'

# Strong
CSRed = '\033[1;31m'
CSGreen = '\033[1;32m'
CSYellow = '\033[1;33m'
CSBlue = '\033[1;34m'
CSWhite = '\033[1;37m'

# Dark
CDRed = '\033[2;31m'
CDGreen = '\033[2;32m'
CDYellow = '\033[2;33m'
CDBlue = '\033[2;34m'
CDWhite = '\033[2;37m'

# Blinking text
CBRed = '\033[5;31m'
CBGreen = '\033[5;32m'
CBYellow = '\033[5;33m'
CBBlue = '\033[5;34m'
CBWhite = '\033[5;37m'

# Reset
CReset = '\033[0m'

class PrintText:
    '''
    Use: class(PrintText)
         self.red("text") - self.yellow("text") ...
    '''
    def __init__(self):
        pass

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
        
    def msg(self, text=''):
        self.line()
        print(text.center(columns))
        self.line()
    
    def line(self, char=None):
        if char == None:
            print('=' * columns)
        else:
            print(char * columns)


app_name = 'storecli'

#==================================================#
# Diretórios de trabalho
#==================================================#
if platform.system() == 'FreeBSD':
    DirHome = os.path.abspath(os.path.join('/usr', Path.home()))
else:
    DirHome = Path.home()

if (platform.system() == 'Linux') or (platform.system() == 'FreeBSD'):
    DirBin = os.path.abspath(os.path.join(DirHome, '.local', 'bin'))
    DirDesktopFiles = os.path.abspath(os.path.join(DirHome, '.local', 'share', 'applications'))
    DirCache = os.path.abspath(os.path.join(DirHome, '.cache', app_name))
    DirConfig = os.path.abspath(os.path.join(DirHome, '.config', app_name))
    DirDownloads = os.path.abspath(os.path.join(DirHome, '.cache', app_name, 'downloads'))
    DirIcons = os.path.abspath(os.path.join(DirHome, '.local', 'share', 'icons'))
    #DirTemp = tempfile.mkdtemp()
    DirTemp = os.path.abspath(os.path.join('/tmp', app_name, getuser()))
    DirUnpack = os.path.abspath(os.path.join(DirTemp, 'unpack'))
    DirGitclone = os.path.abspath(os.path.join(DirTemp, 'gitclone'))

    list_dirs = [
        DirHome,
        DirBin,
        DirCache,
        DirConfig,
        DirDownloads,
        DirTemp,
        DirUnpack,
        DirGitclone,
        DirDesktopFiles,
    ]

elif platform.system() == 'Windows':
    DirBin = os.path.abspath(os.path.join(DirHome, 'AppData', 'Local', 'Programs'))
    DirCache = os.path.abspath(os.path.join(DirHome, 'AppData', 'Local', app_name))
    DirConfig = os.path.abspath(os.path.join(DirHome, 'AppData', 'Local', app_name))
    DirDownloads = os.path.abspath(os.path.join(DirHome, 'AppData', 'Local', app_name, 'downloads'))
    #DirTemp = tempfile.mkdtemp()
    DirTemp = os.path.abspath(os.path.join(DirHome, 'AppData', 'Local', app_name, 'temp'))
    DirUnpack = os.path.abspath(os.path.join(DirTemp, 'unpack'))
    DirGitclone = os.path.abspath(os.path.join(DirTemp, 'gitclone'))

    list_dirs = [
        DirHome,
        DirBin,
        DirCache,
        DirConfig,
        DirDownloads,
        DirTemp,
        DirUnpack,
        DirGitclone,
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

def rmdir(path):
        if not os.access(path, os.W_OK):
            print(f'Autênticação nescessária para apagar ... {path}')
            os.system(f'sudo rm -rf {path}')
        else:
            print(f'Apagando ... {path}')
            #shutil.rmtree(path)
            os.system(f'rm -rf {path}')

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
    try: 
        print(f'Conectando ... {url}')
        html = urllib.request.urlopen(url).read()
    except Exception as erro:
        print(f'Falha: {erro}')
        sys.exit()
    else:
        soup = BeautifulSoup(html, 'html.parser')
        for LINK in soup.findAll('a'):
            link = LINK.get('href')
            links.append(link)
        return links

def sha256(file, sum):
    print(f'Gerando hash do arquivo ... {file}')
    f = open(file, 'rb')
    h = hashlib.sha256()
    h.update(f.read())
    hash_file = h.hexdigest() 
    
    print('Comparando valores ...', end=' ')
    if (hash_file) == sum:
        print('OK')
        return True
    else:
        print('FALHA')
        return False

def check_gpg(sig_file, file):
    if (platform.system() == 'Linux') or (platform.system() == 'FreeBSD'):
        print(f'gpg: verificando arquivo ... {file}', end=' ')
        out = subprocess.getstatusoutput(f'gpg --verify {sig_file} {file}')
        if out[0] == 0:
            print('OK')
            return True
        else:
            print('')
            PrintText().red(out[1])
            return False
    else:
        return False


#-----------------------------------------------------------#
# Descompressão de arquivos.
#-----------------------------------------------------------#
def unpack_tar(tar_file, output_dir=DirUnpack):
        try: 
            os.chdir(output_dir)
        except:
            pass
        else:
            try:
                shutil.rmtree(output_dir)
            except:
                print(f'Autênticação nescessária para remover ... {output_dir}')
                os.system(f'sudo rm -rf {output_dir}')

        if os.path.isdir(output_dir) == False:
            mkdir(output_dir)

        print(f'Descomprimindo: {tar_file}', end= ' ')
        os.chdir(output_dir)
        try:
            tar = tarfile.open(tar_file)
            tar.extractall()
            tar.close()
        except(KeyboardInterrupt):
            print('Cancelado com Ctrl c')
            sys.exit()
        except Exception as err:
            print()
            print(f'Falha na descompressão do  arquivo ... {tar_file}\n', err)
            sys.exit('1')
        else:
            print('OK')

def unpack_zip(zip_file, output_dir=DirUnpack):
        try: 
            os.chdir(output_dir)
        except:
            pass
        else:
            try:
                shutil.rmtree(output_dir)
            except:
                print(f'Autênticação nescessária para remover ... {output_dir}')
                os.system(f'sudo rm -rf {output_dir}')

        if os.path.isdir(output_dir) == False:
            mkdir(output_dir)

        # Verificar se o arquivo e do tipo zip
        if not is_zipfile(file):
            print(f'O arquivo NÃO é do tipo (.zip) ... {zip_file}')
            return

        print(f'Descomprimindo: {zip_file}', end= ' ')
        os.chdir(zip_file)

        try:
            with ZipFile(zip_file, 'r') as zip: 
                # printing all the contents of the zip file 
                # zip.printdir()  
                zip.extractall()
        except:
            print()
            print(f'Falha na descompressão de ... {zip_file}')
            sys.exit('1')
        else:
            print('OK')
    


class UnpackFiles(PrintText):
    def __init__(self, destination=DirUnpack):
        self.destination = destination

    def check_destination(self):
        if os.path.isdir(self.destination) == False:
            mkdir(self.destination)

        if os.access(self.destination, os.W_OK) == True:
            return True
        else:
            print(f'[!] Falha você não tem permissão de escrita em: {self.destination}')
            return False

    def clear_dir_unpack(self):
        if self.check_destination() != True:
            return
        
        os.chdir(self.destination)
        files = os.listdir(self.destination)

        for f in files:
            rmdir(f)    

    def tar(self, file):
        # Verificar se o arquivo e do tipo tar
        if not tarfile.is_tarfile(file):
            self.red(f'O arquivo {file} NÃO é do tipo ".tar"')
            return
            
        self.clear_dir_unpack()
        print(f'Descomprimindo: {file}', end= ' ')
        os.chdir(self.destination)
        try:
            tar = tarfile.open(file)
            tar.extractall()
            tar.close()
            print('OK')
        except(KeyboardInterrupt):
            print('Cancelado com Ctrl c')
            sys.exit()
        except Exception as err:
            print()
            self.red(f'Falha na descompressão de: {file}\n', err)
            sys.exit(1)

    def zip(self, file):
        # Verificar se o arquivo e do tipo zip
        if not is_zipfile(file):
            self.red(f'O arquivo {file} NÃO é do tipo (.zip)')
            return

        self.clear_dir_unpack()
        print(f'Descomprimindo: {file}', end= ' ')
        os.chdir(self.destination)

        try:
            with ZipFile(file, 'r') as zip: 
                # printing all the contents of the zip file 
                # zip.printdir()  
                zip.extractall()
            print('OK')
        except:
            print()
            self.red(f'Falha na descompressão do arquivo ... {file}')
            sys.exit('1')

    def deb(self, file):
        self.clear_dir_unpack()
        os.chdir(DirUnpack)

        print(f'Descomprimindo ... {file}', end=' ')
        try:
            os.system(f'ar -x {file} --output={DirUnpack} 1> /dev/null 2>&1')
        except Exception as err:
            print(' ')
            self.red(err)
            sys.exit(1)
        else:
            print('OK')


# Clonar repositórios:
def gitclone(repo):
    os.chdir(DirGitclone)
    dirs = os.listdir(DirGitclone)
    for d in dirs:
        if os.path.exists(d) == True:
            yes_no = input(f'Deseja apagar {d} [{CYellow}s{CReset}/{CRed}n{CReset}]?: ').strip().lower()
            if (yes_no == 's') or (yes_no == 'y'):
                rmdir(d)
            else:
                return

    os.system(f'git clone {repo}')


#-----------------------------------------------------------#
# Acessórios
#-----------------------------------------------------------#
class Etcher(PrintText):
    def __init__(self):
        pass

    def etcher_archlinux(self):
        # https://github.com/balena-io/etcher/releases
        url_etcher_appimage = 'https://github.com/balena-io/etcher/releases/download/v1.5.99/balenaEtcher-1.5.99-x64.AppImage'
        url_etcher_deb = 'https://github.com/balena-io/etcher/releases/download/v1.5.107/balena-etcher-electron_1.5.107_amd64.deb'

        name_etcher = os.path.basename(url_etcher_deb)
        path_etcher = os.path.abspath(os.path.join(DirDownloads, name_etcher))

        run_download(url_etcher_deb, path_etcher)
        UnpackFiles().deb(path_etcher)
        os.chdir(DirUnpack)
        self.yellow(f'Descomprimindo ... {DirUnpack}/data.tar.bz2')
        os.system('sudo tar -jxvf data.tar.bz2 -C / 1> /dev/null')
        print('Criando link ... /usr/local/bin/balena-etcher-electron')
        os.system('sudo chmod a+x /opt/balenaEtcher')
        os.system('sudo ln -sf /opt/balenaEtcher/balena-etcher-electron /usr/local/bin/balena-etcher-electron')

        if is_executable('balena-etcher-electron') == True:
            self.yellow('balenaEtcher instalado com sucesso.')
        else:
            self.red('Falha na instalação de balenaEtcher.')

    def etcher_debian(self):
        # https://github.com/balena-io/etcher
        url_etcher_deb = 'https://github.com/balena-io/etcher/releases/download/v1.5.107/balena-etcher-electron_1.5.107_amd64.deb'
        repo_etcher_debian = 'deb https://deb.etcher.io stable etcher'

        name_etcher = os.path.basename(url_etcher_deb)
        path_etcher = os.path.abspath(os.path.join(DirDownloads, name_etcher))

        run_download(url_etcher_deb, path_etcher)

        self.yellow('Adicionando key e repositório')
        os.system('sudo apt-key adv --keyserver hkps://keyserver.ubuntu.com:443 --recv-keys 379CE192D401AB61')
        os.system(f'echo "{repo_etcher_debian}" | sudo tee /etc/apt/sources.list.d/balena-etcher.list')
        AptGet().update()
        self.yellow(f'Instalando ... {path_etcher}')
        Dpkg().install(path_etcher)
        AptGet().broke()

        if is_executable('balena-etcher-electron') == True:
            self.yellow('balenaEtcher instalado com sucesso.')
        else:
            self.red('Falha na instalação de balenaEtcher.')


    def install(self):
        if platform.system() == 'Linux':
            if ReleaseInfo().info('ID') == 'arch':
                self.etcher_archlinux()
            elif ReleaseInfo().info('ID') == 'debian':
                self.etcher_debian()

class Veracrypt(PrintText):
    def __init__(self):
        self.URL = 'https://www.veracrypt.fr/en/Downloads.html'
        self.veracrypt_sha256sum_txt = f'{DirTemp}/veracrypt-sha256.txt'
        self.veracrypt_sha256sum_sig = f'{DirTemp}veracrypt-sha256.txt.sig'

    def veracrypt_urls(self):
        '''
        Retornar todos os links encontrados na página de download do veracrypt.
        '''
        return get_links(self.URL)

    def linux_tar(self):
        # Obter o link de download do pacote ".tar".
        urls = self.veracrypt_urls()
        for URL in urls:
            if (URL[-4:] == '.bz2') and (not 'freebsd' in URL) and ('setup' in URL) and (not 'legacy' in URL):
                url_veracrypt_linux = URL
                url_veracrypt_linux_sig = f'{URL}.sig'
                break
        
        # Definir o camiho completo do arquivo a ser baixado
        path_veracrypt_tarfile = '{}/{}'.format(DirDownloads, os.path.basename(url_veracrypt_linux))
        path_veracrypt_tarfile_sig = f'{path_veracrypt_tarfile}.sig'
        
        run_download(url_veracrypt_linux, path_veracrypt_tarfile)
        run_download(url_veracrypt_linux_sig, path_veracrypt_tarfile_sig)
        
        self.yellow('Importando key veracrypt')
        os.system('curl -s https://www.idrix.fr/VeraCrypt/VeraCrypt_PGP_public_key.asc | gpg --import - 1> /dev/null 2>&1')

        # Verificar a intergridade do arquivo ".txt" que contém as hashs 
        if check_gpg(path_veracrypt_tarfile_sig, path_veracrypt_tarfile) != True:
            self.red(f'Arquivo não confiavel: {path_veracrypt_tarfile}')
            return False
        
        unpack_tar(path_veracrypt_tarfile)
        os.chdir(DirUnpack)
        files_in_dir = os.listdir(DirUnpack)
        for file in files_in_dir:
            if 'setup-gui-x64' in file:
                print(f'Executando ... {DirUnpack}/{file}')
                os.system(f'./{file}')

        if is_executable('veracrypt'):
            self.green('Veracrypt instalado com sucesso')
            return True
        else:
            self.red('Falha na instalação de Veracrypt')
            return False

    def freebsd(self):
        '''
        Requerimentos: FUSE library and tools, device mapper tools
        '''
        urls = self.veracrypt_urls()
        for URL in urls:
            if (URL[-4:] == '.bz2') and ('freebsd' in URL) and ('setup' in URL) and (not 'legacy' in URL):
                url_veracrypt_freebsd = URL
                url_veracrypt_freebsd_sig = f'{URL}.sig'
                break
        
        # Definir o camiho completo do arquivo a ser baixado
        path_veracrypt_tarfile = '{}/{}'.format(DirDownloads, os.path.basename(url_veracrypt_freebsd))
        path_veracrypt_tarfile_sig = f'{path_veracrypt_tarfile}.sig'
        
        run_download(url_veracrypt_freebsd, path_veracrypt_tarfile)
        run_download(url_veracrypt_freebsd_sig, path_veracrypt_tarfile_sig)
        
        self.yellow('Importando key veracrypt')
        os.system('curl -s https://www.idrix.fr/VeraCrypt/VeraCrypt_PGP_public_key.asc | gpg --import - 1> /dev/null 2>&1')

        if check_gpg(path_veracrypt_tarfile_sig, path_veracrypt_tarfile) != True:
            self.red(f'Arquivo não confiavel: {path_veracrypt_tarfile}')
            return False
        
        UnpackFiles().tar(path_veracrypt_tarfile)
        os.chdir(DirUnpack)
        files_in_dir = os.listdir(DirUnpack)
        for file in files_in_dir:
            if 'setup-gui-x64' in file:
                print(f'Executando ... {DirUnpack}/{file}')
                os.system(f'./{file}')
                
        if os.path.isfile('/usr/share/applications/veracrypt.desktop'):
            print('Copiando ... /usr/share/local/applications/veracrypt.desktop')
            os.system('sudo cp /usr/share/applications/veracrypt.desktop /usr/local/share/applications/veracrypt.desktop')

        if is_executable('veracrypt'):
            self.green('Veracrypt instalado com sucesso')
            return True
        else:
            self.red('Falha na instalação de Veracrypt')
            return False
            
    def remove(self):
        self.msg('Desisntalando veracrypt')
        os.system('sudo /usr/bin/veracrypt-uninstall.sh')

    def install(self):
        if is_executable('veracrypt'):
            self.yellow('veracrypt já está instalado use a opção "--remove" para desinstalar.')
            return
            
        self.msg('Instalando veracrypt')
        if platform.system() == 'FreeBSD':
            self.freebsd()
        elif platform.system() == 'Linux':
            self.linux_tar()

#-----------------------------------------------------------#
# Desenvolvimento
#-----------------------------------------------------------#
class Java(PrintText):
    def __init__(self):
        pass    

    def install(self):
        self.msg('Instalando: jre11-openjdk jre11-openjdk-headless')
        if platform.system() == 'Linux':
            if ReleaseInfo().info('ID') == 'arch':
                Pacman().install('jre11-openjdk jre11-openjdk-headless')

class Idea(PrintText):
    def __init__(self):
        if platform.system() == 'Linux':
            self.idea_url = 'https://download-cf.jetbrains.com/idea/ideaIC-2020.2.1.tar.gz'
            self.idea_tar_file = os.path.abspath(os.path.join(DirDownloads, os.path.basename(self.idea_url)))
            self.shasum = 'a107f09ae789acc1324fdf8d22322ea4e4654656c742e4dee8a184e265f1b014'
            self.idea_dir = os.path.abspath(os.path.join(DirBin, 'idea-IC'))
            self.idea_script = os.path.abspath(os.path.join(DirBin, 'idea'))
            self.idea_file_desktop = os.path.abspath(os.path.join(DirDesktopFiles, 'jetbrains-idea.desktop')) 
            self.idea_png = os.path.abspath(os.path.join(DirIcons, 'idea.png'))
        elif platform.system() == 'Windows':
            pass

    def linux_tar(self):
        '''
        Instalação do idea community via pacote tar.
        '''
        run_download(self.idea_url, self.idea_tar_file)
        if sha256(self.idea_tar_file, self.shasum) == False:
            return False

        unpack_tar(self.idea_tar_file)
        os.chdir(DirUnpack)
        print(f'Movendo ... {self.idea_dir}')
        os.system(f'mv idea-* {self.idea_dir}')
        os.chdir(self.idea_dir)
        os.system(f'cp ./bin/idea.png {self.idea_png}')
        
        idea_desktop_info = [
            "[Desktop Entry]",
            "Name=IntelliJ IDEA Ultimate Edition",
            "Version=1.0",
            "Comment=java"
            f"Icon={self.idea_png}",
            f"Exec='{self.idea_dir}/bin/idea.sh' %f",
            "Terminal=false",
            "Categories=Development;IDE",
            "Type=Application",
        ]

        print('Criando arquivo ".desktop"')
        f = open(self.idea_file_desktop, 'w')
        for line in idea_desktop_info:
            f.write(f'{line}\n')

        f.seek(0)
        f.close()
        
        # Criar atalho para execução na linha de comando.
        f = open(self.idea_script, 'w')
        f.write("#!/bin/sh\n")
        f.write(f"\ncd {self.idea_dir}/bin/ \n")
        f.write("./idea.sh $@")
        f.seek(0)
        f.close()

        os.system(f"chmod +x {self.idea_script}")
        
    def remove(self):
        print('Desisntalando "idea IC community"')
        if platform.system() == 'Linux':
            if os.path.exists(self.idea_dir):
                self.red(f'Removendo ... {self.idea_dir}')
                os.system(f'rm -rf {self.idea_dir}')

            if os.path.exists(self.idea_script):
                self.red(f'Removendo ... {self.idea_script}')
                os.system(f'rm -rf {self.idea_script}')

            if os.path.exists(self.idea_png):
                self.red(f'Removendo ... {self.idea_png}')
                os.system(f'rm -rf {self.idea_png}')

    def install(self):
        if platform.system() == 'Linux':
            if ReleaseInfo().info('ID') == 'arch':
                Pacman().install('intellij-idea-community-edition')
            else:
                self.linux_tar()

class Pycharm(PrintText):
    def __init__(self):
        if platform.system() == 'Linux':
            self.pycharm_shasum = '60b2eeea5237f536e5d46351fce604452ce6b16d037d2b7696ef37726e1ff78a'  
            self.pycharm_url = 'https://download-cf.jetbrains.com/python/pycharm-community-2020.2.tar.gz'
            self.pycharm_tar_file = os.path.abspath(os.path.join(DirDownloads, os.path.basename(self.pycharm_url)))
            self.pycharm_dir = os.path.abspath(os.path.join(DirBin, 'pycharm-community'))
            self.pycharm_script = os.path.abspath(os.path.join(DirBin, 'pycharm'))
            self.pycharm_file_desktop = os.path.abspath(os.path.join(DirDesktopFiles, 'pycharm.desktop')) 
            self.pycharm_png = os.path.abspath(os.path.join(DirIcons, 'pycharm.png'))
        elif platform.system() == 'Windows':
            self.pycharm_shasum = '65afa1b90f3ecc45946793c4c43a47a46dff2e1da0737ce602f5ee12bd946f1e'
            self.pycharm_url = 'https://download-cf.jetbrains.com/python/pycharm-community-2020.2.exe'
            self.pycharm_name = os.path.basename(self.pycharm_url)
            self.pycharm_pkg = os.path.abspath(os.path.join(DirDownloads, self.pycharm_name))

    def windows(self):
        run_download(self.pycharm_url, self.pycharm_pkg)
        if sha256(self.pycharm_pkg, self.pycharm_shasum) != True:
            return False

        os.system(self.pycharm_pkg)

    def linux_tar(self):
        if is_executable('pycharm'):
            print('Pycharm já instalado use "--remove pycharm" para desinstalar.')
            return

        run_download(self.pycharm_url, self.pycharm_tar_file)
        if sha256(self.pycharm_tar_file, self.pycharm_shasum) != True:
            return False

        unpack.tar(self.pycharm_tar_file)
        os.chdir(DirUnpack)
        print(f'Movendo ... {self.pycharm_dir}')
        os.system('mv pycharm-* {}'.format(self.pycharm_dir))
        os.chdir(self.pycharm_dir)
        os.system(f'cp -R ./bin/pycharm.png {self.pycharm_png}')

        pycharm_desktop_info = [
            "[Desktop Entry]",
            "Name=Pycharm Community",
            "Version=1.0",
            f"Icon={self.pycharm_png}",
            "Exec=pycharm",
            "Terminal=false",
            "Categories=Development;IDE;",
            "Type=Application",
        ]

        print('Criando arquivo ".desktop"')
        f = open(self.pycharm_file_desktop, 'w')
        for line in pycharm_desktop_info:
            f.write(f'{line}\n')

        f.seek(0)
        f.close()

        # Criar atalho para execução na linha de comando.
        f = open(self.pycharm_script, 'w')
        f.write("#!/bin/sh\n")
        f.write(f"\ncd {self.pycharm_dir}/bin/ \n")
        f.write("./pycharm.sh $@")
        f.seek(0)
        f.close()

        os.system(f"chmod +x {self.pycharm_script}")

    def remove(self):
        print('Desisntalando "pycharm community"')
        if platform.system() == 'Linux':
            if os.path.exists(self.pycharm_dir):
                self.red(f'Removendo ... {self.pycharm_dir}')
                os.system(f'rm -rf {self.pycharm_dir}')

            if os.path.exists(self.pycharm_script):
                self.red(f'Removendo ... {self.pycharm_script}')
                os.system(f'rm -rf {self.pycharm_script}')

            if os.path.exists(self.pycharm_png):
                self.red(f'Removendo .. {self.pycharm_png}')
                os.system(f'rm -rf {self.pycharm_png}')

    def install(self):
        if platform.system() == 'Linux':
            if ReleaseInfo().info('ID') == 'arch': # No archlinux pycharm pode ser instalado com o pacman.
                #Pacman().install('pycharm-community-edition')
                self.linux_tar()
            else:
                self.linux_tar()
        elif platform.system() == 'Windows':
            self.windows()
     
#-----------------------------------------------------------#
# Escritório
#-----------------------------------------------------------#
     
class MsFonts(PrintText):
    def __init__(self):
        pass    

    def archlinux(self):
        '''
        Instalar fontes microsoft no ArchLinux.
        '''
        os.chdir(DirGitclone)
        gitclone('https://aur.archlinux.org/ttf-ms-fonts.git')
        os.chdir('ttf-ms-fonts')
        self.blue('Executando: makepkg -s -f')
        os.system('makepkg -s -f')

        files = os.listdir('.')
        for f in files:
            if ('.tar.zst' in f) and ('ttf-ms-fonts' in f):
                print('Renomeando ... ttf-ms-fonts.tar.zst')
                shutil.move(f, 'ttf-ms-fonts.tar.zst')

        print('Executando ... sudo pacman -U --noconfirm ttf-ms-fonts.tar.zst')
        os.system('sudo pacman -U --noconfirm ttf-ms-fonts.tar.zst')

    def install(self):
        if platform.system() == 'Linux':
            if ReleaseInfo().info('ID') == 'arch':
                self.archlinux()
            

#-----------------------------------------------------------#
# Navegadores
#-----------------------------------------------------------#
class Browser(PrintText):
    def __init__(self):
        self.google_chrome_url_deb = 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'
        
    def google_chrome_debian(self):
        '''
        Instalar Google chrome no Debian
        '''
        google_chrome_repo_debian = 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main'
        self.green('Adicionando key e repositório google-chrome')
        os.system("wget -q 'https://dl.google.com/linux/linux_signing_key.pub' -O- | sudo apt-key add -")
        os.system(f'echo "{google_chrome_repo_debian}" | sudo tee /etc/apt/sources.list.d/google-chrome.list')
        AptGet().update()
        AptGet().install('google-chrome-stable')

    def google_chrome_fedora(self):
        '''
        Instalar Google chrome no Fedora
        '''
        self.yellow('Executando ... dnf install fedora-workstation-repositories')
        os.system('sudo dnf install -y fedora-workstation-repositories')
        self.yellow('sudo dnf config-manager --set-enabled google-chrome')
        os.system('sudo dnf config-manager --set-enabled google-chrome')
        os.system('sudo dnf install -y google-chrome-stable')
        
    def google_chrome_archlinux(self):
        '''
        Instalar Google chrome no ArchLinux
        '''
        os.chdir(DirTemp)
        os.system('git clone https://aur.archlinux.org/google-chrome.git')
        Pacman().install('base-devel pipewire')
        os.chdir('google-chrome')
        self.blue('Executando: makepkg -s -f')
        os.system('makepkg -s -f')
        files = os.listdir('.')
        for f in files:
            if ('.tar.zst' in f) and ('google-chrome' in f):
                print('Renomeando ... google-chrome.tar.zst')
                shutil.move(f, 'google-chrome.tar.zst')
         
        print('Executando ... sudo pacman -U --noconfirm google-chrome.tar.zst')
        os.system('sudo pacman -U --noconfirm google-chrome.tar.zst')
        
    def google_chrome(self):
        if is_executable('google-chrome-stable') == True:
            self.yellow('google-chrome já está instalado...')
            return True

        self.msg('Instalando google-chrome')
        info = ReleaseInfo().info('ID') # Detectar qual o sistema base.
        if info == 'arch':
            self.google_chrome_archlinux()
        elif info == 'debian':
            self.google_chrome_debian()
        elif info == 'fedora':
            self.google_chrome_fedora()
        else:
            self.red('Instalação do google-chrome indisponível para o seu sistema')
            sleep(1)

    def opera_stable_archlinux(self):
        pass

    def opera_stable_debian(self):
        opera_repo_debian='deb [arch=amd64] https://deb.opera.com/opera-stable/ stable non-free'
        opera_file='/etc/apt/sources.list.d/opera-stable.list'

        self.yellow("Importando key")
        os.system('wget -q http://deb.opera.com/archive.key -O- | sudo apt-key add -')
        self.yellow("Adicionando repositório")
        os.system(f'echo "{opera_repo_debian}" | sudo tee {opera_file}')
        AptGet().update()
        AptGet().install('opera-stable')

    def opera_stable_fedora(self):
        os.system("Executando ... sudo rpm --import https://rpm.opera.com/rpmrepo.key")
        os.system('sudo rpm --import https://rpm.opera.com/rpmrepo.key')
        print(f'Executando ... cd {DirTemp}')
        os.chdir(DirTemp)

        self.yellow("Adicionando repositório")
        # Gerar arquivo/repositório
        repos = (
            "[opera]"
            "name=Opera packages"
            "type=rpm-md"
            "baseurl=https://rpm.opera.com/rpm"
            "gpgcheck=1"   
            "gpgkey=https://rpm.opera.com/rpmrepo.key"
            "enabled=1"
            )

        file = open(opera.repo, 'w')
        for line in repos:
            file.write(f'{line}\n')
        file.seek(0)
        file.close()
        os.system('sudo mv opera.repo /etc/yum.repos.d/opera.repo')
        os.system('sudo dnf install opera-stable')

    def opera_stable(self):
        if is_executable('opera-stable') == True:
            self.yellow('opera-stable já está instalado...')
            return True

        self.msg('Instalando opera-stable')
        info = ReleaseInfo().info('ID') # Detectar qual o sistema base.
        if info == 'arch':
            self.opera_stable_archlinux()
        elif info == 'debian':
            self.opera_stable_debian()
        elif info == 'fedora':
            self.opera_stable_fedora()
        else:
            self.red('Instalação de opera-stable indisponível para o seu sistema')
            sleep(1)

    def torbrowser(self):
        '''
        Instalar torbrowser em qualquer distribuição Linux.
        '''
        if platform.system() == 'Linux':
            url_torbrowser_installer = 'https://raw.github.com/Brunopvh/torbrowser/master/tor.sh'
            path_torbrowser_installer = os.path.abspath(os.path.join(DirDownloads, 'tor.sh'))
            run_download(url_torbrowser_installer, path_torbrowser_installer)
            os.system(f'chmod +x {path_torbrowser_installer}')
            os.system(f'{path_torbrowser_installer} --install')
        else:
            print('[!] Instalação do "Navegador tor não está disponível para o seu sistema."')
            return False

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
        run_download(self.URL, self.path_file_zip)
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
        run_download(self.URL, self.path_file_zip)
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
        Pkg().install('py27-wxPython30') # Instalar dependências
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
        
#-----------------------------------------------------------#
# Preferências
#-----------------------------------------------------------#
class Papirus(PrintText):
    def __init__(self):
        self.papirus_url = 'https://github.com/PapirusDevelopmentTeam/papirus-icon-theme/archive/master.tar.gz'
        self.papirus_tar_file = os.path.abspath(os.path.join(DirDownloads, 'papirus.tar.gz'))
        self.dir_papirus = os.path.abspath(os.path.join(DirIcons, 'Papirus'))
        self.dir_papirus_dark = os.path.abspath(os.path.join(DirIcons, 'Papirus-Dark'))
        self.dir_papirus_light = os.path.abspath(os.path.join(DirIcons, 'Papirus-Light'))
        self.dir_epapirus = os.path.abspath(os.path.join(DirIcons, 'ePapirus'))

    def papirus_tar(self):
        self.msg('Instalando papirus')
        run_download(self.papirus_url, self.papirus_tar_file)
        unpack.tar(self.papirus_tar_file)
        os.chdir(DirUnpack)
        os.system('mv papirus-* papirus')
        os.chdir('papirus')

        if os.path.isdir(self.dir_papirus) == True:
            self.red(f'Removendo ... {self.dir_papirus}')
            shutil.rmtree(self.dir_papirus)

        if os.path.isdir(self.dir_papirus_dark) == True:
            self.red(f'Removendo ... {self.dir_papirus_dark}')
            shutil.rmtree(self.dir_papirus_dark)

        if os.path.isdir(self.dir_papirus_light) == True:
            self.red(f'Removendo ... {self.dir_papirus_light}')
            shutil.rmtree(self.dir_papirus_light)

        if os.path.isdir(self.dir_epapirus) == True:
            self.red(f'Removendo ... {self.dir_epapirus}')
            shutil.rmtree(self.dir_epapirus)

        self.green(f'Instalando ... {self.dir_papirus}')
        os.system(f'cp -R Papirus {self.dir_papirus}')

        self.green(f'Instalando ... {self.dir_papirus_dark}')
        os.system(f'cp -R Papirus-Dark {self.dir_papirus_dark}')

        self.green(f'Instalando ... {self.dir_papirus_light}')
        os.system(f'cp -R Papirus-Dark {self.dir_papirus_light}')

        self.green(f'Instalando ... {self.dir_epapirus}')
        os.system(f'cp -R Papirus-Dark {self.dir_epapirus}')

    def install(self):
        if platform.system() == 'Linux': # Instalação em sistemas Linux
            if ReleaseInfo().info('ID') == 'arch':
                #Pacman().install('papirus-icon-theme')
                self.papirus_tar()
            else:
                self.papirus_tar()
        elif platform.system() == 'FreeBSD':
            #self.papirus_tar()
            Pkg().install('papirus-icon-theme')
    
#-----------------------------------------------------------#
# Wine
#-----------------------------------------------------------#
class Wine(PrintText):
    def __init__(self):
        pass

    def install(self):
        url_installer_pywine = 'https://raw.github.com/Brunopvh/pywine/master/INSTALL.sh'
        path_installer_pywine = os.path.abspath(os.path.join(DirDownloads, 'wine-installer.sh'))

        if platform.system() == 'Linux':
            run_download(url_installer_pywine, path_installer_pywine)
            os.system(f'chmod +x {path_installer_pywine}')
            self.yellow(f'Executando ... sudo sh {path_installer_pywine}')
            os.system(f'sudo sh {path_installer_pywine}')
            os.system('wine-install --install wine')

