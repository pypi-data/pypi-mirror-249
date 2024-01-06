from setuptools import setup, find_packages
from os.path import abspath
import subprocess, os, sys
from setuptools.command.install import install

setup(
    name='gai-cli',
    version="0.3",
    author="kakkoii1337",
    author_email="kakkoii1337@gmail.com",
    packages=find_packages(),
    description = """Gai/Cli is a command-line interpreter/interface built using Gai/Gen library providing fast and easy access language large models.""",
    classifiers=[
        'Programming Language :: Python :: 3.10',
        "Development Status :: 3 - Alpha",        
        'License :: OSI Approved :: MIT License',
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",        
        'Operating System :: OS Independent',
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",        
        "Topic :: Scientific/Engineering :: Artificial Intelligence",        
    ],
    python_requires='>=3.10',        
    install_requires=[
    ],
    extras_require={
    },
    entry_points={
        'console_scripts': [
            'ttt=gai.cli.ttt:main',
            'tts=gai.cli.tts:main',
            'chunker=gai.cli.chunker:main',
        ],
    }
)