from setuptools import setup, find_packages
from src.pyuvvm import __version__, __author__, __email__


with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pyuvvm',
    description='A Pyton implementation of UVVM for Cocotb',
    long_description=long_description,
    author=__author__,
    author_email=__email__,
    version=__version__,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={
        'pyuvvm.resources': ['*'],
    },
    include_package_data=True,
    install_requires=[
        'importlib-resources;python_version<"3.8"',
        'cocotb',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
