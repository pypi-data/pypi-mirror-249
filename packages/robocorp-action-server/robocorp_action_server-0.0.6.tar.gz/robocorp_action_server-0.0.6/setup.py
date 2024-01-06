# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['robocorp',
 'robocorp.action_server',
 'robocorp.action_server._preload_actions',
 'robocorp.action_server._robo_utils',
 'robocorp.action_server.migrations']

package_data = \
{'': ['*'], 'robocorp.action_server': ['bin/*']}

install_requires = \
['PyYAML>=6,<7',
 'fastapi>=0.104.1,<0.105.0',
 'jsonschema>=4.19.2,<5.0.0',
 'psutil>=5,<6',
 'pydantic>=2.4.2,<3.0.0',
 'requests>=2,<3',
 'robocorp-actions>=0.0.3,<0.0.4',
 'uvicorn>=0.23.2,<0.24.0',
 'websockets>=12.0,<13.0']

entry_points = \
{'console_scripts': ['action-server = robocorp.action_server.cli:main']}

setup_kwargs = {
    'name': 'robocorp-action-server',
    'version': '0.0.6',
    'description': 'Robocorp local task server',
    'long_description': 'docs/README.md',
    'author': 'Fabio Zadrozny',
    'author_email': 'fabiofz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/robocorp/robo/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
