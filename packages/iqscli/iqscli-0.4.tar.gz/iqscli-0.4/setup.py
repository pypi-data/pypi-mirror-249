from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='iqscli',
    version='0.4',
    description='iqscli is an unofficial CLI for IBM Quantum Systems',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/metebalci/iqscli',
    author='Mete Balci',
    author_email='metebalci@gmail.com',
    license='GPLv3',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
    ],
    keywords='cli ibm quantum',
    py_modules=['iqscli'],
    install_requires=['qiskit', 'qiskit-ibm-runtime'],
    entry_points={
        'console_scripts': [
            'iqscli=iqscli:main',
        ],
    },
)
