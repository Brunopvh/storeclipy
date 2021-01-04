#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils
from time import sleep

REQUERIMENTS_CLI_LINUX = ['curl', 'gpg', 'git', 'xterm', 'kdfja']
REQUERIMENTS_CLI_DEBIAN = ['dirmngr', 'apt-transport-https', 'python3-pip', 'python3-setuptools']


class ConfigureCliRequeriments(utils.PrintText):
	def __init__(self):
		super().__init__()
		self.user_config = utils.SetUserConfig(utils.appname)

	def verify_cli(self):
		for app in REQUERIMENTS_CLI_LINUX:
			print(f'Checando ... {app}', end=' ')
			sleep(0.2)
			if utils.is_executable(app) == True:
				self.green('OK')
			else:
				self.red('')



def verify():
	ConfigureCliRequeriments().verify_cli()
	