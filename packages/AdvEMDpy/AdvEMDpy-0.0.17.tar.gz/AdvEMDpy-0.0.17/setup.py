
from setuptools import setup

setup(
  name = 'AdvEMDpy',
  packages = ['AdvEMDpy'],
  version = '0.0.17',
  license='cc-by-nc-4.0',
  description = 'Advanced Empirical Mode Decomposition package with '
                'numerous extensions to various aspects of core algorithm.',
  long_description = 'AdvEMDpy is a Python library that performs Empirical Mode Decomposition with numerous algorithmic variations available at key stages of the core algorithm. This package was developed out of research performed by Cole van Jaarsveldt, Matthew Ames, Gareth W. Peters, and Mike Chantler.',
  author = 'Cole van Jaarsveldt',
  author_email = 'colevj0303@gmail.com',
  url = 'https://github.com/Cole-vJ/AdvEMDpy.git',
  download_url = 'https://github.com/Cole-vJ/AdvEMDpy/archive/refs/tags/v0.0.17.tar.gz',
  keywords = ['EMPIRICAL MODE DECOMPOSITION', 'EMD', 'STATISTICAL EMPIRICAL MODE DECOMPOSITION', 'SEMD',
              'ENHANCED EMPIRICAL MODE DECOMPOSITION', 'EEMD', 'ENSEMBLE EMPIRICAL MODE DECOMPOSITION',
              'HILBERT TRANSFORM', 'TIME SERIES ANALYSIS', 'FILTERING', 'GRADUATION', 'WINSORIZATION', 'DOWNSAMPLING',
              'SPLINES', 'KNOT OPTIMISATION', 'PYTHON', 'R', 'MATLAB',
              'FULL-SPECTRUM ENSEMBLE EMPIRICAL MODE DECOMPOSITION', 'FSEEMD', 'COMPRESSIVE SAMPLING',
              'COMPRESSIVE SAMPLING EMPIRICAL MODE DECOMPOSITION', 'CSEMD'],
  install_requires=[
          'numpy',
          'seaborn',
	  'scipy',
	  'matplotlib',
	  'cvxpy',
	  'colorednoise',
	  'pytest',
	  'PyEMD',
	  'emd',
	  'pandas',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: Free for non-commercial use',
    'Programming Language :: Python :: 3.11',
  ],
)
