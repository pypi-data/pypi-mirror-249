from setuptools import setup, find_packages

setup(
    name='2267570-hw4',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'hw4=hw4:main',
        ],
    },
)
