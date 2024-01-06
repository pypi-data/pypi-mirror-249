# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asynctradier',
 'asynctradier.common',
 'asynctradier.exceptions',
 'asynctradier.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.9.1,<4.0.0', 'strenum>=0.4.15,<0.5.0']

setup_kwargs = {
    'name': 'asynctradier',
    'version': '0.0.1b6',
    'description': '',
    'long_description': '# WIP\n',
    'author': 'Jiakuan Li',
    'author_email': 'jiakuan.li.cs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
