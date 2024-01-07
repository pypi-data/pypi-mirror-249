import argparse
from pathlib import Path
import inflect
from form_generator import parse_model_fields



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
        

def create_view_paginator(model_name, app_name):
    template_folder = Path(f"{app_name}/templates/{app_name}/{get_plural(model_name.lower())}")
    model_filename = f"{app_name}/models/{model_name}.py"
    model_fields = parse_model_fields(model_filename)
    
    

        
    index_content = '''
                    {% if datas.has_other_pages %}
                        <nav aria-label="Page navigation example">
                            <ul class="pagination">
                                {% if datas.has_previous %}
                                    <li class="page-item">
                                        <a href="?page={{ datas.previous_page_number }}" class="page-link" href="#">Previous</a>
                                    </li>
                                {% else %}
                                    <li class="page-item disabled">
                                        <span class="page-link">Previous</span>
                                    </li>
                                    
                                {% endif %}
                                
                            
                                {% for page in datas.paginator.page_range %}
                                    {% if  page >= datas.number|add:'-2' and page <= datas.number|add:'2'  %}
                                        <li class="page-item">
                                            <a href="?page={{page}}" class="page-link {% if datas.number == page %} active {% endif %}">{{ page }}</a>
                                        </li>
                                    {% endif %}
                                    
                                {% endfor %}

                                {% if datas.has_next %}
                                    <li class="page-item">
                                        <a href="?page={{ datas.next_page_number }}" class="page-link">Next</a>
                                    </li>
                                {% else %}
                                    <li class="page-item disabled">
                                        <span class="page-link">Next</span>
                                    </li>
                                    
                                {% endif %}
                            </ul>
                        </nav>
                        <p>
                            {{ datas.number }} of {{ datas.paginator.num_pages }}
                        </p>
                        {% endif %}
                        '''

    with open(template_folder / "paginator.html", "w") as index_file:
        index_file.write(index_content)
     
def create_view_index(model_name, app_name):
    template_folder = Path(f"{app_name}/templates/{app_name}/{get_plural(model_name.lower())}")
    model_filename = f"{app_name}/models/{model_name}.py"
    model_fields = parse_model_fields(model_filename)
    
    table_header = ""
    for key, value in model_fields.items():
        table_header += f"    <th scope='col'>{key}</td>\n"
     
    table_content = ""
    for key, value in model_fields.items():
        table_content += "    <td scope='col'>{{ "+ model_name.lower() +"."+key + "}}</td>\n"
        
    table_content += f'''<td>
                        <a href="{{% url '{model_name.lower()}_view' {model_name.lower()}.id %}}" class="btn btn-success">View</a>
                        <a href="{{% url '{model_name.lower()}_edit' {model_name.lower()}.id %}}" class="btn btn-primary">Edit</a>
                        <form action="{{% url '{model_name.lower()}_delete' {model_name.lower()}.id %}}" method="post">
                            {{% csrf_token %}}
                            <input type="hidden" name="_method" value="DELETE">
                            <button class="btn btn-danger">Delete</button>
                        </form>
                    </td>'''

        
    index_content = '''{% extends "''' + app_name + '''/admin.html" %}
    {% load static %}

    {% block content %}

    {% include "''' + app_name + '''/admin/paginator.html" with datas=''' + get_lower_plural(model_name) + ''' %}
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-success">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    <div class="d-flex my-2 justify-content-end">
        <a href="{% url ''' + model_name.lower() + ''' %}" class="btn btn-success">Create '''+model_name+'''</a>
    </div>
    <table class="table table-bordered">
        <thead>
            <tr>
                <td scope="col">#</td>
                ''' + table_header + '''
                <th scope="col">Actions</th>
            </tr>
        </thead>
        <tbody>

            {% for ''' + model_name.lower() + ''' in ''' + get_lower_plural(model_name) + ''' %}
                <td scope="col">{{ ''' + model_name.lower() + '''.id }}</td>
                ''' + table_content + '''
            {% endfor %}

        </tbody>
    </table>
    {% include "blog/components/paginator.html" with datas=''' + get_lower_plural(model_name) + ''' %}


    {% endblock %}'''

    with open(template_folder / f"{model_name.lower()}_index.html", "w") as index_file:
        index_file.write(index_content)
     
def create_view_show(model_name, app_name):
    template_folder = Path(f"{app_name}/templates/{app_name}/{get_plural(model_name.lower())}")
    model_filename = f"{app_name}/models/{model_name}.py"
    model_fields = parse_model_fields(model_filename)
    
    table_content = ""
    for key, value in model_fields.items():
        table_content += "    <tr>\n"
        table_content += "        <td scope='col'> "+key.capitalize() + ": </td>\n"
        table_content += "        <td scope='col'>{{ "+ model_name.lower() +"."+key + "}}</td>"
        table_content += "    </tr>"
        
    

        
    index_content = '''{% extends "''' + app_name + '''/admin.html" %}
    {% load static %}

    {% block content %}

    {% include "''' + app_name + '''/admin/paginator.html" with datas=''' + get_lower_plural(model_name) + ''' %}
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-success">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    <div class="d-flex my-2 justify-content-end">
        <a href="{% url ''' + model_name.lower() + ''' %}" class="btn btn-success">Create '''+model_name+'''</a>
    </div>
    <table class="table table-bordered">
        <tbody>

            ''' + table_content + '''

        </tbody>
    </table>
    {% include "blog/components/paginator.html" with datas=''' + get_lower_plural(model_name) + ''' %}


    {% endblock %}'''

    with open(template_folder / f"{model_name.lower()}_show.html", "w") as index_file:
        index_file.write(index_content)
     
def create_view_edit(model_name, app_name):
    template_folder = Path(f"{app_name}/templates/{app_name}/{get_plural(model_name.lower())}")
    form_link = f"{model_name.lower()}_form.html"
    # model_filename = f"{app_name}/models/{model_name}.py"
    # model_fields = parse_model_fields(model_filename)
    

        
    index_content = '''{% extends "''' + app_name + '''/admin.html" %}
    {% load static %}

    {% block content %}
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-success">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="d-flex my-2 justify-content-end">
        <a href="{% url ''' + model_name.lower() + ''' %}" class="btn btn-success">Edit '''+model_name+'''</a>
    </div>
    
    {% include "''' + form_link + '''" with ''' + model_name.lower() + '''=''' + model_name.lower() + ''' %}


    {% endblock %}'''

    with open(template_folder / f"{model_name.lower()}_edit.html", "w") as index_file:
        index_file.write(index_content)
     
def create_view_create(model_name, app_name):
    template_folder = Path(f"{app_name}/templates/{app_name}/{get_plural(model_name.lower())}")
    form_link = f"{model_name.lower()}_form.html"
    # model_filename = f"{app_name}/models/{model_name}.py"
    # model_fields = parse_model_fields(model_filename)
    

        
    index_content = '''{% extends "''' + app_name + '''/admin.html" %}
    {% load static %}

    {% block content %}
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-success">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
    
    <div class="d-flex my-2 justify-content-end">
        <a href="{% url ''' + model_name.lower() + ''' %}" class="btn btn-success">Create '''+model_name+'''</a>
    </div>
    
    {% include "''' + form_link + '''" with ''' + model_name.lower() + '''=''' + model_name.lower() + ''' %}


    {% endblock %}'''

    with open(template_folder / f"{model_name.lower()}_create.html", "w") as index_file:
        index_file.write(index_content)
     
def create_view_form(model_name, app_name):
    template_folder = Path(f"{app_name}/templates/{app_name}/{get_plural(model_name.lower())}")
    model_filename = f"{app_name}/models/{model_name}.py"
    model_fields = parse_model_fields(model_filename)
    
    form_content = ""
    for key, value in model_fields.items():
        form_content += "    <div class='form-group'>\n"
        form_content += f"        <label for='{key}'> { key.capitalize() }: </label>\n"
        form_content += "        {{ form."+key+" }}\n"
        form_content += '''
                    {% if form.'''+key+'''.errors %}
                        {% for error in form.'''+key+'''.errors %}
                            <span class="text-danger">
                                {{error}}
                            </span>
                        {% endfor %}
                    {% endif %}
        '''
        form_content += "    </div>"
        
    

        
    index_content = '''<form action="" method="post">
                            {% csrf_token %}

                            {% if '''+ model_name.lower() +''' %}
                                <input type="hidden" name="_method" value="PUT" >
                            {% endif %}
                            '''+form_content+'''
                            
                            <div>
                            {% if '''+ model_name.lower() +''' %}
                                <button class="btn btn-success my-2">Update</button>
                            {% else %}
                                <button class="btn btn-success my-2">Create</button>
                            {% endif %}
                                
                            <a href="{% url '''+ model_name.lower() +'''_index %}" class="btn btn-danger my-2">Cancel</a>
                        </div>
                        </form>
                        {% block scripts %}
                        <script src="https://cdn.ckeditor.com/ckeditor5/40.2.0/classic/ckeditor.js"></script>

                        <script>
                            $(document).ready(function() {
                                $('select').select2();
                            });

                        </script>
                        <script>
                            const editors = document.querySelectorAll('textarea')

                            editors.forEach(editor => {
                                editor.removeAttribute('required')
                                ClassicEditor
                                    .create(editor)
                                    .catch( error => {
                                        console.error( error );
                                    } );
                                
                            });
                        </script>
                        {% endblock %}
                        '''

    with open(template_folder / f"{model_name.lower()}_form.html", "w") as index_file:
        index_file.write(index_content)
     

def generate_templates(model_name, app_name):
    
    template_folder = Path(f"{app_name}/templates/{app_name}/{get_plural(model_name.lower())}")

    if not template_folder.exists():
        template_folder.mkdir(parents=True)

    # paginator template
    create_view_paginator(model_name, app_name)

    # Index template
    create_view_index(model_name, app_name)

    # Detail template
    create_view_show(model_name, app_name)
        
    # Edit template
    create_view_edit(model_name, app_name)
        
    # Edit template
    create_view_create(model_name, app_name)
        
    # Edit template
    create_view_form(model_name, app_name)
        
    print(f"Templates for {model_name} generated in {template_folder}!")


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
        generate_templates(model_name=args.model_name, app_name=args.app_name)
    except LookupError:
        print("L'application spécifiée est introuvable.")
