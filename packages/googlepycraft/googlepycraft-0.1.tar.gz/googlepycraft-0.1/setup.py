# setup.py

from setuptools import setup,find_packages

setup(
    name='googlepycraft',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'firebase-admin',
        'gspread',
        'oauth2client',
        'pandas',
    ],
)
