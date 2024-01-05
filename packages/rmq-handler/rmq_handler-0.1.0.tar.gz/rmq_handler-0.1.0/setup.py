# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rmq_handler', 'rmq_handler.configuration', 'rmq_handler.handlers']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=9.3.1,<10.0.0']

setup_kwargs = {
    'name': 'rmq-handler',
    'version': '0.1.0',
    'description': 'RabbitMQ connections handler.',
    'long_description': '',
    'author': 'Kirill',
    'author_email': 'pnchkirill@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
