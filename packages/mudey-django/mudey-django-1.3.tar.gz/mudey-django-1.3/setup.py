from setuptools import setup, find_packages
from io import open
from os import path
import pathlib


# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()




setup(
    name='mudey-django',
    version='1.3',
    packages=find_packages(),
    description='CLI Django',
    author='Espero-Soft Informatiques',
    author_email='contact@espero-soft.com',
    long_description=README,
    long_description_content_type='text/markdown',
    # url='lien_vers_le_code_source',
    entry_points={
        'console_scripts': [
            'mudey-django = package.module:main',
        ],
    },
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'annotated-types>=0.6.0',
        'asgiref>=3.7.2',
        'Django>=5.0',
        'inflect>=7.0.0',
        'prompt-toolkit>=3.0.36',
        'pydantic>=2.5.3',
        'pydantic_core>=2.14.6',
        'python-dateutil>=2.8.2',
        'questionary>=2.0.1',
        'setuptools>=69.0.3',
        'six>=1.16.0',
        'sqlparse>=0.4.4',
        'typing_extensions>=4.9.0',
        'tzdata>=2023.4',
        'wcwidth>=0.2.12'
    ],
)
