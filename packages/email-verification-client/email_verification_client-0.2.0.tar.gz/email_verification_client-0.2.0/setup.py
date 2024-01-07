from setuptools import setup, find_packages

setup(
    name='email_verification_client',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)