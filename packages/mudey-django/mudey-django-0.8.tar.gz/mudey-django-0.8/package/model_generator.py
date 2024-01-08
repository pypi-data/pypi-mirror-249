# model_generator.py
import argparse
import questionary
from django.db import models
from pathlib import Path
import re

# Dictionnaire des types de champs Django correspondant aux choix possibles
field_choices = {
    "string": 'models.CharField',
    "integer": 'models.IntegerField',
    "text": 'models.TextField',
    "boolean": "models.BooleanField",
    "date": "models.DateField",
    "datetime": "models.DateTimeField",
    "email": "models.EmailField",
    "float": "models.FloatField",
    "decimal": "models.DecimalField",
    "file": "models.FileField",
    "image": "models.ImageField",
    "slug": "models.SlugField",
    "url": "models.URLField",
    "duration": "models.DurationField",
    "uuid": "models.UUIDField",
    "biginteger": "models.BigIntegerField",
    "positiveinteger": "models.PositiveIntegerField",
    "positivebiginteger": "models.PositiveBigIntegerField",
    "binary": "models.BinaryField",
    "smallinteger": "models.SmallIntegerField",
    "time": "models.TimeField",
    "genericip": "models.GenericIPAddressField",
    "foreignkey": 'models.ForeignKey',
    "relation": 'relation'
    # Ajoutez d'autres types de champs ici
}

def is_valid_model_name(name):
    return bool(re.match(r'^[a-zA-Z][_a-zA-Z0-9]*$', name))

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

def generate_model(app_name, model_name = False):
    # model_name = ""
    fields = [('updated_at', 'models.DateTimeField(auto_now=True)', {}),
              ('created_at', 'models.DateTimeField(auto_now_add=True)', {})]
    if not model_name:
        while True:
            model_name = questionary.text("Nom du modèle :").ask().strip()
            if not model_name:
                print("Le nom du modèle ne peut pas être vide. Veuillez saisir un nom valide.")
            elif not is_valid_model_name(model_name):
                print("Le nom du modèle n'est pas valide. Veuillez utiliser un nom de classe Python valide.")
            else:
                break
   
        
        
    model_folder = f"{app_name}/models"
    model_folder_path = Path(model_folder)

    if not model_folder_path.exists():
        model_folder_path.mkdir(parents=True)

    # Nom du fichier pour le modèle
    model_filename = f"{model_folder}/{model_name.capitalize()}.py"
    model_file_path = Path(model_filename)
    
    if model_file_path.exists():
        old_fields = parse_model_fields(model_file_path)
        print("==== fields =====")
        print(old_fields)
        print(f"Le fichier '{model_filename}' existe déjà. Ajouter des champs")
        

        

    while True:
        field_name = questionary.text("Nom du champ (laissez vide pour terminer) :").ask().strip()
        if not field_name:
            break

        field_type = questionary.text("Type du champ (tapez '?' pour voir la liste des types, appuyez sur Entrée pour 'string') :").ask().strip()
        while field_type not in field_choices and field_type != "":
            if field_type == '?':
                print("Types disponibles : ", ', '.join(field_choices.keys()))
            else:
                print("Types disponibles : ", ', '.join(field_choices.keys()))
            field_type = questionary.text("Type du champ (tapez '?' pour voir la liste des types, appuyez sur Entrée pour 'string') :").ask().strip()
 
        if field_type == "":
            field_type = "string"  # Utiliser 'string' par défaut si le type n'est pas valide
        elif field_type in field_choices:
            field_type = field_type
        else:
            if field_type == 'relation':
                related_model = questionary.text("Nom du modèle lié :").ask().strip()
                relationship_type = questionary.select("Type de relation :", choices=["OneToOne", "OneToMany", "ManyToOne", "ManyToMany"]).ask().strip()

                if relationship_type == "OneToOne":
                    fields.append((field_name, f"models.OneToOneField('{related_model}')", {'on_delete': 'models.CASCADE'}))
                elif relationship_type == "OneToMany":
                    fields.append((field_name, f"models.ForeignKey('{related_model}', related_name='{field_name}_set')", {'on_delete': 'models.CASCADE'}))
                elif relationship_type == "ManyToOne":
                    fields.append((field_name, f"models.ForeignKey('{related_model}')", {'on_delete': 'models.CASCADE'}))
                elif relationship_type == "ManyToMany":
                    fields.append((field_name, f"models.ManyToManyField('{related_model}')", {}))
            else:
                fields.append((field_name, field_choices[field_type], {}))
                
        
        null_choice = questionary.confirm("Le champ peut-il être null ?").ask()
            
     
        # Ajouter le champ avec le type et la propriété null appropriés à la liste des champs
        fields.append((field_name, field_choices[field_type], {'blank':null_choice, 'null':null_choice}))

  
    
    if model_file_path.exists():
        # Lire le fichier existant pour extraire les champs
        with open(model_filename, "r") as model_file:
            existing_code = model_file.read()

        # Extraire les noms des champs existants
        existing_fields = [line.strip().split()[0] for line in existing_code.splitlines() if line.strip().startswith(model_name.capitalize())]
        print((existing_fields,))

        # Vérifier les nouveaux champs par rapport aux champs existants
        fields_to_add = [(field_name, field_type, field_options) for field_name, field_type, field_options in fields if field_name not in existing_fields]

       
        # Ajouter les nouveaux champs 'created_at' et 'updated_at
        if fields_to_add:
            with open(model_filename, "a") as model_file:
                last = []
                for field_name, field_type, field_options in fields_to_add:
                    if field_name == "updated_at" or field_name == "created_at":
                        last.append((field_name, field_type, field_options))
                        continue
                    options_string = ', '.join([f"{key}={value}" for key, value in field_options.items()])
                    model_file.write(f"    {field_name} = {field_type}({options_string})\n")
                    
                # for field_name, field_type, field_options in last:
                #     options_string = ', '.join([f"{key}={value}" for key, value in field_options.items()])
                #     model_file.write(f"    {field_name} = {field_type}({options_string})\n")
                
                    
        print(f"Le modèle {model_name.capitalize()} a été mis à jour avec de nouveaux champs dans {model_filename} !")
    else:
        # ... Code pour créer le modèle s'il n'existe pas encore ...
        model_code = f"from django.db import models\n\n"
        model_code += f"class {model_name.capitalize()}(models.Model):\n"
        
        # Enregistrez le code du modèle dans un fichier spécifique
        with open(model_filename, "w") as model_file:
            model_file.write(model_code)
        
        fields_to_add = [(field_name, field_type, field_options) for field_name, field_type, field_options in fields]

       
        # Ajouter les  champs 
        if fields_to_add:
            with open(model_filename, "a") as model_file:
                last = []
                for field_name, field_type, field_options in fields_to_add:
                    if field_name == "updated_at" or field_name == "created_at":
                        last.append((field_name, field_type, field_options))
                        continue
                    options_string = ', '.join([f"{key}={value}" for key, value in field_options.items()])
                    model_file.write(f"    {field_name} = {field_type}({options_string})\n")
                    
                for field_name, field_type, field_options in last:
                    model_file.write(f"    {field_name} = {field_type}\n")
                
        print(f"Le modèle {model_name.capitalize()} a été créé dans {model_filename} !")
    # print(f"Le modèle {model_name.capitalize()} a été créé dans {model_filename} !")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générer un modèle Django interactif.")
    parser.add_argument("app_name", help="Nom de l'application dans laquelle vous souhaitez générer le dossier models.")
    parser.add_argument("model_name", help="Nom du model que vous souhaitez créer.")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.0")
    args = parser.parse_args()

    generate_model(app_name=args.app_name, model_name=args.model_name)