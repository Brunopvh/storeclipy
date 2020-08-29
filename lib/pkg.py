#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
import subprocess
from time import sleep

columns = os.get_terminal_size()[0]
line = ('-' * columns)

class ProcessLoop:
    def __init__(self, pid=''):
        self.pid = pid
        self.chars = ('-', '\\', '|', '/')
        self.process_list = []

    def get_process_list(self):
        '''
        Obter uma lista com todos os processos em execução no sistema
        essa lista sera inserida na variável self.process_list
        '''
        self.process_list = [] 
        all_process = subprocess.getstatusoutput('ps aux')[1].split('\n')
        for i in all_process:
            self.process_list.append(i) 

        return self.process_list

    def process_loop(self):
        PROCESS = self.get_process_list()
        for proc in PROCESS:
            proc = proc.split()
            if self.pid in proc[1]:
                is_pid = 'True'
                break
            else:
                is_pid = 'False'

        if is_pid == 'False':
            print(f'O processo com PID ({self.pid}) não está em execução.')
            sleep(0.15)
            return

        num = int('0')
        while True:
            PROCESS = self.get_process_list()
            for proc in PROCESS:
                proc = proc.split()
                if self.pid in proc[1]:
                    is_pid = 'True'
                    break
                else:
                    is_pid = 'False'

            if is_pid == 'False':
                print(f'Aguardando processo com pid ({self.pid}) \033[0;33mfinalizado\033[m [{self.chars[num]}]')
                sleep(0.1)
                break
                return
            else:
                print(f'\033[KAguardando processo com pid ({self.pid}) finalizar [{self.chars[num]}]', end='\r')
                sleep(0.15)

            if num == int('3'):
                num = int('-1')
            num += 1
            

class Pkg:

    def __init__(self):
        pass
            
    def pkg_is_list(self, pkgs):
        '''
        Verificar se os pacotes foram passados para classe em forma de lista
        ESTA FUNÇÃO NÃO ESTÁ SENDO USADA.
        '''
        if isinstance(pkgs, list): 
            return 'True'
        else:
            print('\033[0;31mFalha o(s) pacotes para instalação precisam ser passados em forma de uma lista.\033[m') 
            print(__class__)
            return 'False'
    
    def pkg_process_loop(self):
        all_procs = ' '
        
        while True:
            all_procs = ProcessLoop().get_process_list()
            for P in all_procs:
                if ('pkg install' in P) or ('pkg update' in P) or ('pkg delete' in P):
                    pid_pkg = P.split()[1] # Converter a linha de saída em lista e retornar o segundo item.
                    sleep(0.1)
                    break
                else:
                    pid_pkg = None

            if pid_pkg == None:
                break
            else:               
                ProcessLoop(pid_pkg).process_loop()
                
    def install(self, pkgs):
        self.pkg_process_loop() # Verificar se existe outro processo 'pkg' em execução no sistema.

        print(line)
        print(f'Instalando: {pkgs}')            
        print(line)
        os.system(f'sudo pkg install {pkgs}')

    def update(self):
        print(line)
        self.pkg_process_loop()
        print('Executando: sudo pkg update')
        os.system('sudo pkg update')

if __name__ == '__main__':
    AptGet().install(sys.argv[1:])
    


   
        

