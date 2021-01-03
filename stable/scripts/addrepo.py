#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import sys
import argparse
import tempfile
from os import path, geteuid, makedirs, remove, system
from shutil import copyfile
from time import sleep

__version__ = '2020-06-16'

# Cores
CRed='\033[0;31m'
CGreen='\033[0;32m'
CYellow='\033[0;33m'
CBlue='\033[1;34m'
CWhite='\033[0;37m'
CReset='\033[0m'

# root
if geteuid() != int('0'):
	print(f'{CRed}[!] Você precisa ser o root{CReset}')
	sys.exit('1')

tmpDir = '/tmp/addrepo_temp'
tmpFile = (f'{tmpDir}/tmp.conf')

if path.isdir(tmpDir) == False:
	makedirs(tmpDir)

if path.isfile(tmpFile) == True:
	remove(tmpFile)

def usage():
	print(f"""   
   Use: {path.basename(sys.argv[0])} --repo archlinux
        {path.basename(sys.argv[0])} --repo debian
        {path.basename(sys.argv[0])} --repo fedora
        {path.basename(sys.argv[0])} --repo kalilinux
""")

class OsInfo:
	release_content=open('/etc/os-release', 'rt') 
	releaseLines = release_content.readlines()
	
	@classmethod
	def get_releaselines(cls):
		return cls.releaseLines

	@classmethod
	def get_id(cls):
		for line in cls.releaseLines:
			if line[0:3] == 'ID=':
				os_id = str(line[3:]).replace('\n', '')
				return os_id
				break

	@classmethod
	def get_codename(cls):
		for line in cls.releaseLines:
			if line[0:17] == 'VERSION_CODENAME=':
				os_codename = str(line[17:]).replace('\n', '')
				return os_codename
				break
			else:
				os_codename = ''

		return os_codename

class AddRepo:
	# Obter o nome é codinome do sistema.
	os_id = OsInfo.get_id()
	os_codename = OsInfo.get_codename()

	# repositórios Debian
	debianRepoMain = str((f'deb http://deb.debian.org/debian {os_codename} main'))
	debianRepoContrib = str((f'deb http://deb.debian.org/debian {os_codename} contrib'))
	debianRepoNonfree = str((f'deb http://deb.debian.org/debian {os_codename} non-free'))
	debianMainContribNonfree = str((f'deb http://deb.debian.org/debian {os_codename} main contrib non-free'))

	# repositórios KaliLinux 
	kaliRepoMain = str('deb http://http.kali.org/kali kali-rolling main')
	kaliRepoContrib = str('deb http://http.kali.org/kali kali-rolling contrib')
	kaliRepoNonfree = str('deb http://http.kali.org/kali kali-rolling non-free')
	kaliMainContribNonfree = str('deb http://http.kali.org/kali kali-rolling main non-free contrib')

	# repositórios fedora.

	def __init__(self):
		pass

	def read_files(self, file):
		try:
			f = open(file, 'rt')
		except:
			print()
			print(f'[!] Falha ao tenter abrir o arquivo: {file}')
			return

		content = f.readlines()
		return content

	def archlinux(self):
		# Verificar se o sistema e ArchLinux.
		if self.os_id != 'arch':
			print(f'{CRed}[!] Seu sistema não é ArchLinux{CReset}')
			return
		
		# Criar backup do arquivo /etc/pacman.conf se ainda não existir
		# um backup.
		if path.isfile('/etc/pacman.conf.copia') == True:
			print(f'{CYellow}[+] Backup encontrado: /etc/pacman.conf.copia{CReset}')
		else:
			print(f'{CYellow}[+] Fazendo backup do arquivo: /etc/pacman.conf{CReset}')
			copyfile('/etc/pacman.conf', '/etc/pacman.conf.copia')

		content_conf = open('/etc/pacman.conf', 'rt')
		lines_content_conf = content_conf.readlines()

		for num in range(0, len(lines_content_conf)):
			line = str(lines_content_conf[num]).replace('\n', '')
			
			if (line == str('#[multilib]')) or (line == str('[multilib]')):
				numLineMirrorList = int(num + 1) # Linha que está em baixo do [multilib]
				lines_content_conf[numLineMirrorList] = 'Include = /etc/pacman.d/mirrorlist\n'
				lines_content_conf[num] = '[multilib]\n'

		
		# Gravar o novo conteúdo em um arquivo temporário.
		content_temp = open(tmpFile, 'w+')
		for X in lines_content_conf:
			X = str(X)
			content_temp.write(f'{X}')

		content_temp.seek(0)
		content_temp.close()
		content_conf.close()
		print(f'{CYellow}[+] Configurando: /etc/pacman.conf{CReset}')
		copyfile(tmpFile, '/etc/pacman.conf')

		print(f'{CYellow}[+] Atualizando repostórios {CReset}')
		system('pacman -Sy')
			

	def debian(self):
		# Verificar se o sistema e Debian.
		if self.os_id != 'debian':
			print(f'{CRed}[!] Seu sistema não é Debin{CReset}')
			return
		
		debianSourecesList = open('/etc/apt/sources.list', 'rt')
		contentSources = debianSourecesList.readlines()
		num = int('0')
		for line in contentSources:
		
			line = str(contentSources[num].replace('\n', ''))

			if line == self.debianRepoMain:
				print(f'{CYellow}[+] Removendo repositório main duplicado{CReset}')
				del contentSources[num]
			elif line == self.debianRepoContrib:
				print(f'{CYellow}[+] Removendo repositório contrib duplicado{CReset}')
				del contentSources[num]
			elif line == self.debianRepoNonfree:
				print(f'{CYellow}[+] Removendo repositório non-free duplicado{CReset}')
				del contentSources[num]
			elif line == self.debianMainContribNonfree:
				print(f'{CYellow}[+] Removendo repositório main contrib non-free duplicado{CReset}')
				del contentSources[num]

			num += 1

		contentSources.append(self.debianMainContribNonfree)

		# Gravar o novo conteúdo em um arquivo temporário.
		content_temp = open(tmpFile, 'w')
		for line in contentSources:
			content_temp.write(line)

		content_temp.seek(0)
		content_temp.close()
		debianSourecesList.close()

		# Substituir 'sources.list' pelo novo arquivo temporário
		print(f'{CYellow}[+] Configurando: /etc/apt/sources.list{CReset}')
		copyfile(tmpFile, '/etc/apt/sources.list')

		print(f'{CYellow}[+] Atualizando repostórios {CReset}')
		system('apt update')

	def kali_linux(self):
		contentSources = self.read_files('/etc/apt/sources.list')

		num = int('0')
		for line in contentSources:
		
			line = str(contentSources[num].replace('\n', ''))

			if line == self.kaliRepoMain:
				print(f'{CYellow}[+] Removendo repositório main duplicado{CReset}')
				del contentSources[num]
			elif line == self.kaliRepoContrib:
				print(f'{CYellow}[+] Removendo repositório contrib duplicado{CReset}')
				del contentSources[num]
			elif line == self.kaliRepoNonfree:
				print(f'{CYellow}[+] Removendo repositório non-free duplicado{CReset}')
				del contentSources[num]
			elif line == self.kaliMainContribNonfree:
				print(f'{CYellow}[+] Removendo repositório main contrib non-free duplicado{CReset}')
				del contentSources[num]

			num += 1

		contentSources.append(self.kaliMainContribNonfree)

		# Gravar o novo conteúdo em um arquivo temporário.
		content_temp = open(tmpFile, 'w')
		for line in contentSources:
			content_temp.write(line)

		content_temp.seek(0)
		content_temp.close()
		kaliSourecesList.close()
		print(f'{CYellow}[+] Configurando: /etc/apt/sources.list{CReset}')
		copyfile(tmpFile, '/etc/apt/sources.list')

		print(f'{CYellow}[+] Atualizando repostórios {CReset}')
		system('apt update')

	def fedora(self):
		# sudo dnf repolist
		# sudo dnf repository-packages fedora list
		# sudo dnf repository-packages fedora list available
		# sudo dnf repository-packages fedora list installed
		# sudo vim /etc/yum.repos.d/grafana.repo
		# sudo dnf config-manager --add-repo /etc/yum.repos.d/grafana.repo
		# sudo dnf --enablerepo=grafana install grafana  
		# sudo dnf --disablerepo=fedora-extras install grafana
		# dnf --best upgrade
		# 

		# Verificar se o sistema e Fedora.
		if self.os_id != 'fedora':
			print(f'{CRed}[!] Seu sistema não é Fedora{CReset}')
			return

		repoFusionFree = 'https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release'
		repoFusionNonFree = 'https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release'

		print(f"{CYellow}Adicionando os seguintes repositórios: {CReset}")
		print(repoFusionNonFree)
		print(repoFusionFree)
		print("fedora-workstation-repositories")
		
		system(f'sudo dnf install -y {repoFusionFree}-$(rpm -E %fedora).noarch.rpm')
		system(f'sudo dnf install -y {repoFusionNonFree}-$(rpm -E %fedora).noarch.rpm') 
		system('sudo dnf install -y fedora-workstation-repositories')


parser = argparse.ArgumentParser(description='Habilita repostório em distribuições Linux.')

parser.add_argument(
	'-v', '--version', 
	action='version', 
	version=(f"%(prog)s {__version__}")
	)

parser.add_argument(
	'-u', '--usage',
	action='store_const', 
	dest='usage',
	const=usage,
	help='Mostra ajuda'
	)

parser.add_argument(
	'-r', '--repo', 
	action='store', 
	dest='distro',
	type=str,
	help='Adicionar repostório'
	)


args = parser.parse_args()

if args.usage:
	usage()
elif args.distro:

	if args.distro == 'archlinux':
		AddRepo().archlinux()
	elif args.distro == 'debian':
		AddRepo().debian()
	elif args.distro == 'fedora':
		AddRepo().fedora()
	elif args.distro == 'kalilinux':
		AddRepo().kali_linux()