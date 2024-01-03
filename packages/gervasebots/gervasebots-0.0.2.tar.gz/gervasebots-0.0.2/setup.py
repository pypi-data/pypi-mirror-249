from setuptools import setup, find_packages
print(find_packages())
setup(
    name='gervasebots',
    version='0.0.2',
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
