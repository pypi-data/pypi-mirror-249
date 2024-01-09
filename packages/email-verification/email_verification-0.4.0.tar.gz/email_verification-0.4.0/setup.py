# setup.py
from setuptools import setup, find_packages

setup(
    name='email_verification',
    version='0.4.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2',
        'urllib3==2.1.0',

    ],
)
