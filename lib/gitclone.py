#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from lib.yesno import YesNo
from lib.colors import PrintText as p, SetColor

class GitClone:
	'''
	Esta classe clona repositórios do github com o comando $ git clone
	O caminho default e o diretório atual. Porém neste programa iremos 
	instanciar esta classe passando como caminho para download dos repositórios
	um diretório em /tmp que será definido por uma variável antes de instanciar 
	a classe por exemplo - gitclone = GitClone('/tmp/caminho/escolhido'), assim
	ao executar um download/clone fazemos gitclone.clone_repo('gihub.com/url.git')
	sempre que desejar alterar o local de download, basta instanciar a classe com
	o caminho de download desejado.
	'''
	def __init__(self, download_dir='.'):
		self.download_dir = download_dir

	def clean_download_dir(self):
		os.chdir(self.download_dir)
		content = os.listdir(self.download_dir)	
		for i in content:
			p.yellow(f'Limpando: {i}')
			try:
				shutil.rmtree(i)
			except:
				p.red(f'Falha ao tentar remover: {i}')
				if YesNo.yesno(f'Deseja remover {i}') == 'True':
					os.system(f'sudo rm -rf {i}')

	def clone_repo(self, repo):
		#self.clean_download_dir()

		p.yellow(f'Clonando: {repo}')
		p.yellow(f'Destino: {self.download_dir}')
		os.chdir(self.download_dir)
		try:
			os.system(f'git clone {repo}')
		except(KeyboardInterrupt):
			print()
			p.red('Interrompido com Ctrl c') 
			sleep(0.2)
		except:
			print()
			p.red(f'Falha ao tentar clonar: {repo}')
			sys.exit('1')