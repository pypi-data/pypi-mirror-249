# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cumulative', 'cumulative.transforms']

package_data = \
{'': ['*']}

install_requires = \
['ipywidgets>=8.1.1,<9.0.0',
 'matplotlib>=3.8.2,<4.0.0',
 'pandas>=2.1.3,<3.0.0',
 'scikit-learn>=1.3.2,<2.0.0',
 'scipy>=1.11.4,<2.0.0',
 'statsmodels>=0.14.1,<0.15.0',
 'tqdm>=4.66.1,<5.0.0',
 'tsfel>=0.1.6,<0.2.0']

setup_kwargs = {
    'name': 'cumulative',
    'version': '0.0.16',
    'description': 'Manipulation and analysis of data series collections',
    'long_description': '# CUMULATIVE\n\nWork in progress, not yet ready for prime time.\n\n## License\n\nThis project is licensed under the terms of the [BSD 3-Clause License](LICENSE).\n\n',
    'author': 'Michele Dallachiesa',
    'author_email': 'michele.dallachiesa@sigforge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/elehcimd/cumulative',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0',
}


setup(**setup_kwargs)
