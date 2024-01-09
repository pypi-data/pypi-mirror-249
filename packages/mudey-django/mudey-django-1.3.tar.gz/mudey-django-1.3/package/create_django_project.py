import argparse
import subprocess
from pathlib import Path

def check_django_installation():
    try:
        # Vérifier l'installation de Django en tentant d'importer le module
        import django
        return True
    except ImportError:
        return False

def install_django():
    try:
        subprocess.run(["pip", "install", "django"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_django_project(project_name):
    # Vérifier si Django est installé, sinon l'installer
    if not check_django_installation():
        print("Django not found. Installing Django...")
        if not install_django():
            print("Failed to install Django. Aborting project creation.")
            return

    try:
        # Création du répertoire pour le projet
        project_dir = Path.cwd() / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        # Création du projet Django dans le répertoire spécifié
        subprocess.run(["django-admin", "startproject", "config", str(project_dir)], check=True)
        print(f"Project '{project_name}' created successfully in '{project_dir}'!")

        # Configuration des paramètres dans settings.py
        BASE_DIR = Path.cwd() / project_name
        settings_file = BASE_DIR / 'config' / 'settings.py'

        if settings_file.exists():
            STATIC = "static"
            MEDIA_ROOT = "media"
            
            with open(settings_file, 'a') as f:
                f.write(f"\n\n# Added by script\n")
                f.write(f"STATIC_URL = '/{STATIC}/'\n")
                f.write(f"STATICFILES_DIRS = [BASE_DIR / '{STATIC}']\n")
                f.write(f"MEDIA_URL = '/media/'\n")
                f.write(f"MEDIA_ROOT = BASE_DIR / '{MEDIA_ROOT}'\n")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating project '{project_name}': {e}")
        return

def main():
    parser = argparse.ArgumentParser(description="Create a Django project")
    parser.add_argument("project_name", help="Name of the Django project to create")
    args = parser.parse_args()

    create_django_project(args.project_name)

if __name__ == "__main__":
    main()
