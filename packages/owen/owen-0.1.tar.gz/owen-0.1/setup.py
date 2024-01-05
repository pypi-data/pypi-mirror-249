import os
from setuptools import setup, find_packages

setup(
    name='owen',
    version='0.1',
    description='owen',
    author='owen',
    author_email='758024724@qq.com',
    packages=find_packages(),  # packages=["pytest"],
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[],
    # install_requires=['numpy>=1.16.4', 'scipy>=1.3.1', 'xarray>=0.15.0'],
)
