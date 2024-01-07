# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jobapppy']

package_data = \
{'': ['*'], 'jobapppy': ['templates/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'pydantic[email]>=2.5.3,<3.0.0',
 'pyyaml>=6.0.1,<7.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['jobapppy = jobapppy.cli:cli']}

setup_kwargs = {
    'name': 'jobapppy',
    'version': '0.0.2',
    'description': 'Command-line tools and interfaces to generate formatted resume documents (markdown, tex, pdf, etc)',
    'long_description': '# jobapppy\n\n[![PyPI version](https://badge.fury.io/py/jobapppy.svg)](https://badge.fury.io/py/jobapppy)[![Python Versions](https://img.shields.io/pypi/pyversions/jobapppy?style=plastic)](https://pypi.org/project/jobapppy)\n[![Main](https://github.com/cahna/jobapppy/actions/workflows/main.yaml/badge.svg)](https://github.com/cahna/jobapppy/actions/workflows/main.yaml)[![codecov](https://codecov.io/gh/cahna/jobapppy/graph/badge.svg?token=3XULKTDJ2I)](https://codecov.io/gh/cahna/jobapppy)\n\nCommand-line tools and interfaces to generate formatted resume documents (markdown, tex, pdf, etc).\n\nDocumentation: [https://cahna.github.io/jobapppy](https://cahna.github.io/jobapppy)\n\n## CLI Usage\n\n- via script name installed in path:\n   ```console\n   jobapppy --help\n   ```\n- as a python module:\n   ```console\n   python -m jobapppy --help\n   ```\n\n## Tutorial\n\n1. Create a `resume.yaml` file that satisfies jobapppy\'s schema \n   - see `resume.example.yaml`\n   - view the JSONSchema by running:\n      ```console\n      jobapppy schema -i2\n      ```\n2. (optional) Check that `resume.yaml` can be parsed:\n   ```console\n   jobapppy parse -c resume.yaml\n   ```\n3. Generate resume from templates:\n   - Markdown (default, `-t md`)\n      - Echo to stdout (default):\n         ```console\n         jobapppy template resume.yaml\n         ```\n      - Echo to file:\n         ```console\n         jobapppy template resume.yaml resume.md\n         ```\n   - Tex (`-t tex`)\n      1. Generate `resume.tex`:\n         ```console\n         jobapppy template -t tex resume.yaml resume.tex\n         ```\n      2. Generate `resume.pdf`:\n         ```console\n         docker run --rm -it -v "$(pwd):/data" --net=none --user="$(id -u):$(id -g)" cahna/jobapp lualatex -synctex=1 -interaction=nonstopmode resume.tex\n         ```\n',
    'author': 'Conor Heine',
    'author_email': 'conor.heine+jobapppy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://cahna.github.io/jobapppy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
