from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='sintx',
  version='0.1.4',
  description='Sintacs Modules',
  long_description=open('README.md').read(),
long_description_content_type="text/markdown",
  url='https://facebook.com/sintxcs',  
  author='Sintacs.',
  author_email='sintacs@isnotdev.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Sintxcs, Sintacs, Sintx', 
  packages=find_packages(),
  install_requires=[''] 
)
