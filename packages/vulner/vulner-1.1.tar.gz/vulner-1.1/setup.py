from setuptools import setup, find_packages

setup(
    name='vulner',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'click',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'vulner = vulner.main:main',
        ],
    },
)