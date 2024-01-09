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
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générer une vue Django pour un modèle.")
    parser.add_argument("app_name", help="Nom de l'application dans laquelle vous souhaitez générer la vue.")
    parser.add_argument("model_name", help="Nom du modèle pour lequel vous souhaitez générer la vue.")
    args = parser.parse_args()

    try:
        generate_templates(model_name=args.model_name, app_name=args.app_name)
    except LookupError:
        print("L'application spécifiée est introuvable.")
