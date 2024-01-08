from setuptools import setup, find_packages

setup(
    name='mudey-django',
    version='0.8',
    packages=find_packages(),
    description='CLI Django',
    author='Espero-Soft Informatiques',
    author_email='contact@espero-soft.com',
    long_description='''# mudey-django CLI

Ce package fournit une interface en ligne de commande (CLI) pour simplifier la génération de composants dans des projets Django.

## Installation

Pour installer `mudey-django`, utilisez `pip` :

```bash
pip install mudey-django
```

## Utilisation

Une fois installé, `mudey-django` peut être utilisé pour générer différents composants d'une application Django. Voici quelques exemples de commandes disponibles :

- Créer une entité :
  ```bash
  mudey-django make:entity nom_application nom_modele
  ```
- Créer un formulaire :
  ```bash
  mudey-django make:form nom_application nom_modele
  ```
- Créer un modèle :
  ```bash
  mudey-django make:model nom_application nom_modele
  ```
- Créer une vue :
  ```bash
  mudey-django make:view nom_application nom_modele
  ```
- Créer des opérations CRUD pour une entité :
  ```bash
  mudey-django make:crud nom_application nom_modele
  ```

Assurez-vous d'avoir votre environnement Django configuré avant d'utiliser ces commandes.

## Configuration requise

Ce package nécessite Python 3.x et les dépendances listées dans `setup.py`.

## Contributions

Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce package, n'hésitez pas à ouvrir une issue ou à proposer une pull request.

## Auteurs

Ce package est maintenu par Espero-Soft Informatiques. Contactez-nous à contact@espero-soft.com pour toute question ou commentaire.

''',
    long_description_content_type='text/markdown',
    # url='lien_vers_le_code_source',
    entry_points={
        'console_scripts': [
            'mudey-django = package.module:main',
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
