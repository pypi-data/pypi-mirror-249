from setuptools import setup, find_packages

setup(
    name='gervasebots',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'gervasebots=gervasebots:main',
        ],
    },
)
