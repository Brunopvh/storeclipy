#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib.colors import SetColor, PrintText as p

s = SetColor()

class YesNo:

	def yesno(text):
		yes_no = str(input(f'[?] {text} [{s.yellow}s{s.reset}/{s.red}n{s.reset}]: '))
		yes_no = yes_no.lower().strip()

		if (yes_no == 's') or (yes_no == 'sim') or (yes_no == 'yes') or (yes_no == 'y'):
			return 'True'
		elif (yes_no == 'n') or (yes_no == 'nao') or (yes_no == 'no'):
			return 'False'
		else:
			p.red('Opção inválida')
			return 'False'