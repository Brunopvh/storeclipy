#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
REFERÊNCIAS
  https://www.it-swarm.dev/pt/python/como-posso-obter-links-href-de-html-usando-python/969762638/
  https://www.crummy.com/software/BeautifulSoup/bs4/doc/
  https://pythonhelp.wordpress.com/tag/hashlib/
'''

import os, sys, stat
import subprocess
import re
import shutil
import urllib.request
import tempfile
import utils
import pkgmanager

#-----------------------------------------------------------#
# Acessórios
#-----------------------------------------------------------#
class Etcher(utils.SetUserConfig, utils.PrintText):
	def __init__(self):
		# https://github.com/balena-io/etcher/releases
		super().__init__(utils.appname, create_dirs=True)
		self.root_dirs = utils.SetRootConfig(utils.appname, create_dirs=True)
		if utils.KERNEL_TYPE == 'Linux':
			self.desktop_file = os.path.abspath(os.path.join(self.dir_desktop_links, 'balena-etcher-electron.desktop'))
			self.etcher_destination_dir = os.path.abspath(os.path.join(self.dir_bin, 'balenaEtcher'))
			self.etcher_destination_file = os.path.abspath(os.path.join(self.etcher_destination_dir, 'balena-etcher-electron.AppImage'))
			self.etcher_script = os.path.abspath(os.path.join(self.dir_bin, 'balena-etcher-electron'))
		else:
			self.etcher_package_path = ''
			self.etcher_url = ''
			self.etcher_destination_dir = ''
		
	def add_desktop_file(self):
		'''
		Criar arquivo .desktop
		'''
		lines_desktop_file = [
		'[Desktop Entry]',
		'Name=balenaEtcher',
		'Exec={}'.format(self.etcher_script),
		'Terminal=false',
		'Type=Application',
		'Icon=balena-etcher-electron',
		'StartupWMClass=balenaEtcher',
		'Comment=Flash OS images to SD cards and USB drives, safely and easily.',
		'MimeType=x-scheme-handler/etcher;',
		'Categories=Utility;',
		]

		obj_desktop_file = utils.ReadFile(self.file_temp)
		obj_desktop_file.write_file(lines_desktop_file)
		print(f'Configurando ... {self.desktop_file}')
		os.system(f'mv {self.file_temp} {self.desktop_file}')
		os.system(f'chmod 755 {self.desktop_file}')

	def add_etcher_script_appimage(self):
		'''
		Método para criar o script que executa o pacote AppImage no sistema.
		'''
		lines_script = [
			'#!/bin/bash',
			f'cd {self.etcher_destination_dir}',
			f'{self.etcher_destination_file} "$@" --no-sandbox',
			]

		obj_script = utils.ReadFile(self.file_temp)
		obj_script.write_file(lines_script)
		os.system(f'mv {self.file_temp} {self.etcher_script}')
		os.system(f'chmod a+x {self.etcher_script}')

	def etcher_appimage(self):
		'''
		Instalar o etcher no formato AppImage em qualquer Linux.
		'''
		self.etcher_url = 'https://github.com/balena-io/etcher/releases/download/v1.5.109/balenaEtcher-1.5.109-x64.AppImage'
		name_etcher = os.path.basename(self.etcher_url)
		self.etcher_package_path = os.path.abspath(os.path.join(self.dir_cache, name_etcher))
		
		if utils.DownloadFiles().curl_download(self.etcher_url, self.etcher_package_path) == False:
			return False
			
		print(f'Instalando em ... {self.etcher_destination_dir}')
		utils.mkdir(self.etcher_destination_dir)
		os.system(f'cp {self.etcher_package_path} {self.etcher_destination_file}')
		os.system(f'chmod a+x {self.etcher_destination_file}')
		self.add_etcher_script_appimage()
		self.add_desktop_file()

	def etcher_debian(self):
		if utils.is_root() == False:
			return False

		self.sblue('Adicionando key e repositório')
		os.system('sudo apt-key adv --keyserver hkps://keyserver.ubuntu.com:443 --recv-keys 379CE192D401AB61')
		os.system(f'echo "deb https://deb.etcher.io stable etcher" | sudo tee /etc/apt/sources.list.d/balena-etcher.list')
		pkgmanager.AptGet().update()
		pkgmanager.AptGet().install('balena-etcher-electron')
		# pkgmanager.AptGet().broke()

	def etcher_windows(self):
		self.etcher_url = 'https://github.com/balena-io/etcher/releases/download/v1.5.45/balenaEtcher-Setup-1.5.45.exe'
		etcher_file_name = os.path.basename(self.etcher_url)
		self.etcher_package_path = os.path.join(self.dir_cache, etcher_file_name)
		utils.DownloadFiles().curl_download(self.etcher_url, self.etcher_package_path)
		os.system(self.etcher_package_path)

	def remove(self):
		if utils.KERNEL_TYPE == 'Linux':
			if utils.ReleaseInfo().get('BASE_DISTRO') == 'debian':
				pkgmanager.AptGet().remove('balena-etcher-electron')
			elif utils.ReleaseInfo().get('ID') == 'arch':
				utils.rmdir(self.etcher_destination_dir)
				utils.rmdir(self.etcher_script)
				utils.rmdir(self.desktop_file)

	def install(self) -> bool:
		if utils.KERNEL_TYPE == 'Linux':
			if utils.ReleaseInfo().get('ID') == 'arch':
				self.etcher_appimage()
			elif utils.ReleaseInfo().get('ID') == 'debian':
				self.etcher_debian()
		elif utils.ReleaseInfo().get('BASE_DISTRO') == 'windows':
			self.etcher_windows()

		print(utils.ReleaseInfo().get('BASE_DISTRO'))
		return
		if shutil.which('balena-etcher-electron') != None:
			self.yellow('balenaEtcher instalado com sucesso.')
			return True
		else:
			self.red('Falha na instalação de balenaEtcher.')
			return False

class Veracrypt(utils.SetUserConfig, utils.PrintText):
	def __init__(self):
		super().__init__(utils.appname, create_dirs=True)
		# Urls e arquivos.
		self.url_download_page = 'https://www.veracrypt.fr/en/Downloads.html'
		self.url_veracrypt_pub_key = 'https://www.idrix.fr/VeraCrypt/VeraCrypt_PGP_public_key.asc'
		self.url_veracrypt_sig = ''
		self.url_veracrypt_package = '' 
		self.path_veracrypt_pub_key = os.path.abspath(os.path.join(self.dir_temp, 'VeraCrypt_PGP_public_key.asc'))
		self.path_veracrypt_sig = ''
		self.path_veracrypt_package = ''
		self.unpack_files = utils.Unpack(destination=self.dir_unpack, clear_dir=True)

	def set_url_veracrypt(self):
		''' 
		Setar as variáveis self.url_veracrypt_package e self.url_veracrypt_sig
		'''
		urls = utils.get_html_links(self.url_download_page)
		RegExpLinux = re.compile(r'https.*.tar.bz2.sig')
		RegExpWindows = re.compile(r'https.*Setup.*.exe.sig')
		for URL in urls:
			if utils.KERNEL_TYPE == 'Linux':
				if RegExpLinux.findall(URL) != []:
					if (not 'freebsd' in URL) and (not 'legacy' in URL) and (not 'Source' in URL):
						self.url_veracrypt_sig = URL
			elif utils.KERNEL_TYPE == 'Windows':
				if (RegExpWindows.findall(URL) != []):
					if (not 'legacy' in URL.lower()):
						self.url_veracrypt_sig = URL

		self.url_veracrypt_package = self.url_veracrypt_sig.replace('.sig', '')

	def linux_tar(self) -> bool:
		# Definir o camiho completo dos arquivos a serem baixados.
		name_tarfile = os.path.basename(self.url_veracrypt_package)
		self.path_veracrypt_package = os.path.abspath(os.path.join(self.dir_cache, name_tarfile))
		self.path_veracrypt_sig = f'{self.path_veracrypt_package}.sig'	
		utils.DownloadFiles().wget_download(self.url_veracrypt_package, self.path_veracrypt_package)
		utils.DownloadFiles().downloader(self.url_veracrypt_sig, self.path_veracrypt_sig)

		utils.utils.gpg_import(self.path_veracrypt_pub_key, self.url_veracrypt_pub_key)

		# Verificar a intergridade do pacote de instalação. 
		if utils.utils.gpg_verify(self.path_veracrypt_sig, self.path_veracrypt_package) != True:
			return False

		self.unpack_files.tar(self.path_veracrypt_package)
		os.chdir(self.dir_unpack)
		RegexSetupFile = re.compile(r'veracrypt-.*-setup-gui-x64')
		files_in_dir = os.listdir(self.dir_unpack)
		for file in files_in_dir:
			if RegexSetupFile.findall(file) != []:
				setup_file_gui = os.path.abspath(os.path.realpath(file))
				break

		print(f'Executando ... {setup_file_gui}')
		if utils.is_root() == False:
			return False
		os.system(f'sh {setup_file_gui}')
		os.system(f'sudo rm {setup_file_gui}')
		if utils.is_executable('veracrypt'):
			self.green('Veracrypt instalado com sucesso')
			return True
		else:
			self.red('Falha na instalação de Veracrypt')
			return False

	def win64_setup(self):
		name_tarfile = os.path.basename(self.url_veracrypt_package)
		self.path_veracrypt_package = os.path.abspath(os.path.join(self.dir_cache, name_tarfile))
		utils.DownloadFiles().wget_download(self.url_veracrypt_package, self.path_veracrypt_package)
	
	def remove(self):
		self.msg('Desisntalando veracrypt')
		if utils.KERNEL_TYPE == 'Linux':
			if utils.is_root() == False:
				return False
			os.system('sudo /usr/bin/veracrypt-uninstall.sh')
		else:
			pass
		
	def install(self):
		self.set_url_veracrypt()
		if (utils.KERNEL_TYPE == 'Linux') or (utils.KERNEL_TYPE == 'FreeBSD'):
			if shutil.which('veracrypt') != None:
				print('veracrypt já está instalado use a opção "--remove" para desinstalar.')
				return True
			self.msg('Instalando veracrypt')
			self.linux_tar()
		elif utils.KERNEL_TYPE == 'Windows':
			self.win64_setup()
		else:
			self.sred('Programa indisponível para o seu sistema')
			return False

#-----------------------------------------------------------#
# Desenvolvimento
#-----------------------------------------------------------#
class Java(utils.PrintText):
	def __init__(self):
		pass    

	def install(self):
		pass

class Idea(utils.SetUserConfig, utils.PrintText):
	def __init__(self):
		super().__init__(utils.appname, create_dirs=True)
		if utils.KERNEL_TYPE == 'Linux':
			self.idea_url = 'https://download-cf.jetbrains.com/idea/ideaIC-2020.2.1.tar.gz'
			self.idea_tar_file = os.path.abspath(os.path.join(self.dir_cache, os.path.basename(self.idea_url)))
			self.shasum_tar_file = 'a107f09ae789acc1324fdf8d22322ea4e4654656c742e4dee8a184e265f1b014'
			self.idea_dir = os.path.abspath(os.path.join(self.dir_bin, 'idea-IC'))
			self.idea_script = os.path.abspath(os.path.join(self.dir_bin, 'idea'))
			self.idea_file_desktop = os.path.abspath(os.path.join(self.dir_desktop_links, 'jetbrains-idea.desktop')) 
			self.idea_png = os.path.abspath(os.path.join(self.dir_icons, 'idea.png'))

		self.unpack_files = utils.Unpack(destination=self.dir_unpack, clear_dir=True)

	def linux_tar(self):
		'''
		Instalação do idea community via pacote tar.
		'''
		# https://www.tutorialspoint.com/python/os_chmod.htm
		if os.path.isdir(self.idea_dir) == True:
			self.syellow('idea-IC já está instalado.')
			#return True

		utils.DownloadFiles().curl_download(self.idea_url, self.idea_tar_file)
		if utils.sha256(self.idea_tar_file, self.shasum_tar_file) == False:
			return False

		self.unpack_files.tar(self.idea_tar_file)
		os.chdir(self.dir_unpack)
		dirs = os.listdir(self.dir_unpack)
		RegexIdeaic = re.compile(r'^idea-')
		for d in dirs:
			if RegexIdeaic.findall(d) != []:
				idea_temp_dir = os.path.abspath(os.path.join(d))
				break
		
		print(f'Copiando {idea_temp_dir} ... {self.idea_dir}', end=' ')
		try:
			shutil.copytree(idea_temp_dir, self.idea_dir, symlinks=True, ignore=None)
		except(FileExistsError):
			self.red('')
			self.sred(f'O arquivo já existe.')
		except Exception as err:
			self.red('Erro')
			print(err)
		else:
			self.sblue('OK')
		
		os.chdir(self.idea_dir)
		shutil.copy('./bin/idea.png', self.idea_png)
		
		idea_desktop_info = [
			"[Desktop Entry]",
			"Name=IntelliJ IDEA Ultimate Edition",
			"Version=1.0",
			"Comment=java",
			f"Icon={self.idea_png}",
			f"Exec={self.dir_bin}/idea",
			"Terminal=false",
			"Categories=Development;IDE",
			"Type=Application",
		]

		idea_script_info = [
			r'#!/bin/sh',
			f'cd {self.idea_dir}/bin',
			r'./idea.sh "$@"',
		]

		obj_desktop_file = utils.ReadFile(self.idea_file_desktop)
		obj_desktop_file.write_file(idea_desktop_info)

		obj_script_idea = utils.ReadFile(self.idea_script)
		obj_script_idea.write_file(idea_script_info)
		os.system(f'chmod +x {self.idea_script}')
		
	def remove(self):
		print('Desisntalando "idea IC community"')
		if utils.KERNEL_TYPE == 'Linux':
			utils.rmdir(self.idea_dir)
			utils.rmdir(self.idea_script)
			utils.rmdir(self.idea_png)
			utils.rmdir(self.idea_file_desktop)
		elif utils.KERNEL_TYPE == 'Windows':
			pass

	def install(self):
		if utils.KERNEL_TYPE == 'Linux':
			self.linux_tar()
		elif utils.KERNEL_TYPE == 'Windows':
			pass
		
class Pycharm(utils.SetUserConfig, utils.PrintText):
	def __init__(self):
		super().__init__(utils.appname)
		if utils.KERNEL_TYPE == 'Linux':
			self.pycharm_shasum = '60b2eeea5237f536e5d46351fce604452ce6b16d037d2b7696ef37726e1ff78a'  
			self.pycharm_url = 'https://download-cf.jetbrains.com/python/pycharm-community-2020.2.tar.gz'
			self.pycharm_tar_file = os.path.abspath(os.path.join(self.dir_cache, os.path.basename(self.pycharm_url)))
			self.pycharm_dir = os.path.abspath(os.path.join(self.dir_bin, 'pycharm-community'))
			self.pycharm_script = os.path.abspath(os.path.join(self.dir_bin, 'pycharm'))
			self.pycharm_file_desktop = os.path.abspath(os.path.join(self.dir_desktop_links, 'pycharm.desktop')) 
			self.pycharm_png = os.path.abspath(os.path.join(self.dir_icons, 'pycharm.png'))
		elif utils.KERNEL_TYPE == 'Windows':
			pass
		
	def windows(self):
		utils.DownloadFiles().curl_download(self.pycharm_url, self.pycharm_pkg)
		if sha256(self.pycharm_pkg, self.pycharm_shasum) != True:
			return False
		os.system(self.pycharm_pkg)

	def linux_tar(self):
		if utils.is_executable('pycharm'):
			print('Pycharm já instalado use "--remove pycharm" para desinstalar.')
			return

		utils.DownloadFiles().curl_download(self.pycharm_url, self.pycharm_tar_file)
		if utils.sha256(self.pycharm_tar_file, self.pycharm_shasum) != True:
			return False

		utils.Unpack(self.dir_unpack).tar(self.pycharm_tar_file)
		os.chdir(self.dir_unpack)
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

		# Criar atalho para execução na linha de comando.
		pycharm_script_info = [
			"#!/bin/sh",
			f"cd {self.pycharm_dir}/bin",
			r"./pycharm.sh $@",
		]

		obj_desktop_file_pycharm = utils.ReadFile(self.pycharm_file_desktop)
		obj_desktop_file_pycharm.write_file(pycharm_desktop_info)
		obj_script_pycharm = utils.ReadFile(self.pycharm_script)
		obj_script_pycharm.write_file(pycharm_script_info)
		os.system(f"chmod +x {self.pycharm_script}")

	def remove(self):
		print('Desisntalando "pycharm community"')
		if utils.KERNEL_TYPE == 'Linux':
			utils.rmdir(self.pycharm_dir)
			utils.rmdir(self.pycharm_script)
			utils.rmdir(self.pycharm_png)
			utils.rmdir(self.pycharm_file_desktop)
		elif utils.KERNEL_TYPE == 'Windows':
			pass

	def install(self):	
		if utils.KERNEL_TYPE == 'Linux':	
			self.linux_tar()	
		elif utils.KERNEL_TYPE == 'Windows':
			pass
	 
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
class Browser(utils.SetUserConfig, utils.PrintText):
	def __init__(self):
		super().__init__(utils.appname)
		self.urls_google_chrome = {
			'debian': 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb',
			'fedora': None,
			'windows': None
		}

		self.os_info = utils.ReleaseInfo().get('ALL')
		if self.os_info['BASE_DISTRO'] == 'debian':
			self.url = self.urls_google_chrome['debian']
		elif self.os_info['BASE_DISTRO'] == 'fedora':
			self.url = self.urls_google_chrome['fedora']
		elif self.os_info['BASE_DISTRO'] == 'windows':
			self.url = self.urls_google_chrome['windows']
		
	def google_chrome_debian(self):
		'''
		Instalar Google chrome no Debian
		'''
		if utils.is_root() == False:
			return False

		try:
			pkgmanager.AptGet().key_add('https://dl.google.com/linux/linux_signing_key.pub')
		except:
			sys.exit(1)
		
		self.green('Adicionando repositório google-chrome')
		google_chrome_tempfile = tempfile.NamedTemporaryFile(delete=True).name 
		obj_temp_file = utils.ReadFile(google_chrome_tempfile)
		obj_temp_file.write_file(['deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main'])
		os.system(f'sudo mv {google_chrome_tempfile} /etc/apt/sources.list.d/google-chrome.list')
		pkgmanager.AptGet().update()
		pkgmanager.AptGet().install('google-chrome-stable')

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
		os.chdir(self.dir_temp)
		utils.DownloadFiles().gitclone('https://aur.archlinux.org/google-chrome.git', self.dir_gitclone)
		utils.Pacman().install('base-devel pipewire')
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
			#return True

		self.msg('Instalando google-chrome')
		if self.os_info['BASE_DISTRO'] == 'arch':
			self.google_chrome_archlinux()
		elif self.os_info['BASE_DISTRO'] == 'debian':
			self.google_chrome_debian()
		elif self.os_info['BASE_DISTRO'] == 'fedora':
			self.google_chrome_fedora()
		elif self.os_info['BASE_DISTRO'] == 'windows':
			pass
		else:
			self.red('Instalação do google-chrome indisponível para o seu sistema')
			sleep(1)

	def opera_stable_archlinux(self):
		pass

	def opera_stable_debian(self):
		if utils.is_root() == False:
			return False
			
		try:
			pkgmanager.AptGet().key_add('http://deb.opera.com/archive.key')
		except Exception as err:
			print(err)
			sys.exit(1)
		# Adicionar repositório em sources.list.d
		self.green("Adicionando repositório")
		obj_opera_stable_temp_file = utils.ReadFile(self.file_temp)
		obj_opera_stable_temp_file.write_file(['deb [arch=amd64] https://deb.opera.com/opera-stable/ stable non-free'])
		os.system('sudo mv {} {}'.format(self.file_temp, '/etc/apt/sources.list.d/opera-stable.list'))
		pkgmanager.AptGet().update()
		utils.AptGet().install('opera-stable')

	def opera_stable_fedora(self):
		os.system("Executando ... sudo rpm --import https://rpm.opera.com/rpmrepo.key")
		os.system('sudo rpm --import https://rpm.opera.com/rpmrepo.key')
		print(f'Executando ... cd {self.dir_temp}')
		os.chdir(self.dir_temp)

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
		if self.os_info['BASE_DISTRO'] == 'arch':
			self.opera_stable_archlinux()
		elif self.os_info['BASE_DISTRO'] == 'debian':
			self.opera_stable_debian()
		elif self.os_info['BASE_DISTRO'] == 'fedora':
			self.opera_stable_fedora()
		elif self.os_info['BASE_DISTRO'] == 'windows':
			pass
		else:
			self.red('Instalação de opera-stable indisponível para o seu sistema')
			sleep(1)

	def torbrowser(self):
		if utils.KERNEL_TYPE == 'Linux':
			url_torbrowser_installer = 'https://raw.github.com/Brunopvh/torbrowser/master/tor.sh'
			path_torbrowser_installer = os.path.abspath(os.path.join(DirDownloads, 'tor.sh'))
			utils.DownloadFiles().curl_download(url_torbrowser_installer, path_torbrowser_installer)
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
		self.path_asc_philipp = os.path.abspath(os.path.join(self.dir_temp, 'philipp.asc'))
		self.path_youtube_dl_sig = os.path.abspath(os.path.join(self.dir_temp, 'youtube-dl.sig'))
		self.path_youtube_dl_file = os.path.abspath(os.path.join(DirDownloads, 'youtube-dl'))

		if utils.KERNEL_TYPE == 'Windows':
			self.url_youtube_dl += '.exe'
		
	def linux(self):
		utils.DownloadFiles().curl_download(self.url_asc_philipp, self.path_asc_philipp)
		utils.DownloadFiles().curl_download(self.url_youtubedl_sig, self.path_youtube_dl_sig)
		utils.DownloadFiles().curl_download(self.url_youtube_dl, self.path_youtube_dl_file)
		utils.gpg_import(self.path_asc_philipp)
		if (utils.gpg_verify(self.path_youtube_dl_sig, self.path_youtube_dl_file) != True):
			return False

		os.system(f'cp {self.path_youtube_dl_file} {self.dir_bin}/youtube-dl')
		os.system(f'chmod +x {self.dir_bin}/youtube-dl')
	   
	def install(self):
		self.msg('Instalando ... youtube-dl')
		self.linux()
		
class YoutubeDlGui(utils.PrintText):
	def __init__(self):
		self.URL = 'https://github.com/MrS0m30n3/youtube-dl-gui/archive/master.zip'
		self.path_file_zip = os.path.abspath(os.path.join(DirDownloads, 'youtube-dlg.zip'))
		self.destination_ytdlg = os.path.abspath(os.path.join(self.dir_bin, 'youtube_dl_gui'))
		self.exec_ytdl = os.path.abspath(os.path.join(self.dir_bin, 'youtube-dl-gui')) 
				
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
		utils.DownloadFiles().curl_download(self.URL, self.path_file_zip)
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
		os.chdir(self.dir_temp)
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
		self.dir_papirus = os.path.abspath(os.path.join(self.dir_icons, 'Papirus'))
		self.dir_papirus_dark = os.path.abspath(os.path.join(self.dir_icons, 'Papirus-Dark'))
		self.dir_papirus_light = os.path.abspath(os.path.join(self.dir_icons, 'Papirus-Light'))
		self.dir_epapirus = os.path.abspath(os.path.join(self.dir_icons, 'ePapirus'))

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

