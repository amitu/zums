from setuptools import setup, find_packages

setup(
    name = "zums",
    version = "0.1.3",
    url = 'http://github.com/amitu/zums',
    license = 'BSD',
    description = "ZeroMQ based User and Session management for webapps in different languages/frameworks",
    author = 'Amit Upadhyay',
    author_email = "upadhyay@gmail.com",
    packages = find_packages('ROOT'),
    package_dir = {'': 'ROOT'},
    install_requires = ['setuptools', "fhurl", "msgpack-python", "argparse"],
    entry_points={
        'console_scripts': [
            'zumsd = zums.zumsd:main', "zums_httpd =  zums.zumsd_users.serve:main"
        ]
    },
)
