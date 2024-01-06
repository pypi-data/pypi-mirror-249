# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chrono_python',
 'chrono_python.common',
 'chrono_python.common.parsers',
 'chrono_python.locales',
 'chrono_python.locales.en',
 'chrono_python.locales.en.parsers',
 'chrono_python.locales.en.refiners',
 'chrono_python.locales.ja']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chrono-python',
    'version': '2.0.0.dev0',
    'description': 'A natural language date parser.',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
