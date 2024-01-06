from setuptools import setup, find_packages
import os

def getRequirements():
    with open('requirements.txt', 'r') as f:
        requirements = f.read().splitlines()
    return requirements

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='sarapy',
    version='0.1.1',
    packages=find_packages(),
    install_requires=getRequirements(),
    author='Lucas Baldezzari',
    author_email='lmbaldezzari@gmail.com',
    description='Library for Sarapico Metadata processing',
    long_description=readme(),
    url='https://github.com/lucasbaldezzari/sarapy',
    license='MIT', ##revisar licencia
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Operating System :: Unix',
    ],
)