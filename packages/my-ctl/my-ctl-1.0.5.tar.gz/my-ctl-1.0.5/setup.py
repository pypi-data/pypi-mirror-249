from setuptools import setup, find_packages
setup(
name='my-ctl',
version='1.0.5',
description='myctl quick create  project',
author_email='labelnet@foxmail.com',
author='labelnet',
license='labelnet',
keywords=['my-ctl'],
packages=find_packages(),
include_package_data=True,
install_requires=['nuitka', 'requests', 'pytest', 'pyyaml', 'click', 'twine'],
python_requires='>=3.8',
entry_points="""
[console_scripts]
myctl=my_ctl:cli
"""
)