from setuptools import setup, find_packages

setup(
    name='vuln',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'click',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'vuln = vuln:main',
        ],
    },
)