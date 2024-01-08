# setup.py

from setuptools import setup,find_packages

setup(
    name='googlepycraft',
    version='0.1.1',
    packages=find_packages(),
    author='Fru Ngwa',
    author_email='fru.ngwa22@gmail.com',
    url='https://github.com/Fru404',
    install_requires=[
        'firebase-admin',
        'gspread',
        'oauth2client',
        'pandas',
        'PyYAML',
    ],
    description='A Python package for manipulating google sheets directly on any coding platform and perform CRUD operations easily. Sheets can be stored and retrieved in firebase storage'
)
