import os
from setuptools import find_packages, setup

# Utility function to read the README file.
# Used for the long_description. 
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='netbox-plugin-netdisco',
    version='0.1',
    description=('A plugin for comparing and synchronizing Netdisco device'
     'inventory with NetBox.'),
    long_description=read('README.md'),
    url='https://github.com/mksoska/netbox-plugin-netdisco',
    author='Marek Soska',
    author_email='mareksoska22@gmail.com',
    keywords='netbox plugin netdisco topology',
    license='MIT',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)