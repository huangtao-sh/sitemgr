#!/usr/bin/env python3
import os
import sys
from glob import glob
from setuptools import setup,find_packages
from distutils.sysconfig import get_python_lib
# Warn if we are installing over top of an existing installation. This can
# cause issues where files that were deleted from a more recent Django are
# still present in site-packages. See #18115.

# Dynamically calculate the version based on django.VERSION.

version = '0.0.1'
setup(
    name='sitemgr',
    version=version,
    url='',
    author='huangtao',
    author_email='huangtao.jh@gmail.com',
    description=('My web site'),
    license='GPL',
    packages=find_packages(),
    include_package_data=True,
    scripts=['prdsite.py','devsite.py'],
    data_files=[
        ('/var/www/mysite/',['sitemgr/wsgi.py']),
        ('/etc/mysite/',['conf/installed_apps']),
        ('/var/www/mysite/static',glob('static/*.*')),
        ('/var/www/mysite/templates',glob('templates/*.*')),
        ('/etc/apache2/sites-available/',['conf/mysite']),
        ]
)
