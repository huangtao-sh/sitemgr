#!/usr/bin/env python3
import os
import sys
from glob import glob
from setuptools import setup,find_packages
from distutils.sysconfig import get_python_lib
# Warn if we are installing over top of an existing installation. This can
# cause issues where files that were deleted from a more recent Django are
# still present in site-packages. See #18115.
WORK_PATH='/var/www/mysite'
CONFIG_PATH='/etc/mysite'
# Dynamically calculate the version based on django.VERSION.
packages=find_packages()
def find_package_data(packages):
    def get_files(init_dir):
        files=[]
        dirs=os.listdir(init_dir if init_dir else '.')
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
        if dirs:
            for d in dirs:
                a=os.path.join(init_dir,d)
                if os.path.isdir(a):
                    if not os.path.isfile(os.path.join(a,'__init__.py')):
                        files.extend(get_files(a))
                elif os.path.splitext(a)[1]!='.py':
                    files.append(a)
        return files

    package_data={}
    for package in packages:
        init=package.replace('.','/')
        datas=get_files(package.replace('.','/'))
        if datas:
            l=len(init)+1
            datas=[f[l:] for f in datas]
            package_data[package]=datas

    return package_data
version = '0.0.1'
setup(
    name='sitemgr',
    version=version,
    url='',
    author='huangtao',
    author_email='huangtao.jh@gmail.com',
    description=('My web site'),
    license='GPL',
    packages=packages,
    package_data=find_package_data(packages),
    include_package_data=True,
    scripts=['script/prdsite.py'],
    data_files=[
        (WORK_PATH,['script/wsgi.py']),
        (CONFIG_PATH,['conf/installed_apps']),
        (os.path.join(WORK_PATH,'static'),glob('static/*.*')),
        (os.path.join(WORK_PATH,'media'),glob('media/*.*')),
        ('/etc/apache2/sites-available/',['conf/mysite']),
        ]
)
