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
