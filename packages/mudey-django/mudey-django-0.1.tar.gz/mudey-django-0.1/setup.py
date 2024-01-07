from setuptools import setup, find_packages

setup(
    name='mudey-django',
    version='0.1',
    packages=find_packages(),
    description='CLI Django',
    author='Espero-Soft Informatiques',
    author_email='contact@espero-soft.com',
    # url='lien_vers_le_code_source',
    entry_points={
        'console_scripts': [
            'espero-django = package.module:__main__',
        ],
    },
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
