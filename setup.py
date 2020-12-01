from setuptools import setup, find_packages

setup(
    name='j_archive',
    version=0.1,
    packages=find_packages(),
    install_requires=[
        'bs4',
        'glob2',
        'requests',
    ],
    author='Joseph Cappadona',
    author_email='josephcappadona27@gmail.com',
    description='a library to scrape and use data from j-archive.com',
    license='GPLv3',
)