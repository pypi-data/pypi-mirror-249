from setuptools import setup

setup(name = 'hydromt_wff',
      version= '0.0.2',
      description= 'The package automates the pre-processing and preparation of Delft3D FM to simulates wadi flash floods',
      author= 'Aseel Moahmed',
      packages=['hydromt_wff'],
      package_data={'hydromt_wff': ['data/*.csv']},
      zip_safe=False)