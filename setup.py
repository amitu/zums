from setuptools import setup, find_packages

setup(
    name = "zums",
    version = "0.1.2",
    url = 'http://github.com/amitu/zums',
    license = 'BSD',
    description = "ZeroMQ based User and Session management for webapps in different languages/frameworks",
    long_description = file("README.rst").read(),
    author = 'Amit Upadhyay',
    author_email = "upadhyay@gmail.com",
    packages = find_packages('ROOT'),
    package_dir = {'': 'ROOT'},
    install_requires = ['setuptools'],
    entry_points={
      'console_scripts': ['zumsd = zums.zumsd:main']
    }
)
