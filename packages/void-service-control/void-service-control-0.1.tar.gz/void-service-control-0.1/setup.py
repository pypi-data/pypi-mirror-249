from setuptools import setup, find_packages

setup(
    name='void-service-control',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vsc = vsc.vsc:main'
        ],
    },
)

