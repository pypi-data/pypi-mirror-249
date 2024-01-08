from setuptools import setup, find_packages

setup(
    name='vulne',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'click',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'CVE = CVE.main:main',
        ],
    },
)