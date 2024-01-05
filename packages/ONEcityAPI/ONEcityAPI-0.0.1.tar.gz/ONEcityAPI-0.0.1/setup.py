from setuptools import setup, find_packages

DESCRIPTION = 'A Python package for interacting with the ONEcity API'
LONG_DESCRIPTION = 'This package provides a simple and intuitive interface for interacting with the ONEcity API. It includes features for getting water consumption data and customer info.'

setup(
    name="ONEcityAPI",
    version='0.0.1',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Alon Teplitsky",
    author_email="alon.ttp@gmail.com",
    license='MIT',
    url="https://github.com/0xAlon/ONEcityAPI",
    packages=find_packages(),
    install_requires=["requests", "urllib3"],
    keywords='ONEcityAPI'
)
