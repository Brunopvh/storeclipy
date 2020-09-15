#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
import urllib.request
import platform
import lib.wget as wget

class Downloader:
    def __init__(self, output_dir=os.getcwd()):
        try:
            self.terminal_widh = os.get_terminal_size()[0]
        except:
            self.terminal_widh = None
        self.output_dir = output_dir

    def bar_custom(self, current, total, width=80):
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

            # Espaço total da janela do terminal menos o total de caracteres da variável 'show_progress_msg'.
            num_space_widh = int(self.terminal_widh - len(show_progress_msg))  

            # Dividir o numero inteiro da variavel 'num_space_widh' em 100 partes inteiras iguais que serão 
            # preenchidas com '=>(percentual%)'. 
            num_space_line = int(num_space_widh // 100) 

            # Espaço vazio, diferença entre o tamanho total livre menos os espaços ocupados pela linha
            # de progresso e as infomações na variável 'show_progress_msg'.
            space = num_space_widh - (100 * num_space_line) - 1

            # Linha de progresso será exibida proporcionalmento ao percentual de download.
            progress_line = (num_space_line * progress)

            # Espaço livre que será preenchido pela barra de progresso conforme o progresso do download.
            null_line = (num_space_widh - progress_line - (num_space_widh % 100) -1)

            # Linha de progresso será exibido da seguinte forma '[=>(percentual%)--------]'
            show_line = f'{("=" * progress_line)}>({progress}%){("-" * null_line)}'

            # Exibição formatada na tela do terminal.
            show_download_progress = '[{}] | {} |'.format(show_line, show_progress_msg) 

            if len(show_download_progress) < num_space_widh:
                print(f'\033[KAguarde...', end='\r')
            else:
                print(f'\033[K{show_download_progress}', end='\r')
        else:
            print(f'\033[KAguarde...', end='\r')
            
    def wget_download(self, url, output_path):
        if os.path.isfile(output_path):
            print(f'Arquivo encontrado ... {output_path}')
            return True

        os.chdir(self.output_dir)
        print(f'Conectando ... {url}')
        #info = urllib.request.urlopen(url)
        #length = info.getheader('content-length')
        print(f'Destino ... {output_path}')
        wget.download(url, output_path)
        print('')
        
    def curl_download(self, url, output_path):
        if os.path.isfile(output_path):
            print(f'Arquivo encontrado ... {output_path}')
            return True

        os.chdir(self.output_dir)
        print(f'Conectando ... {url}')
        os.system(f'curl -S -L {url} -o {output_path}')
        





