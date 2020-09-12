#!/usr/bin/env python3
'''
https://www.programcreek.com/python/example/82300/gnupg.GPG
'''

import os
import platform
from pathlib import Path
#import gnupg
import gpg

if platform.system() == 'FreeBSD':
    DirHome = os.path.abspath(os.path.join('/usr', Path.home()))
else:
    DirHome = os.path.abspath(os.path.join(Path.home()))

DirGpg = os.path.abspath(os.path.join(DirHome, '.gnupg'))

def gpg_import(key_file, url_key=None):
    '''
    https://docs.red-dove.com/python-gnupg/#importing-and-receiving-keys
    https://gist.github.com/ryantuck/56c5aaa8f9124422ac964629f4c8deb0
    https://www.programcreek.com/python/example/82300/gnupg.GPG

    pip3 install python-gnupg --user
    '''
    if url_key != None:
        print(f'Baixando ... {url_key}', end=' ')
        try:
            urllib.request.urlretrieve(url_key, key_file)
        except Exception as err:
            print('\n', err)
            return False
        else:
            print('OK')

    with open(key_file) as f:
        key_data = f.read()

    print(f'Importando ... {key_file}')  
    gpg = gnupg.GPG(gnupghome=DirGpg)  
    import_result = gpg.import_keys(key_data)
    for k in import_result.results:
        print(k)

def gpg_verify(path_file, path_to_signature_file):
    '''
    https://www.programcreek.com/python/example/82300/gnupg.GPG
    '''
    with gpg.Context() as c:
        c.set_engine_info(gpg.constants.protocol.OpenPGP, home_dir=DirGpg)

        sig = gpg.Data(file=path_to_signature_file)
        signed = gpg.Data(file=path_file)

        try:
            c.verify(signature=sig, signed_data=signed)
        except gpg.errors.BadSignatures as e:
            print(e)
        else:
            print(' OK')

def gpg_list():
    import gpg
    
    c = gpg.Context()
    for key in c.keylist():
        user = key.uids[0]
        print("Keys for %s (%s):" % (user.name, user.email))
        for subkey in key.subkeys:
            features = []
            if subkey.can_authenticate:
                features.append('auth')
            if subkey.can_certify:
                features.append('cert')
            if subkey.can_encrypt:
                features.append('encrypt')
            if subkey.can_sign:
                features.append('sign')
                print(' %s %s' %(subkey.fpr, ','.join(features)))