import argparse
from model_generator import generate_model
from view_generator import generate_templates, generate_view
from form_generator import generate_form

# ...

def make_entity(args):
    print(f"Executing make:entity command for app: {args.app_name} and model: {args.model_name}.")
    # generate_entity()
    generate_model(app_name=args.app_name, model_name=args.model_name)
    generate_view(app_name=args.app_name, model_name=args.model_name)
    generate_templates(model_name=args.model_name, app_name=args.app_name)

def make_form(args):
    print(f"Executing make:form command for app: {args.app_name} and model: {args.model_name}")
    generate_form(app_name=args.app_name, model_name=args.model_name)

def make_view(args):
    print(f"Executing make:model command for app: {args.app_name} and model: {args.model_name}")
    generate_view(app_name=args.app_name, model_name=args.model_name)
    generate_templates(model_name=args.model_name, app_name=args.app_name)
    
def make_model(args):
    print(f"Executing make:model command for app: {args.app_name} and model: {args.model_name}")
    generate_model(app_name=args.app_name, model_name=args.model_name)

def make_entity_crud(args):
    print(f"Executing make:entity:crud command for app: {args.app_name} and model: {args.model_name}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Custom CLI for performing tasks")
    subparsers = parser.add_subparsers()

    entity_parser = subparsers.add_parser("make:entity", help="Create an entity")
    entity_parser.add_argument("app_name", help="Name of the app")
    entity_parser.add_argument("model_name", help="Name of the model")
    entity_parser.set_defaults(func=make_entity)

    form_parser = subparsers.add_parser("make:form", help="Create a form")
    form_parser.add_argument("app_name", help="Name of the app")
    form_parser.add_argument("model_name", help="Name of the model")
    form_parser.set_defaults(func=make_form)
    
    model_parser = subparsers.add_parser("make:model", help="Create a model")
    model_parser.add_argument("app_name", help="Name of the app")
    model_parser.add_argument("model_name", help="Name of the model")
    model_parser.set_defaults(func=make_model)
    
    view_parser = subparsers.add_parser("make:view", help="Create a view")
    view_parser.add_argument("app_name", help="Name of the app")
    view_parser.add_argument("model_name", help="Name of the model")
    view_parser.set_defaults(func=make_view)

    entity_crud_parser = subparsers.add_parser("make:crud", help="Create CRUD for an entity")
    entity_crud_parser.add_argument("app_name", help="Name of the app")
    entity_crud_parser.add_argument("model_name", help="Name of the model")
    entity_crud_parser.set_defaults(func=make_entity_crud)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
