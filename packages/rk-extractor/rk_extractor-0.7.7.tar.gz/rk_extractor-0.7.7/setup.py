from setuptools import setup, find_packages

import os
import glob

#----------------------------------------------
def is_code(file_path):
    try:
        with open(file_path) as ifile:
            ifile.read()
    except:
        return False

    return True
#----------------------------------------------
def get_scripts(dir_path):
    l_obj = glob.glob(f'{dir_path}/*')
    l_scr = [ obj for obj in l_obj if is_code(obj)]

    return l_scr
#----------------------------------------------
def get_packages():
    l_pkg = find_packages(where='src') + ['']

    return l_pkg
#----------------------------------------------
setup(
        name              = 'rk_extractor',
        version           = '0.7.7',
        description       = 'Used to extract RK from simultaneous fits',
        scripts           = get_scripts('scripts/jobs') + get_scripts('scripts/offline'),
        long_description  = '',
        packages          = get_packages(), 
        package_dir       = {'' : 'src'},
        package_data      = {'extractor_data' : ['*/*/*.json']},
        install_requires  = open('requirements.txt').read().splitlines()
        )

