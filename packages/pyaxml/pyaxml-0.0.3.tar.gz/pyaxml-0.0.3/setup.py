#!/usr/bin/env python
 
from setuptools_protobuf import Protobuf
from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess


name="pyaxml"

setup(
    name=name,
    version='0.0.3',
    packages=[name, "pyaxml/proto"],
    author="MadSquirrel",
    author_email="benoit.forgette@ci-yow.com",
    description="Manipulate AXML file and create one from scratch",
    package_data={"pyaxml/proto" : ["*.proto"]},
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    download_url=f"https://gitlab.com/MadSquirrels/mobile/{name}",
    include_package_data=True,
    url='https://ci-yow.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 1 - Planning"
    ],
 
    entry_points = {
    },
    cmdclass={
    },
    
    protobufs=[Protobuf('pyaxml/proto/axml.proto')],
    setup_requires=['setuptools-protobuf'],
    install_requires = [
        'androguard',
        'click',
    ],
    python_requires='>=3.5'
 
)
