#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#

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

class SetColor:
	def __init__(self):
		self.reset = CReset
		self.red = CRed
		self.green = CGreen
		self.yellow = CYellow
		self.blue = CBlue
		self.white = CWhite

	def red(self):
		print(self.red, end='')

	def green(self):
		print(self.green, end='')

	def yellow(self):
		print(self.yellow, end='')

	def blue(self):
		print(self.blue, end='')

	def white(self):
		print(self.white, end='')

	def reset(self):
		print(self.reset, end='')



class PrintText:

	def red(text=''):
		print(f'[{CRed}!{CReset}] {text}')

	def green(text=''):
		print(f'[{CGreen}*{CReset}] {text}')

	def yellow(text=''):
		print(f'[{CYellow}+{CReset}] {text}')

	def blue(text=''):
		print(f'{CBlue}[*]{CReset} {text}')

	def white(text=''):
		print(f'{CWhite}[>]{CReset} {text}')


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


	def msg(text=''):
		line = ('-' * 45)
		print(line)
		print(text)
		print(line)

	def inline(text=''):
		print(f'\033[K{text}', end='\r')




