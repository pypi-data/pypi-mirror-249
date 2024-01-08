import logging
import os

from setuptools import setup, find_namespace_packages

logger = logging.getLogger(__name__)
VERSION = "0.0.17"

# version = os.getenv("TGEDR_NIHAO_VERSION", VERSION)
version = VERSION 

logging.info(f"[tgedr-nihao] building version: {version}")

setup(
    name='tgedr-nihao',
    version=version,
    description='studies with financial data sources',
    url='https://github.com/jtviegas-sandbox/nihao',
    author='joao tiago viegas',
    author_email='jtviegas@gmail.com',
    license='Unlicense',
    classifiers=[
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
    ],
    keywords='finance development data science',
    include_package_data=True,
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=[
        "yfinance",
        "boto3>=1.28",
        "pyarrow>=14",
        "pyspark>=3.5"
    ],
    python_requires='>=3.7',
    # package_data={'sample': ['package_data.dat'],},
)
