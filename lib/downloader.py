#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
import urllib.request
import platform
import lib.wget as wget

'''
try:
    import wget
except Exception as err:
    print(err)
    print('Instale o módulo wget: pip3 install wget --user')
    sys.exit()
'''

class Downloader:
    def __init__(self, url, output_path):
        self.url = url
        self.output_path = output_path
        self.terminal_widh = os.get_terminal_size()[0]

    def bar_custom(self, current, total, width=80):
        # print('\033[K[>] Progresso: %d%% [%d / %d]MB ' % (progress, current, total), end='\r')
        if total > 1048576: # Converter bytes para MB
            current = current / 1048576
            total = total / 1048576
            und = 'MB'
        else:
            und = 'K'

        progress = (current / total) * 100 # Percentual
        if (current) and (progress > 0):
            current = '{:.2f}'.format(current)
            total = '{:.2f}'.format(total)
            progress = int(progress)
            show_progress_msg = '{}/{}{}'.format(current, total, und)
           
            num_space_widh = int(self.terminal_widh - len(show_progress_msg)) # Espaço livre disponível. 
            num_space_line = int(num_space_widh // 100) # Dividir o espaço livre em 100 partes inteiras iguais. 
            progress_line = (num_space_line * progress)
            null_line = (num_space_widh - progress_line - (num_space_widh % 100) -1)
            show_line = f'{("=" * progress_line)}>({progress}%){("-" * null_line)}'
            show_download_progress = '[{}] | {} |'.format(show_line, show_progress_msg)

            print(f'\033[K{show_download_progress}', end='\r')
        else:
            print(f'\033[KAguarde...', end='\r')
            

    def bar_custom_old(self, current, total, width=80):
        # print('\033[K[>] Progresso: %d%% [%d / %d]MB ' % (progress, current, total), end='\r')
        
        if current > 1048576: # Converter bytes para MB
            current = current / 1048576
            total = total / 1048576

        progress = (current / total) * 100 # Percentual
        
        current = '{:.2f}'.format(current)
        total = '{:.2f}'.format(total)
        progress = '{:.1f}'.format(progress)
        
        print(f'\033[KProgresso ... [{progress}%] [{current}/{total}]MB', end='\r')

    def wget_download(self):
        if os.path.isfile(self.output_path):
            print(f'Arquivo encontrado ... {self.output_path}')
            return True

        print(f'Destino ... {self.output_path}')
        wget.download(self.url, self.output_path, bar=self.bar_custom)
        print('')

    def curl_download(self):
        print(f'Destino ... {self.output_path}')
        if (platform.system() != 'Windows'):
            os.system(f'curl -S -L {self.url} -o {self.output_path}')
        else:
            os.system(f'curl.exe -S -L {self.url} -o {self.output_path}')
  
           
def run_download(url, output_path):
    # info = urllib.request.urlopen(url)
    # length = int(info.getheader('content-length'))
    # if length and (length != None):
    
    if os.path.isfile(output_path) == True:
        print(f'Arquivo encontrado ... {output_path}')
        return
    
    print(f'Conectando ... {url}')
    info = urllib.request.urlopen(url)
    length = info.getheader('content-length')
    if length:
        Downloader(url, output_path).wget_download()
    else:
        Downloader(url, output_path).curl_download()




