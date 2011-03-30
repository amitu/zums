try:
        from ez_setup import use_setuptools
except ImportError:
        pass
else:
        use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "zums",
    version = "0.1.4",
    url = 'http://packages.python.org/zums/',
    license = 'BSD',
    description = "ZeroMQ based User and Session management for webapps in different languages/frameworks",
    author = 'Amit Upadhyay',
    author_email = "upadhyay@gmail.com",
    packages = find_packages('ROOT'),
    package_dir = {'': 'ROOT'},
    install_requires = ['setuptools', "fhurl", "argparse"],
    entry_points={
        'console_scripts': [
            'zumsd = zums.zumsd:main', "zums_httpd =  zums.zumsd_users.serve:main"
        ]
    },
)
