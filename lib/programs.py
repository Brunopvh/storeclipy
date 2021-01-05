#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
REFERÊNCIAS
  https://www.it-swarm.dev/pt/python/como-posso-obter-links-href-de-html-usando-python/969762638/
  https://www.crummy.com/software/BeautifulSoup/bs4/doc/
  https://pythonhelp.wordpress.com/tag/hashlib/
'''

import os, sys
import subprocess
import shutil
import urllib.request
import utils


#-----------------------------------------------------------#
# Acessórios
#-----------------------------------------------------------#
class Etcher(utils.SetUserConfig, utils.PrintText):
	def __init__(self):
		# https://github.com/balena-io/etcher/releases
		super().__init__(utils.appname, create_dirs=True)
		self.root_dirs = utils.SetRootConfig(utils.appname, create_dirs=True)
		if utils.KERNEL_TYPE == 'Linux':
			self.desktop_file = '/usr/share/applications/balena-etcher-electron.desktop'
			self.etcher_destination = '/opt/balenaEtcher'
		else:
			self.etcher_package = ''
			self.etcher_url = ''
			self.etcher_destination = ''
		
	def add_desktop_file(self):
		'''
		Criar arquivo .desktop
		'''
		lines = [
			'[Desktop Entry]',
			'Name=balenaEtcher',
			'Exec=/opt/balenaEtcher/balena-etcher-electron %U',
			'Terminal=false',
			'Type=Application',
			'Icon=balena-etcher-electron',
			'StartupWMClass=balenaEtcher',
			'Comment=Flash OS images to SD cards and USB drives, safely and easily.',
			'MimeType=x-scheme-handler/etcher;',
			'Categories=Utility;',
		]

		obj_file = utils.ReadFile(self.file_temp)
		obj_file.write_file(lines)
		
		self.yellow(f'Configurando ... {self.desktop_file}')
		os.system(f'sudo mv {self.file_temp} {self.desktop_file}')
		os.system(f'sudo chown root:root {self.desktop_file}')
		os.system(f'sudo chmod 755 {self.desktop_file}')

	def add_etcher_script_appimage(self):
		'''
		Método para criar o script que executa o pacote AppImage no sistema.
		'''
		lines = [
			'#!/bin/bash',
			'script_dir="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"',
			'if [[ $EUID -ne 0 ]] || [[ $ELECTRON_RUN_AS_NODE ]]; then',
			'"${script_dir}"/balena-etcher-electron.AppImage "$@"',
			'else',
			'"${script_dir}"/balena-etcher-electron.AppImage "$@" --no-sandbox',
			'fi',
		]

		obj_script = utils.ReadFile(self.file_temp)
		obj_script.write_file(lines)

		self.yellow(f'Configurando ... /opt/balenaEtcher/balena-etcher-electron')
		os.system(f'sudo mv {self.file_temp} /opt/balenaEtcher/balena-etcher-electron')
		os.system(f'sudo chown root:root /opt/balenaEtcher/balena-etcher-electron')
		os.system(f'sudo chmod a+x /opt/balenaEtcher/balena-etcher-electron')

	def etcher_appimage(self):
		'''
		Instala o etcher no formato AppImage em qualquer Linux.
		'''
		self.etcher_url = 'https://github.com/balena-io/etcher/releases/download/v1.5.109/balenaEtcher-1.5.109-x64.AppImage'
		name_etcher = os.path.basename(self.etcher_url)
		self.etcher_package = os.path.abspath(os.path.join(self.dir_cache, name_etcher))
		
		if utils.DownloadFiles().curl_download(self.etcher_url, self.etcher_package) == False:
			return False
			
		self.yellow(f'Instalando em ... {self.etcher_destination}')
		os.system(f'sudo mkdir -p {self.etcher_destination}')
		os.system(f'sudo cp {self.etcher_package} /opt/balenaEtcher/balena-etcher-electron.AppImage')
		os.system('sudo chmod a+x /opt/balenaEtcher/balena-etcher-electron.AppImage')
		os.system('sudo ln -sf /opt/balenaEtcher/balena-etcher-electron /usr/local/bin/balena-etcher-electron')
		self.add_etcher_script_appimage()
		self.add_desktop_file()

	def etcher_archlinux(self):
		'''
		Instalar o etcher no archlinux, apartir de um pacote ".deb"
		'''
		self.etcher_url = 'https://github.com/balena-io/etcher/releases/download/v1.5.107/balena-etcher-electron_1.5.107_amd64.deb'
		name_etcher = os.path.basename(self.etcher_url)
		self.etcher_package = os.path.abspath(os.path.join(DirDownloads, name_etcher))
		curl_download(self.etcher_url, self.etcher_package)
		Unpack().deb(self.etcher_package)
		os.chdir(DirUnpack)
		self.yellow(f'Descomprimindo ... {DirUnpack}/data.tar.bz2')
		os.system('sudo tar -jxvf data.tar.bz2 -C / 1> /dev/null')
		print('Criando link ... /usr/local/bin/balena-etcher-electron')
		os.system('sudo chmod a+x /opt/balenaEtcher')
		os.system('sudo ln -sf /opt/balenaEtcher/balena-etcher-electron /usr/local/bin/balena-etcher-electron')

	def etcher_debian(self):
		self.yellow('Adicionando key e repositório')
		os.system('sudo apt-key adv --keyserver hkps://keyserver.ubuntu.com:443 --recv-keys 379CE192D401AB61')
		os.system(f'echo "deb https://deb.etcher.io stable etcher" | sudo tee /etc/apt/sources.list.d/balena-etcher.list')
		AptGet().update()
		AptGet().install('balena-etcher-electron')
		#AptGet().broke()

	def remove(self):
		if utils.KERNEL_TYPE == 'Linux':
			if utils.ReleaseInfo().get('ID') == 'arch':
				rmdir(self.etcher_destination)
				rmdir('/usr/local/bin/balena-etcher-electron')
				rmdir(self.desktop_file)
			elif utils.ReleaseInfo().get('ID') == 'debian':
				AptGet().remove('balena-etcher-electron')

	def install(self):
		if utils.KERNEL_TYPE == 'Linux':
			if utils.ReleaseInfo().get('ID') == 'arch':
				self.etcher_archlinux()
			elif utils.ReleaseInfo().get('ID') == 'debian':
				#self.etcher_debian()
				self.etcher_appimage()

		if utils.is_executable('balena-etcher-electron') == True:
			self.yellow('balenaEtcher instalado com sucesso.')
		else:
			self.red('Falha na instalação de balenaEtcher.')

class Veracrypt(utils.PrintText):
	def __init__(self):
		# Urls e arquivos.
		self.URL = 'https://www.veracrypt.fr/en/Downloads.html'
		self.url_veracrypt_asc = 'https://www.idrix.fr/VeraCrypt/VeraCrypt_PGP_public_key.asc'
		self.url_veracrypt_sig = ''
		self.url_veracrypt_package = '' # Cada método irá determinar sua propria url de download.
		self.path_veracrypt_asc = os.path.abspath(os.path.join(DirTemp, 'VeraCrypt_PGP_public_key.asc'))
		self.path_veracrypt_sig = '' # Cada método definirá no path deste arquivo.
		self.path_veracrypt_package = ''

	def linux_tar(self):
		# Obter o link de download do pacote ".tar".
		urls = get_links(self.URL)
		for URL in urls:
			if (URL[-4:] == '.bz2') and (not 'freebsd' in URL) and ('setup' in URL) and (not 'legacy' in URL):
				self.url_veracrypt_package = URL
				self.url_veracrypt_sig = f'{URL}.sig'
				break
		
		# Definir o camiho completo dos arquivos a serem baixados.
		name_tarfile = os.path.basename(self.url_veracrypt_package)
		self.path_veracrypt_package = os.path.abspath(os.path.join(DirDownloads, name_tarfile))
		self.path_veracrypt_sig = f'{self.path_veracrypt_package}.sig'
		
		curl_download(self.url_veracrypt_package, self.path_veracrypt_package)
		curl_download(self.url_veracrypt_sig, self.path_veracrypt_sig)
		gpg_import(self.path_veracrypt_asc, self.url_veracrypt_asc)

		# Verificar a intergridade do pacote de instalação. 
		if gpg_verify(self.path_veracrypt_sig, self.path_veracrypt_package) != True:
			self.red(f'Arquivo não confiavel: {self.path_veracrypt_package}')
			return False
		
		Unpack().tar(self.path_veracrypt_package)
		os.chdir(DirUnpack)
		files_in_dir = os.listdir(DirUnpack)
		for file in files_in_dir:
			if 'setup-gui-x64' in file:
				setup = file

		print(f'Executando ... {setup}')
		os.system(f'./{setup}')
		os.system(f'sudo rm {setup}')
		if utils.is_executable('veracrypt'):
			self.green('Veracrypt instalado com sucesso')
			return True
		else:
			self.red('Falha na instalação de Veracrypt')
			return False
	
	def remove(self):
		self.msg('Desisntalando veracrypt')
		os.system('sudo /usr/bin/veracrypt-uninstall.sh')
		
	def install(self):
		if utils.is_executable('veracrypt'):
			self.yellow('veracrypt já está instalado use a opção "--remove" para desinstalar.')
			return
			
		self.msg('Instalando veracrypt')
		self.linux_tar()

#-----------------------------------------------------------#
# Desenvolvimento
#-----------------------------------------------------------#
class Java(utils.PrintText):
	def __init__(self):
		pass    

	def install(self):
		self.msg('Instalando: jre11-openjdk jre11-openjdk-headless')
		if utils.KERNEL_TYPE == 'Linux':
			if utils.ReleaseInfo().get('ID') == 'arch':
				Pacman().install('jre11-openjdk jre11-openjdk-headless')
			else:
				pass

class Idea(utils.PrintText):
	def __init__(self):
		self.idea_url = 'https://download-cf.jetbrains.com/idea/ideaIC-2020.2.1.tar.gz'
		self.idea_tar_file = os.path.abspath(os.path.join(DirDownloads, os.path.basename(self.idea_url)))
		self.shasum = 'a107f09ae789acc1324fdf8d22322ea4e4654656c742e4dee8a184e265f1b014'
		self.idea_dir = os.path.abspath(os.path.join(DirBin, 'idea-IC'))
		self.idea_script = os.path.abspath(os.path.join(DirBin, 'idea'))
		self.idea_file_desktop = os.path.abspath(os.path.join(DirDesktopFiles, 'jetbrains-idea.desktop')) 
		self.idea_png = os.path.abspath(os.path.join(DirIcons, 'idea.png'))

	def linux_tar(self):
		'''
		Instalação do idea community via pacote tar.
		'''
		curl_download(self.idea_url, self.idea_tar_file)
		if sha256(self.idea_tar_file, self.shasum) == False:
			return False

		Unpack().tar(self.idea_tar_file)
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
		self.linux_tar()
		
class Pycharm(utils.PrintText):
	def __init__(self):
		self.pycharm_shasum = '60b2eeea5237f536e5d46351fce604452ce6b16d037d2b7696ef37726e1ff78a'  
		self.pycharm_url = 'https://download-cf.jetbrains.com/python/pycharm-community-2020.2.tar.gz'
		self.pycharm_tar_file = os.path.abspath(os.path.join(DirDownloads, os.path.basename(self.pycharm_url)))
		self.pycharm_dir = os.path.abspath(os.path.join(DirBin, 'pycharm-community'))
		self.pycharm_script = os.path.abspath(os.path.join(DirBin, 'pycharm'))
		self.pycharm_file_desktop = os.path.abspath(os.path.join(DirDesktopFiles, 'pycharm.desktop')) 
		self.pycharm_png = os.path.abspath(os.path.join(DirIcons, 'pycharm.png'))
		
	def windows(self):
		curl_download(self.pycharm_url, self.pycharm_pkg)
		if sha256(self.pycharm_pkg, self.pycharm_shasum) != True:
			return False
		os.system(self.pycharm_pkg)

	def linux_tar(self):
		if utils.is_executable('pycharm'):
			print('Pycharm já instalado use "--remove pycharm" para desinstalar.')
			return

		curl_download(self.pycharm_url, self.pycharm_tar_file)
		if sha256(self.pycharm_tar_file, self.pycharm_shasum) != True:
			return False

		Unpack().tar(self.pycharm_tar_file)
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
		self.linux_tar()	
	 
#-----------------------------------------------------------#
# Escritório
#-----------------------------------------------------------#
	 
class MsFonts(utils.PrintText):
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
		if utils.KERNEL_TYPE == 'Linux':
			if utils.ReleaseInfo().get('ID') == 'arch':
				self.archlinux()
			

#-----------------------------------------------------------#
# Navegadores
#-----------------------------------------------------------#
class Browser(utils.PrintText):
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
		if utils.is_executable('google-chrome-stable') == True:
			self.yellow('google-chrome já está instalado...')
			return True

		self.msg('Instalando google-chrome')
		info = utils.ReleaseInfo().get('ID') # Detectar qual o sistema base.
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
		if utils.is_executable('opera-stable') == True:
			self.yellow('opera-stable já está instalado...')
			return True

		self.msg('Instalando opera-stable')
		info = utils.ReleaseInfo().get('ID') # Detectar qual o sistema base.
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
		if utils.KERNEL_TYPE == 'Linux':
			url_torbrowser_installer = 'https://raw.github.com/Brunopvh/torbrowser/master/tor.sh'
			path_torbrowser_installer = os.path.abspath(os.path.join(DirDownloads, 'tor.sh'))
			curl_download(url_torbrowser_installer, path_torbrowser_installer)
			os.system(f'chmod +x {path_torbrowser_installer}')
			os.system(f'{path_torbrowser_installer} --install')
		else:
			print('[!] Instalação do "Navegador tor não está disponível para o seu sistema."')
			return False

#-----------------------------------------------------------#
# Internet
#-----------------------------------------------------------#
class YoutubeDl(utils.PrintText):
	def __init__(self):
		'''
		http://ytdl-org.github.io/youtube-dl/download.html
		'''
		self.url_asc_philipp = 'https://phihag.de/keys/A4826A18.asc'
		self.url_asc_sergey = 'https://dstftw.github.io/keys/18A9236D.asc'
		self.url_youtubedl_sig = 'https://yt-dl.org/downloads/latest/youtube-dl.sig'
		self.url_youtube_dl = 'https://yt-dl.org/downloads/latest/youtube-dl'
		self.path_asc_philipp = os.path.abspath(os.path.join(DirTemp, 'philipp.asc'))
		self.path_youtube_dl_sig = os.path.abspath(os.path.join(DirTemp, 'youtube-dl.sig'))
		self.path_youtube_dl_file = os.path.abspath(os.path.join(DirDownloads, 'youtube-dl'))
		
	def linux(self):
		curl_download(self.url_asc_philipp, self.path_asc_philipp)
		curl_download(self.url_youtubedl_sig, self.path_youtube_dl_sig)
		curl_download(self.url_youtube_dl, self.path_youtube_dl_file)
		gpg_import(self.path_asc_philipp)
		if (gpg_verify(self.path_youtube_dl_sig, self.path_youtube_dl_file) != True):
			return False

		os.system(f'cp {self.path_youtube_dl_file} {DirBin}/youtube-dl')
		os.system(f'chmod +x {DirBin}/youtube-dl')
	   
	def install(self):
		self.msg('Instalando ... youtube-dl')
		self.linux()
		
class YoutubeDlGui(utils.PrintText):
	def __init__(self):
		self.URL = 'https://github.com/MrS0m30n3/youtube-dl-gui/archive/master.zip'
		self.path_file_zip = os.path.abspath(os.path.join(DirDownloads, 'youtube-dlg.zip'))
		self.destination_ytdlg = os.path.abspath(os.path.join(DirBin, 'youtube_dl_gui'))
		self.exec_ytdl = os.path.abspath(os.path.join(DirBin, 'youtube-dl-gui')) 
				
	def twodict(self):
		gitclone('https://github.com/MrS0m30n3/twodict.git')
		self.yellow('Instalando python twodict')
		os.chdir('twodict')
		
		if utils.is_executable('python2.7') == True:
			os.system('sudo python2.7 setup.py install')
		elif utils.is_executable('python2') == True:
			os.system('sudo python2 setup.py install')
		elif utils.is_executable('python') == True:
			os.system('sudo python setup.py install')
		else:
			self.red('Instale o python2 para prosseguir')
			sys.exit('1')
			
	def compile_ytdlg(self):
		curl_download(self.URL, self.path_file_zip)
		Unpack().zip(self.path_file_zip)
		os.chdir(f'{DirUnpack}/youtube-dl-gui-master')
		self.yellow('Compilando youtube-dl-gui')
		if utils.is_executable('python2.7') == True:
			os.system('sudo python2.7 setup.py install')
		elif utils.is_executable('python2') == True:
			os.system('sudo python2 setup.py install')
		elif utils.is_executable('python') == True:
			os.system('sudo python setup.py install')
		else:
			self.red('Instale o python2 para prosseguir')
			sys.exit('1')
	
	def file_desktop_root(self):
		'''
		Cria o arquivo de configuração ".desktop" para o root.
		'''
		os.chdir(DirTemp)
		if utils.KERNEL_TYPE == 'Linux':
			f = '/usr/share/applications/youtube-dl-gui.desktop'
		elif utils.KERNEL_TYPE == 'FreeBSD':
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
		if utils.is_executable('gtk-update-icon-cache'):
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

	def debian(self):
		AptGet().install('python python-pip python-setuptools python-wxgtk3.0 python-twodict gettext')
		self.compile_ytdlg()
		self.file_desktop_root()

	def install(self):
		if utils.is_executable('youtube-dl-gui'):
			self.yellow('Youtube-dl-gui já está instalado')

		self.msg('Instalando youtube-dl-gui')
		if utils.KERNEL_TYPE == 'FreeBSD':
			self.freebsd()
		elif utils.KERNEL_TYPE == 'Linux':
			if utils.ReleaseInfo().get('ID') == 'arch':
				self.archlinux()
			elif utils.ReleaseInfo().get('CODENAME') == 'buster':
				self.debian()
		
#-----------------------------------------------------------#
# Preferências
#-----------------------------------------------------------#
class Papirus(utils.PrintText):
	def __init__(self):
		self.papirus_url = 'https://github.com/PapirusDevelopmentTeam/papirus-icon-theme/archive/master.tar.gz'
		self.papirus_tar_file = os.path.abspath(os.path.join(DirDownloads, 'papirus.tar.gz'))
		self.dir_papirus = os.path.abspath(os.path.join(DirIcons, 'Papirus'))
		self.dir_papirus_dark = os.path.abspath(os.path.join(DirIcons, 'Papirus-Dark'))
		self.dir_papirus_light = os.path.abspath(os.path.join(DirIcons, 'Papirus-Light'))
		self.dir_epapirus = os.path.abspath(os.path.join(DirIcons, 'ePapirus'))

	def papirus_tar(self):
		self.msg('Instalando papirus')
		wget_download(self.papirus_url, self.papirus_tar_file)
		Unpack().tar(self.papirus_tar_file)
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
		if utils.KERNEL_TYPE == 'Linux': # Instalação em sistemas Linux
			if utils.ReleaseInfo().get('ID') == 'arch':
				#Pacman().install('papirus-icon-theme')
				self.papirus_tar()
			elif os.path.isfile('/etc/debian_version') == True:
				AptGet().install('papirus-icon-theme')
			else:
				self.papirus_tar()
		elif utils.KERNEL_TYPE == 'FreeBSD':
			Pkg().install('papirus-icon-theme')
	
#-----------------------------------------------------------#
# Wine
#-----------------------------------------------------------#
class Wine(utils.PrintText):
	def __init__(self):
		pass

	def install(self):
		url_installer_pywine = 'https://raw.github.com/Brunopvh/pywine/master/INSTALL.sh'
		path_installer_pywine = os.path.abspath(os.path.join(DirDownloads, 'wine-installer.sh'))

		if utils.KERNEL_TYPE == 'Linux':
			wget_download(url_installer_pywine, path_installer_pywine)
			os.system(f'chmod +x {path_installer_pywine}')
			self.yellow(f'Executando ... sudo sh {path_installer_pywine}')
			os.system(f'sudo sh {path_installer_pywine}')
			os.system('wine-install --install wine')

