from setuptools import setup, find_packages

setup(
    name='stochastic_relaxation',
    author='Eron Ristich',
    author_email='eristich@asu.edu',
    description='Implementation of various algorithms for integration of the generalized Langevin equation',
    packages=find_packages(where='src'),
    install_requires=[
        'numpy',
        'scipy',
        'matplotlib',
        'tqdm',
        'pint',
        'xarray',
        'zarr',
        'argparse'
    ],
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
