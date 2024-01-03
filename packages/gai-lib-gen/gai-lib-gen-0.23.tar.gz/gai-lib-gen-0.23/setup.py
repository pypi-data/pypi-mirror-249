VERSION='0.23'
from setuptools import setup, find_packages
from os.path import abspath
import subprocess, os, sys
from setuptools.command.install import install

with open("README.md", "r", encoding="utf-8") as readme_file:
    README = readme_file.read()

def parse_requirements(filename):
    with open(filename) as f:
        required = f.read().splitlines()
    return required

setup(
    name='gai-lib-gen',
    version=VERSION,
    author="kakkoii1337",
    author_email="kakkoii1337@gmail.com",
    packages=find_packages(exclude=["tests*","gai.gen.api"]),
    description = """Gai/Gen is the Universal Multi-Modal Wrapper Library for LLM. The library is designed to provide a simplified and unified interface for seamless switching between multi-modal open source language models on a local machine and OpenAI APIs.""",
    long_description=README,
    long_description_content_type="text/markdown",
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
        "TTT": parse_requirements("requirements_ttt.txt"),
        "ITT": parse_requirements("requirements_itt.txt"),
        'STT': parse_requirements("requirements_stt.txt"),
        'TTS': parse_requirements("requirements_tts.txt")          
    },
)