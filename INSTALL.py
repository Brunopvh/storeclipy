#!/usr/bin/env python3
#

__version__ = '2020-09-09'

import os, sys
import platform
import tempfile
import tarfile
import urllib.request
from pathlib import Path

URL_STORECLIPY='https://github.com/Brunopvh/storeclipy/archive/master.tar.gz'

if (platform.system() == 'FreeBSD') or (platform.system() == 'Linux'):
	# root
	if os.geteuid() != int('0'):
		print('Você precisa ser o "root" saindo...')
		sys.exit('1')
else:
	print('Seu sistema não é suportado...')
	sys.exit()

dir_temp = '/tmp/space_storecli'
#dir_temp = tempfile.mkdtemp()
if os.path.isdir(dir_temp) == False:
	os.makedirs(dir_temp)

if os.path.isdir('/opt') == False:
	os.makedirs('/opt')

print(f'Navegando ... {dir_temp}') 
os.chdir(dir_temp)

print(f'Baixando ... {URL_STORECLIPY}', end=' ')
try:
	urllib.request.urlretrieve(URL_STORECLIPY, 'storeclipy.tar.gz')
except:
	print('Falha no download')
	sys.exit('1')
else:
	print('OK')


print('Descompactando ... storeclipy.tar.gz', end=' ')
try:
	tar = tarfile.open('storeclipy.tar.gz')
	tar.extractall()
	tar.close()
except(KeyboardInterrupt):
	print('Cancelado com Ctrl c')
	sys.exit()
except Exception as err:
	print()
	print(f'Falha na descompressão do  arquivo ... storeclipy.tar.gz\n', err)
	sys.exit('1')
else:
	print('OK')


if os.path.exists('/opt/storeclipy-amd64') == True:
	print('Removendo ... /opt/storeclipy-amd64')
	os.system('rm -rf /opt/storeclipy-amd64')

if os.path.exists('/usr/local/bin/storeclipy') == True:
	os.system('rm -rf /usr/local/bin/storeclipy')

os.system('mv storeclipy-master /opt/storeclipy-amd64')
os.system('chmod -R a+x /opt/storeclipy-amd64')
print('Executando ... ln -sf /opt/storeclipy-amd64/storecli.py /usr/local/bin/storeclipy')
os.system('ln -sf /opt/storeclipy-amd64/storecli.py /usr/local/bin/storeclipy')
os.system('chmod a+x /usr/local/bin/storeclipy')


if os.path.isdir(dir_temp) == True:
	print(f'Removendo ... {dir_temp}')
	os.system(f'rm -rf {dir_temp}')


