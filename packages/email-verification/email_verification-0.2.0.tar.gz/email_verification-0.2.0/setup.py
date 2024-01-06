# setup.py
from setuptools import setup, find_packages

setup(
    name='email_verification',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2',
        'wemake-python-styleguide==0.18.0',

    ],
)
