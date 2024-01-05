from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='sintxcs',
  version='0.0.1',
  description='Sintacs Collection of Made Modules',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Sintacs',
  author_email='sintacs@isnotdev.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Sintxcs', 
  packages=find_packages(),
  install_requires=[''] 
)
