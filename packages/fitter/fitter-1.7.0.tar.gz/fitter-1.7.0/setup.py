# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fitter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.6,<9.0.0',
 'joblib>=1.3.1,<2.0.0',
 'loguru>=0.7.2,<0.8.0',
 'matplotlib>=3.7.2,<4.0.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=0.23.4,<3.0.0',
 'rich-click>=1.7.2,<2.0.0',
 'scipy>=0.18.0,<2.0.0',
 'tqdm>=4.65.1,<5.0.0']

entry_points = \
{'console_scripts': ['fitter = fitter.main:main']}

setup_kwargs = {
    'name': 'fitter',
    'version': '1.7.0',
    'description': 'A tool to fit data to many distributions and get the best one(s)',
    'long_description': '\n\n#############################\nFITTER documentation\n#############################\n\n.. image:: https://badge.fury.io/py/fitter.svg\n    :target: https://pypi.python.org/pypi/fitter\n\n.. image:: https://github.com/cokelaer/fitter/actions/workflows/main.yml/badge.svg?branch=main\n    :target: https://github.com/cokelaer/fitter/actions/workflows/main.yml\n\n.. image:: https://coveralls.io/repos/cokelaer/fitter/badge.png?branch=main\n    :target: https://coveralls.io/r/cokelaer/fitter?branch=main\n\n.. image:: http://readthedocs.org/projects/fitter/badge/?version=latest\n    :target: http://fitter.readthedocs.org/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://zenodo.org/badge/23078551.svg\n   :target: https://zenodo.org/badge/latestdoi/23078551\n\nCompatible with Python 3.7, and 3.8, 3.9\n\n\nWhat is it ?\n################\n\nThe **fitter** package is a Python library used for fitting probability distributions to data. It provides a straightforward and and intuitive interface to estimate parameters for various types of distributions, both continuous and discrete. Using **fitter**, you can easily fit a range of distributions to your data and compare their fit, aiding in the selection of the most suitable distribution. The package is designed to be user-friendly and requires minimal setup, making it a useful tool for data scientists and statisticians working with probability distributions.\n\nInstallation\n###################\n\n::\n\n    pip install fitter\n\n**fitter** is also available on **conda** (bioconda channel)::\n\n     conda install fitter\n\n\nUsage\n##################\n\nstandalone\n===========\n\nA standalone application (very simple) is also provided and works with input CSV\nfiles::\n\n    fitter fitdist data.csv --column-number 1 --distributions gamma,normal\n\nIt creates a file called fitter.png and a log fitter.log\n\nFrom Python shell\n==================\n\nFirst, let us create a data samples with N = 10,000 points from a gamma distribution::\n\n    from scipy import stats\n    data = stats.gamma.rvs(2, loc=1.5, scale=2, size=10000)\n\n.. note:: the fitting is slow so keep the size value to reasonable value.\n\nNow, without any knowledge about the distribution or its parameter, what is the distribution that fits the data best ? Scipy has 80 distributions and the **Fitter** class will scan all of them, call the fit function for you, ignoring those that fail or run forever and finally give you a summary of the best distributions in the sense of sum of the square errors. The best is to give an example::\n\n\n    from fitter import Fitter\n    f = Fitter(data)\n    f.fit()\n    # may take some time since by default, all distributions are tried\n    # but you call manually provide a smaller set of distributions\n    f.summary()\n\n\n.. image:: http://pythonhosted.org/fitter/_images/index-1.png\n    :target: http://pythonhosted.org/fitter/_images/index-1.png\n\n\nSee the `online <http://fitter.readthedocs.io/>`_ documentation for details.\n\n\nContributors\n=============\n\n\nSetting up and maintaining Fitter has been possible thanks to users and contributors.\nThanks to all:\n\n.. image:: https://contrib.rocks/image?repo=cokelaer/fitter\n    :target: https://github.com/cokelaer/fitter/graphs/contributors\n\n\n\n\nChangelog\n~~~~~~~~~\n========= ==========================================================================\nVersion   Description\n========= ==========================================================================\n1.7.0     * replace logging with loguru\n          * main application update to add missing --output-image option and use\n            rich_click\n          * replace pkg_resources with importlib\n1.6.0     * for developers: uses pyproject.toml instead of setup.py\n          * Fix progress bar fixing https://github.com/cokelaer/fitter/pull/74\n          * Fix BIC formula https://github.com/cokelaer/fitter/pull/77\n1.5.2     * PR https://github.com/cokelaer/fitter/pull/74 to fix logger\n1.5.1     * fixed regression putting back joblib\n1.5.0     * removed easydev and replaced by tqdm for progress bar\n          * progressbar from tqdm also allows replacement of joblib need\n1.4.1     * Update timeout in docs from 10 to 30 seconds by @mpadge in\n            https://github.com/cokelaer/fitter/pull/47\n          * Add Kolmogorov-Smirnov goodness-of-fit statistic by @lahdjirayhan in\n            https://github.com/cokelaer/fitter/pull/58\n          * switch branch from master to main\n1.4.0     * get_best function now returns the parameters as a dictionary\n            of parameter names and their values rather than just a list of\n            values (https://github.com/cokelaer/fitter/issues/23) thanks to\n            contributor @kabirmdasraful\n          * Accepting PR to fix progress bar issue reported in\n            https://github.com/cokelaer/fitter/pull/37\n1.3.0     * parallel process implemented https://github.com/cokelaer/fitter/pull/25\n            thanks to @arsenyinfo\n1.2.3     * remove vervose arguments in Fitter class. Using the logging module\n            instead\n          * the Fitter.fit has now a progress bar\n          * add a standalone application called … fitter (see the doc)\n1.2.2     was not released\n1.2.1     adding new class called histfit (see documentation)\n1.2       * Fixed the version. Previous version switched from\n            1.0.9 to 1.1.11. To start a fresh version, we increase to 1.2.0\n          * Merged pull request required by bioconda\n          * Merged pull request related to implementation of\n            AIC/BIC/KL criteria (https://github.com/cokelaer/fitter/pull/19).\n            This also fixes https://github.com/cokelaer/fitter/issues/9\n          * Implement two functions to get all distributions, or a list of\n            common distributions to help users decreading computational time\n            (https://github.com/cokelaer/fitter/issues/20). Also added a FAQS\n            section.\n          * travis tested Python 3.6 and 3.7 (not 3.5 anymore)\n1.1       * Fixed deprecated warning\n          * fitter is now in readthedocs at fitter.readthedocs.io\n1.0.9     * https://github.com/cokelaer/fitter/pull/8 and 11\n            PR https://github.com/cokelaer/fitter/pull/8\n1.0.6     * summary() now returns the dataframe (instead of printing it)\n1.0.5      https://github.com/cokelaer/fitter/issues\n1.0.2     add manifest to fix missing source in the pypi repository.\n========= ==========================================================================\n',
    'author': 'Thomas Cokelaer',
    'author_email': 'cokelaer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
