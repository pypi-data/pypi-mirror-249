# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alfred_osint',
 'alfred_osint.alfred',
 'alfred_osint.lang',
 'alfred_osint.modules']

package_data = \
{'alfred_osint': ['captured/*', 'config/*', 'proxys/*', 'sites/*']}

install_requires = \
['alive-progress>=3.1.5,<4.0.0',
 'bs4>=0.0.1,<0.0.2',
 'colorama>=0.4.6,<0.5.0',
 'cryptography>=41.0.7,<42.0.0',
 'requests>=2.31.0,<3.0.0',
 'rich>=13.7.0,<14.0.0',
 'selenium>=4.16.0,<5.0.0',
 'torrequest>=0.1.0,<0.2.0',
 'tqdm>=4.66.1,<5.0.0',
 'wget>=3.2,<4.0']

entry_points = \
{'console_scripts': ['alfred-osint = alfred_osint.brib:main']}

setup_kwargs = {
    'name': 'alfred-osint',
    'version': '0.2.3.7',
    'description': 'Alfred is a advanced OSINT information gathering tool',
    'long_description': '# alfred-osint\nAlfred is a advanced OSINT information gathering tool.\n',
    'author': 'EliteGreyIT67',
    'author_email': 'elitegreyit@gmail.com',
    'maintainer': 'EliteGreyIT67',
    'maintainer_email': 'elitegreyit@gmail.com',
    'url': 'https://github.com/EliteGreyIT67/alfred-osint',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
