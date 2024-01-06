# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rozetka',
 'rozetka.entities',
 'rozetka.examples',
 'rozetka.runners',
 'rozetka.tools']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp-retry',
 'curl-cffi>=0.5.10',
 'global-logger',
 'influxdb-client[async]',
 'knockknock',
 'pathlib',
 'pendulum>=3.0.0',
 'pip',
 'progress',
 'python-worker',
 'ratelimit',
 'requests']

setup_kwargs = {
    'name': 'rozetka-api',
    'version': '1.4.0',
    'description': 'Rozetka Python API',
    'long_description': 'Rozetka.ua Python API\n---------------------\n\nExamples\n^^^^^^^^\n\nrozetka/examples/example_item.py\n\nrozetka/examples/example_category.py\n\nGithub\n^^^^^^^^\nhttps://github.com/ALERTua/rozetka_api\n\nPyPi\n^^^^^^^^\nhttps://pypi.org/project/rozetka-api/\n',
    'author': 'Alexey ALERT Rubasheff',
    'author_email': 'alexey.rubasheff@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ALERTua/rozetka_api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11.6,<3.12',
}


setup(**setup_kwargs)
