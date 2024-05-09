from setuptools import setup


import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")



setup(
    name='ts2vvg',
    version=get_version("ts2vvg/__init__.py"),
    description='Implementation of Vector Visibility Graph (VVG), an algorithm to convert multivariate time series into a graph',
    url='https://github.com/raffoliveira/ts2vvg',
    author='Rafael F. Oliveira',
    author_email='rafaelollywer@gmail.com',
    packages=['ts2vvg'],
    install_requires=[
        'networkx',
        'numpy'
    ]
)
