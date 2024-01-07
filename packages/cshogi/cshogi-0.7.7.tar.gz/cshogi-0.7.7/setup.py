# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cshogi',
 'cshogi.dlshogi',
 'cshogi.gym_shogi',
 'cshogi.gym_shogi.envs',
 'cshogi.usi',
 'cshogi.web']

package_data = \
{'': ['*'], 'cshogi.web': ['static/*', 'templates/*']}

extras_require = \
{':python_version == "3.6"': ['numpy>=1.19.5,<1.20.0'],
 ':python_version == "3.7"': ['numpy>=1.21.6,<1.22.0'],
 ':python_version >= "3.12" and python_version < "4.0"': ['numpy>=1.26.0,<1.27.0'],
 ':python_version >= "3.8" and python_version < "3.12"': ['numpy']}

setup_kwargs = {
    'name': 'cshogi',
    'version': '0.7.7',
    'description': 'A fast Python shogi library',
    'long_description': 'None',
    'author': 'Tadao Yamaoka',
    'author_email': 'tadaoyamaoka@gmail.com',
    'maintainer': 'Tadao Yamaoka',
    'maintainer_email': 'tadaoyamaoka@gmail.com',
    'url': 'https://github.com/TadaoYamaoka/cshogi',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
