#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
import urllib.request
import platform
import lib.wget as wget


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

            # Espaço total da janela do terminal menos o total de caracteres da variavel 'show_progress_msg'.
            num_space_widh = int(self.terminal_widh - len(show_progress_msg))  

            # Dividir o numero inteiro da variavel 'num_space_widh' em 100 partes inteiras iguais que serão 
            # preenchidas com '=>(percentual%)'. 
            num_space_line = int(num_space_widh // 100) 

            # Linha de progresso será exibida proporcionalmento ao percentual de download.
            progress_line = (num_space_line * progress)

            # Espaço livre que será preenchido pela barra de progresso conforme o progresso do download.
            null_line = (num_space_widh - progress_line - (num_space_widh % 100) -1)

            # Progresso será exibido da seguinte forma '[=>(percentual%)--------]'
            show_line = f'{("=" * progress_line)}>({progress}%){("-" * null_line)}'

            # Exibição formatada na tela do terminal.
            show_download_progress = '[{}] | {} |'.format(show_line, show_progress_msg) 

            if len(show_download_progress) < num_space_widh:
                print(f'\033[KAguarde...', end='\r')
            else:
                print(f'\033[K{show_download_progress}', end='\r')
        else:
            print(f'\033[KAguarde...', end='\r')
            

    def wget_download(self):
        if os.path.isfile(self.output_path):
            print(f'Arquivo encontrado ... {self.output_path}')
            return True

        print(f'Destino ... {self.output_path}')
        wget.download(self.url, self.output_path, bar=self.bar_custom)
        print('')

    def curl_download(self):
        '''
        Realizar downloads com a ferramenta 'curl'.
        '''
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




