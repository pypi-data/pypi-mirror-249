import logging
import os

from setuptools import setup, find_namespace_packages

logger = logging.getLogger(__name__)
version = "0.0.20" 
logging.info(f"[tgedr-pycode] building version: {version}")

setup(
    name='tgedr-pycode',
    version=version,
    description='python handy code',
    url='https://github.com/jtviegas-sandbox/pycode',
    author='joao tiago viegas',
    author_email='jtviegas@gmail.com',
    license='Unlicense',
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
    ],
    keywords='python development pyspark',
    include_package_data=True,
    package_dir={"": "src/lib"},
    packages=find_namespace_packages(where="src/lib"),
    install_requires=[
        "matplotlib>=3",
        "matplotlib-inline",
        "numpy",
        "pandas",
        "pyspark>=3",
        "seaborn"
    ],
    python_requires='>=3.7',
    # package_data={'sample': ['package_data.dat'],},
)
