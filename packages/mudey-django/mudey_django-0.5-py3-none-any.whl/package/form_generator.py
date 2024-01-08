import argparse
from django import forms
from pathlib import Path
import re

# Dictionnaire associant les champs aux widgets correspondants
field_widgets = {
    'DateField': "forms.DateInput(attrs={'class': 'form-control datepicker'})",
    'DateTimeField': "forms.DateTimeInput(attrs={'class': 'form-control datetimepicker'})",
    'CharField': "forms.TextInput(attrs={'class': 'form-control custom-text-input'})",
    'EmailField': "forms.EmailInput(attrs={'class': 'form-control custom-email-input'})",
    'BooleanField': "forms.CheckboxInput(attrs={'class': 'form-control custom-checkbox'})",
    'IntegerField': "forms.NumberInput(attrs={'class': 'form-control custom-number-input'})",
    'FloatField': "forms.NumberInput(attrs={'class': 'form-control custom-float-input'})",
    'URLField': "forms.URLInput(attrs={'class': 'form-control custom-url-input'})",
    'FileField': "forms.ClearableFileInput(attrs={'class': 'form-control custom-file-input'})",
    'ImageField': "forms.ClearableFileInput(attrs={'class': 'form-control custom-image-input'})",
    'TextField': "forms.Textarea(attrs={'class': 'form-control custom-textarea'})",
    'SlugField': "forms.TextInput(attrs={'class': 'form-control custom-slug-input'})",
    'ChoiceField': "forms.Select(attrs={'class': 'form-control custom-select'})",
    'ModelChoiceField': "forms.Select(attrs={'class': 'form-control custom-model-select'})",
    'TimeField': "forms.TimeInput(attrs={'class': 'form-control custom-time-input'})",
    'DecimalField': "forms.NumberInput(attrs={'class': 'form-control custom-decimal-input'})",
}


def parse_model_fields(file_path):
    field_pattern = re.compile(r'^\s*(\w+)\s*=\s*models\.(\w+)\(', re.MULTILINE)
    fields = {}

    with open(file_path, 'r') as file:
        content = file.read()
        matches = field_pattern.finditer(content)

        for match in matches:
            field_name = match.group(1)
            field_type = match.group(2)
            fields[field_name] = field_type

    return fields

def generate_form(app_name, model_name):
    # Chemin du dossier des formulaires dans l'application spécifiée
    form_folder = Path(f"{app_name}/forms")

    if not form_folder.exists():
        form_folder.mkdir(parents=True)

    # Nom du fichier pour le formulaire
    form_filename = form_folder / f"{model_name}Form.py"

  
    if form_filename.exists():
        user_input = input(f"Le fichier '{form_filename}' existe déjà. Voulez-vous l'écraser ? (O/n): ")
        if user_input.lower() != 'o':
            print("Annulation de la création du formulaire.")
            return

    # Génération du contenu du formulaire Django
    model_filename = f"{app_name}/models/{model_name}.py"
    model_fields = parse_model_fields(model_filename)
    
    form_content = f"from django import forms\nfrom {app_name}.models import {model_name}\n\n"
    form_content += f"class {model_name}Form(forms.ModelForm):\n"
    form_content += f"    class Meta:\n"
    form_content += f"        model = {model_name}\n"
    form_content += f"        fields = {tuple(model_fields.keys())}\n\n"

    # Ajout des widgets aux champs spécifiques du modèle
    print(model_fields)
    form_content += "        widgets = {\n"
    for field_name, field_type in model_fields.items():
        field_type = field_type
        if field_type in field_widgets:
            form_content += f"            '{field_name}' : forms.{field_widgets[field_type]},\n"
         
    form_content += "        }\n"   
    # Écriture du contenu dans le fichier du formulaire
    with open(form_filename, "w") as form_file:
        form_file.write(form_content)

    print(f"Le formulaire {model_name}Form a été créé dans {form_folder} !")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générer un formulaire Django interactif.")
    parser.add_argument("app_name", help="Nom de l'application dans laquelle vous souhaitez générer le formulaire.")
    parser.add_argument("model_name", help="Nom du modèle pour lequel vous souhaitez générer le formulaire.")
    args = parser.parse_args()

    try:
        generate_form(args.model_name, args.app_name)
    except LookupError:
        print("L'application spécifiée est introuvable.")
