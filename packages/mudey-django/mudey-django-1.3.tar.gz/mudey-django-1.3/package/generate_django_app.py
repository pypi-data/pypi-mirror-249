import argparse
import subprocess
from pathlib import Path

def generate_django_app(app_name):
    try:
        # Créer l'application Django en utilisant django-admin
        subprocess.run(["django-admin", "startapp", app_name], check=True)
        print(f"Django app '{app_name}' created successfully!")
        
        # Supprimer le fichier models.py
        models_file = Path.cwd() / app_name / "models.py"
        models_file.unlink()
        views_file = Path.cwd() / app_name / "views.py"
        views_file.unlink()

        # Créer un répertoire models
        models_dir = Path.cwd() / app_name / "models"
        views_dir = Path.cwd() / app_name / "views"
        models_dir.mkdir(exist_ok=True)
        views_dir.mkdir(exist_ok=True)
        print(f"Directory '{models_dir}' created successfully!")
        
        
        # Créer le fichier urls.py avec les URL patterns
        urls_file = Path.cwd() / app_name / "urls.py"
        if not urls_file.exists():
            with open(urls_file, 'w') as f:
                f.write("from django.urls import path\n")
                f.write("from . import views\n\n")
                f.write("urlpatterns = [\n")
                f.write("    path('', views.index, name='home'),\n")
                f.write("]\n")
            print(f"File '{urls_file}' created successfully!")


    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating Django app '{app_name}': {e}")
        return

def main():
    parser = argparse.ArgumentParser(description="Generate a Django app")
    parser.add_argument("app_name", help="Name of the Django app to create")
    args = parser.parse_args()

    generate_django_app(args.app_name)

if __name__ == "__main__":
    main()
