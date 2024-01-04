from setuptools import setup
from pathlib import Path

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = 'Gaussian and binomial distributions are two of the most important probability distributions in statistics and data analysis. Both distributions are available in PyPI as Python packages. This package provides a variety of functions for working with these distributions, including calculating probabilities, generating random samples, and plotting distributions.'



setup(name='distribgb',
      version='1.1',
      description='Gaussian and Binomial distributions',
      long_description = long_description,
      long_description_content_type='text/markdown',
      packages=['distribgb'],
      zip_safe=False)
