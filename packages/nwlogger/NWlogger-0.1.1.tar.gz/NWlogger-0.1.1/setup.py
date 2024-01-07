import os

from setuptools import find_packages, setup


setup(
    name="NWlogger",
    packages=['coevalogger', 'coevalogger.utils'],
    version="0.1.1",
    description="NeuroWave Logger",
    author="NeuroWave",
    author_email='info@neurowave.ai',
    url="https://github.com/NeurowaveAI/coeval_logger/tree/0.1.0",
    download_url = 'https://github.com/NeurowaveAI/coeval_logger/archive/refs/tags/0.1.0.tar.gz',
    license='(c) NeuroWave License',
    classifiers = ['License :: Other/Proprietary License']
    
)
