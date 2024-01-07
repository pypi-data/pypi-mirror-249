# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['killjoy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'killjoy',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Ivan Dmitrievsky',
    'author_email': 'ivan.dmitrievsky@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
