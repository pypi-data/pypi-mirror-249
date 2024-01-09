# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cumulative', 'cumulative.transforms']

package_data = \
{'': ['*']}

install_requires = \
['ipywidgets>=7.1.1,<8.0.0',
 'matplotlib>=3.7.1,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'scikit-learn>=1.2.2,<2.0.0',
 'scipy>=1.11.4,<2.0.0',
 'statsmodels>=0.14.1,<0.15.0',
 'tqdm>=4.66.1,<5.0.0',
 'tsfel>=0.1.6,<0.2.0']

setup_kwargs = {
    'name': 'cumulative',
    'version': '0.0.18',
    'description': 'Manipulation and analysis of data series collections',
    'long_description': '# CUMULATIVE\n\nManipulation and analysis of data series collections.\n\n* **Documentation**: [https://elehcimd.github.io/cumulative/license/](https://elehcimd.github.io/cumulative/license/)\n* **Source code**: [https://github.com/elehcimd/cumulative](https://github.com/elehcimd/cumulative)\n\n## License\n\nThis project is licensed under the terms of the [BSD 3-Clause License](https://elehcimd.github.io/cumulative/license/).\n\n',
    'author': 'Michele Dallachiesa',
    'author_email': 'michele.dallachiesa@sigforge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://elehcimd.github.io/cumulative/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0',
}


setup(**setup_kwargs)
