#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
import urllib.request


try:
    from tqdm import tqdm
except:
    print('Instale o módulo tqdm: pip3 install tqdm --user')
    sys.exit()


try:
    import wget
except:
    print('Instale o módulo wget: pip install wget --user')
    sys.exit()

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def run_download(url, output_path):
    if os.path.isfile(output_path) == True:
        print(f'Arquivo encontrado ... {output_path}')
        return
	
	
    with DownloadProgressBar(
    						unit='B', 
    						unit_scale=True,
							miniters=1, 
							desc=url.split('/')[-1]
							) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)
        
def wget_download(url, output_path):
    if os.path.isfile(output_path) == True:
        print(f'Arquivo encontrado ... {output_path}')
        return
    
    print(f'Baixando ... {output_path}')
    wget.download(url, output_path)
    print(' OK')




