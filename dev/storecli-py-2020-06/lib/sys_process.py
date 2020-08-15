#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

from subprocess import getstatusoutput
from time import sleep

class ShowProcessLoop:
    def __init__(self, process_name):
        self.process_name = process_name
        self.process_list = []

    def get_process_list(self):
        self.process_list = [] # Limpar a variável para.
        all_process = getstatusoutput('ps aux')[1].split('\n')
        for i in all_process:
            if self.process_name in i:
                self.process_list.append(i) 

        return self.process_list

    def show_loop(self, pid):
        # print(f'\033[K[>] Aguardando processo com pid ({pid}) finalizar [|]', end='\r')
        chars = ('-', '\\', '|', '/')

        for c in chars:
            print(f'\033[K[>] Aguardando processo com pid ({pid}) finalizar [{c}]', end='\r')
            sleep(0.25)
  

    def apt_process_loop(self):
        if int(len(self.get_process_list())) == int('0'):
            return
        
        while True:
            apt_procs = self.get_process_list()
            Pid_Apt = apt_procs[0].split()[1]
            Name_Apt = apt_procs[0].split()[10]
            self.show_loop(Pid_Apt)
            if int(len(self.get_process_list())) == int('0'):
                print(f'[>] Aguardando processo com pid ({Pid_Apt}) \033[0;33mfinalizado\033[m [-]')
                sleep(0.1)
                break
                return
            apt_procs = ''
            
            




   
        

