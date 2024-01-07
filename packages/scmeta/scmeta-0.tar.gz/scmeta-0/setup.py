# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['SCMeTA',
 'SCMeTA.accelerate',
 'SCMeTA.batch',
 'SCMeTA.config',
 'SCMeTA.core',
 'SCMeTA.file',
 'SCMeTA.file.plugin',
 'SCMeTA.match',
 'SCMeTA.method',
 'SCMeTA.method.fill',
 'SCMeTA.method.machine_learning',
 'SCMeTA.plot',
 'SCMeTA.plot.Bokeh',
 'SCMeTA.plot.Mpl',
 'SCMeTA.search']

package_data = \
{'': ['*'], 'SCMeTA.file.plugin': ['dll/*']}

install_requires = \
['combat>=0.3.3,<0.4.0',
 'matplotlib>=3.7.2,<4.0.0',
 'numpy>=1.25.2,<2.0.0',
 'pandas>=2.1.0,<3.0.0',
 'polars>=0.19.1,<0.20.0',
 'pyrawtools>=0.2.3,<0.3.0',
 'pythonnet>=3.0.3,<4.0.0',
 'scikit-learn>=1.3.0,<2.0.0',
 'scipy>=1.11.2,<2.0.0',
 'tqdm>=4.66.1,<5.0.0',
 'umap-learn>=0.5.4,<0.6.0']

setup_kwargs = {
    'name': 'scmeta',
    'version': '0',
    'description': 'A python package for single-cell metabolism analysis.',
    'long_description': '# SCMeTA\n\nSCMeTA is a python library of single-cell meta-analysis tools. It provides a set of functions for single-cell meta-analysis, including data integration, batch effect correction, cell type annotation, cell clustering, cell trajectory inference, and cell type marker identification. It also provides a set of functions for single-cell data visualization, including dimension reduction, cell clustering, cell trajectory inference, and cell type marker identification. \n\n## Installation\n\nSCMeTA is available on PyPI and can be installed with pip:\n\n```bash\npip install scmeta\n```\n\n## Usage\n\n### Data integration\n\n```python\n\nfrom SCMeTA import Process\n\nsc = Process()\n\n# Load data\n\nsc.load("data/example.RAW")\n\n# Data process\n\nsc.pre_process()\nsc.process()\nsc.post_process()\n\n```\n\n## Documentation\n\nThe official documentation is hosted on Read the Docs: https://sc-meta.com/\n\n## License\n\nSCMeTA is licensed under the GPLv3 license. See the LICENSE file for more details.\n\n\n',
    'author': 'EstrellaXD',
    'author_email': 'estrellaxd05@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.sc-meta.org/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.13',
}


setup(**setup_kwargs)
