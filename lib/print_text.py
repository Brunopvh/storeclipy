#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform

try:
	columns = os.get_terminal_size()[0]
except:
	columns = int(40)

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
	def __init__(self):
		pass

	def red(self, text=''):
		print(f'{CSRed}[!] {text}{CReset}')

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
			print('-' * columns)
		else:
			print(char * columns)

	# Strong
	def sred(text=''):
		print(f'{CSRed}{text}{CReset}')

	def sgreen(text=''):
		print(f'{CSGreen}{text}{CReset}')

	def syellow(text=''):
		print(f'{CSYellow}{text}{CReset}')

	def sblue(text=''):
		print(f'{CSBlue}{text}{CReset}')

	def swhite(text=''):
		print(f'{CSWhite}{text}{CReset}')

	# Dark
	def dred(text=''):
		print(f'{CDRed}{text}{CReset}')

	def dgreen(text=''):
		print(f'{CDGreen}{text}{CReset}')

	def dyellow(text=''):
		print(f'{CDYellow}{text}{CReset}')

	def dblue(text=''):
		print(f'{CDBlue}{text}{CReset}')

	def dwhite(text=''):
		print(f'{CDWhite}{text}{CReset}')




