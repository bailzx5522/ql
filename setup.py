import os
from setuptools import setup

setup(
    name = "ql",
    version = "1.0.0",
    author = "BLZ",
    description = ("FTD"),
    license = "BSD",
    #url = "http://packages.python.org/an_example_pypi_project",
    #42.62.41.17:qltest123!@#
    install_requires=[
        'sqlalchemy', 'MySQL-python',
    ],
    packages=['ql', 'ql/common', 'ql/db', 'ql/claw', 'ql/strategy']
)
