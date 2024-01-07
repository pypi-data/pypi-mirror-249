from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='easiest_sort',
  version='0.0.2',
  author='Eliastikus',
  author_email='eliastikus@gmail.com',
  description='Python module for easiest and fast sort',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/eliastikus/Python',
  License='Apache License, Version 2.0, see LICENSE file ',
  packages=['easiest_sort'],
  classifiers=[
    'Programming Language :: Python :: 3.13',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent'
  ],
  keywords='easiest sort',
  project_urls={
    'GitHub': 'https://github.com/eliastikus'
  },
)