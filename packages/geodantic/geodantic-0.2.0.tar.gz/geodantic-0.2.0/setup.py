# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geodantic']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=2.5.3']

setup_kwargs = {
    'name': 'geodantic',
    'version': '0.2.0',
    'description': 'GeoJSON parsing and validation using Pydantic',
    'long_description': '# geodantic',
    'author': 'Alexander Malyga',
    'author_email': 'alexander@malyga.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/alexandermalyga/geodantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.12,<4.0',
}


setup(**setup_kwargs)
