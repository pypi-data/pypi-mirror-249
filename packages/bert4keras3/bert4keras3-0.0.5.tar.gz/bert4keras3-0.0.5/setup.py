# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 18:59:44 2023

@author: Administrator
"""
from distutils.core import setup
from setuptools import find_packages


with open("README.rst", "r",encoding='utf-8') as f:
  long_description = f.read()

setup(name='bert4keras3',  # 包名
      version='0.0.5',  # 版本号
      description='bert4keras for keras3',
      long_description=long_description,
      author='passlin',
      author_email='935499957@qq.com',
      url='https://github.com/pass-lin/bert4keras3',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries'
      ],
      )
