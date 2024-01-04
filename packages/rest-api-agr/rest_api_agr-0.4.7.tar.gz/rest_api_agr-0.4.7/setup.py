from setuptools import setup, find_packages
from src.rest_api_agr import __version__


with open('requirements.txt') as f:
    requirements = f.readlines()


with open("README.md", 'r') as f:
    long_description = f.read()


setup(
    name='rest_api_agr',
    version=__version__,
    author='agrubio',
    author_email="ablg11673@gmail.com",
    description='This package is made for an example of REST API.',
    url='https://github.com/AbelGRubio/01-rest-api.git',
    keywords='development, setup, setuptools',
    python_requires='>=3.12',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['rest_api_agr', 'rest_api_agr.*']),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # include_package_data=True,
    # package_data={'': ['data/*.csv', 'data/*.txt']},
)
