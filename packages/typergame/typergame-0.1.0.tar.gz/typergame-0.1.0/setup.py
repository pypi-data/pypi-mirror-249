from setuptools import setup, find_packages

setup(
    name = 'typergame',
    packages = find_packages(),
    version = '0.1.0',
    description = 'A library to easily set up typergames.',
    author = 'Drooler',
    install_requires = ["os", "sys", "time"]
)