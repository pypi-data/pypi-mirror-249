# mudey-django CLI

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

