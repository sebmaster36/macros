from setuptools import setup

setup(
    name='client',
    packages=['client'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)