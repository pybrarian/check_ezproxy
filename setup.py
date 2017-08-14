# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*\'(.*)\'',
    open('check_ezproxy/check_ezproxy.py').read(),
    re.M
    ).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name="check_ezproxy",
    packages=["check_ezproxy"],
    entry_points={
        "console_scripts": ['check_ezproxy = check_ezproxy.check_ezproxy:main']
        },
    version=version,
    description="Command line tool to test EZProxy stanza configurations and link health.",
    long_description=long_descr,
    license='MIT',
    author="Ed Hill",
    author_email="hill.charles2@gmail.com",
    url="https://github.com/chill17/check_ezproxy/",
    install_requires=['requests', 'pykbart', 'gevent'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

)
