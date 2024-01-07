# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['detadoc']

package_data = \
{'': ['*']}

install_requires = \
['bcrypt>=4.1.1,<5.0.0',
 'email-validator>=2.1.0,<3.0.0',
 'hx-markup>=0.2.2,<0.3.0',
 'ormspace>=0.2.3,<0.3.0',
 'spacestar>=0.1.6,<0.2.0']

setup_kwargs = {
    'name': 'detadoc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Arantes',
    'author_email': 'arantesdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
