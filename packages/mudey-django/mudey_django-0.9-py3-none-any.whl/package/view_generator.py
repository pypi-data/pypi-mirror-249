import argparse
from pathlib import Path
import inflect
import re


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

def get_plural(word):
    p = inflect.engine()
    plural_word = p.plural(word)
    return plural_word

def get_lower_plural(word):
    p = inflect.engine()
    plural_word = p.plural(word.lower())
    return plural_word

def copy_file(source_file, destination_file):
    try:
        with open(source_file, 'r') as source:
            with open(destination_file, 'w') as destination:
                content = source.read()
                destination.write(content)
        print(f"File copied from '{source_file}' to '{destination_file}' successfully.")
    except FileNotFoundError:
        print("File not found. Please provide valid file names.")

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






def generate_view(app_name, model_name):
    # Chemin du dossier des vues dans l'application spécifiée
    views_folder = Path(f"{app_name}/views")

    if not views_folder.exists():
        views_folder.mkdir(parents=True)

    # Nom du fichier pour la vue
    view_filename = views_folder / f"{model_name}View.py"

    if view_filename.exists():
        user_input = input(f"Le fichier '{view_filename}' existe déjà. Voulez-vous l'écraser ? (O/n): ")
        if user_input.lower() != 'o':
            print("Annulation de la création de la vue.")
            return

    # Génération du contenu de la vue Django
    view_content = f"from {app_name}.models import {model_name}\n"
    view_content += f"from django.shortcuts import render, get_object_or_404, redirect\n"
    view_content += f"from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage\n"
    view_content += f"from django.contrib import messages\n"
    view_content += f"from {app_name}.forms.{model_name}Form import {model_name}Form\n\n"
    view_content += f"def index(request):\n"
    view_content += f"    {get_plural(model_name.lower())}_list = {model_name}.objects.all()\n"
    view_content += f"    paginator = Paginator({get_plural(model_name.lower())}_list, 8)\n"
    view_content += f"    page = request.GET.get('page', 1)\n\n"
    view_content += f"    try:\n"
    view_content += f"        {get_plural(model_name.lower())} = paginator.page(page)\n"
    view_content += f"    except PageNotAnInteger:\n"
    view_content += f"        {get_plural(model_name.lower())} = paginator.page(1)\n"
    view_content += f"    except EmptyPage:\n"
    view_content += f"        {get_plural(model_name.lower())} = paginator.page(paginator.num_pages)\n"
    view_content += f"    except:\n"
    view_content += f"        {get_plural(model_name.lower())} = paginator.page(1)\n\n"
    view_content += f"    return render(request, '{app_name}/{get_plural(model_name.lower())}/{model_name.lower()}_index.html', {{'{get_plural(model_name.lower())}': {get_plural(model_name.lower())}}})\n\n"
    view_content += f"# Les autres fonctions comme show, create, update, delete... \n"
    view_content += f"def show(request, id):\n"
    view_content += f"    {model_name.lower()} = get_object_or_404({model_name}, id=id)\n"
    view_content += f"    return render(request, '{app_name}/{get_plural(model_name.lower())}/{model_name.lower()}_show.html', {{'{model_name.lower()}': {model_name.lower()}}})\n\n"

    view_content += f"def create(request):\n"
    view_content += f"    if request.method == 'POST':\n"
    view_content += f"        form = {model_name}Form(request.POST, request.FILES)\n"
    view_content += f"        if form.is_valid():\n"
    view_content += f"            form.save()\n"
    view_content += f"            messages.success(request, '{model_name} has been saved !')\n"
    view_content += f"            return redirect('{model_name.lower()}_index')\n"
    view_content += f"    else:\n"
    view_content += f"        form = {model_name}Form()\n"
    view_content += f"    return render(request, '{app_name}/{get_plural(model_name.lower())}/{model_name.lower()}_new.html', {{'form': form}})\n\n"
    
    view_content += f"def update(request, id):\n"
    view_content += f"    {model_name.lower()} = get_object_or_404({model_name}, id=id)\n\n"
    view_content += f"    if request.method == 'POST':\n"
    view_content += f"        if request.POST.get('_method') == 'PUT':\n"
    view_content += f"            form = {model_name}Form(request.POST, request.FILES, instance={model_name.lower()})\n"
    view_content += f"            if form.is_valid():\n"
    view_content += f"                form.save()\n"
    view_content += f"                messages.success(request, '{model_name} has been updated !')\n"
    view_content += f"                return redirect('{model_name.lower()}_index')\n"
    view_content += f"        else:\n"
    view_content += f"            form = {model_name}Form(instance={model_name.lower()})\n"
    view_content += f"    else:\n"
    view_content += f"        form = {model_name}Form(instance={model_name.lower()})\n"
    view_content += f"    return render(request, '{app_name}/{get_plural(model_name.lower())}/{model_name.lower()}_new.html', {{'form': form, '{model_name.lower()}': {model_name.lower()}}})\n\n"

    view_content += f"def delete(request, id):\n"
    view_content += f"    {model_name.lower()} = get_object_or_404({model_name}, id=id)\n"
    view_content += f"    if request.method == 'POST':\n"
    view_content += f"        if request.POST.get('_method') == 'DELETE':\n"
    view_content += f"            {model_name.lower()}.delete()\n"
    view_content += f"            messages.success(request, '{model_name} has been deleted !')\n"
    view_content += f"    return redirect('{model_name.lower()}_index')\n\n"
    

    # Écriture du contenu dans le fichier de la vue
    with open(view_filename, "w") as view_file:
        view_file.write(view_content)

    print(f"La vue {model_name}View a été créée dans {views_folder} !")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générer une vue Django pour un modèle.")
    parser.add_argument("app_name", help="Nom de l'application dans laquelle vous souhaitez générer la vue.")
    parser.add_argument("model_name", help="Nom du modèle pour lequel vous souhaitez générer la vue.")
    args = parser.parse_args()

    try:
        generate_view(model_name=args.model_name, app_name=args.app_name)
    except LookupError:
        print("L'application spécifiée est introuvable.")
