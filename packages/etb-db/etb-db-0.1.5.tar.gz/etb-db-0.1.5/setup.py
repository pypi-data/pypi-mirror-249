# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['etb_db']

package_data = \
{'': ['*']}

install_requires = \
['mysql-connector-python>=8.2.0,<9.0.0',
 'psycopg2-binary>=2.9.9,<3.0.0',
 'sqlalchemy>=2.0.24,<3.0.0']

setup_kwargs = {
    'name': 'etb-db',
    'version': '0.1.5',
    'description': 'A very simple class for interacting with MySQL and PostgreSQL databases',
    'long_description': '',
    'author': 'Tate Button',
    'author_email': 'yg3bpwn0or679hau8fxi@duck.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HFxLhT8JqeU5BnUG/etb-db',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
