from setuptools import setup, find_packages

setup(
    name = "zums",
    version = "0.1",
    url = 'http://github.com/amitu/zums',
    license = 'BSD',
    description = file("README.rst").read(),
    author = 'Amit Upadhyay',
    packages = find_packages('ROOT'),
    package_dir = {'': 'ROOT'},
    install_requires = ['setuptools'],
)
