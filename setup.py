import os
from setuptools import setup

setup(
    name = "ql",
    version = "1.0.0",
    author = "BLZ",
    description = ("FTD"),
    license = "BSD",
    #url = "http://packages.python.org/an_example_pypi_project",
    packages=['ql', 'ql/common', 'ql/db', 'ql/claw']
)
