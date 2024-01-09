from setuptools import setup

setup(
    name='ThisPackageIsDataTransfer',
    version='1.0.0',
    packages=['DataTransfer'],
    entry_points={
        'console_scripts': [
            'transfer=DataTranser.main:main'
        ]
    }
)