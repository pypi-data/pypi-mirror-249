from django.db.models import ForeignKey

from .fields.fields import StateField


def beautify_fields(field):
    field = field.split("_")
    field = " ".join(field)
    return field.title()


def get_all_fields(model):
    _fields = model._meta.get_fields()
    fields = [field for field in _fields if not isinstance(field, StateField)]
    return fields


def get_all_relation_fields(model):
    _fields = model._meta.get_fields()
    fields_ = [
        field
        for field in _fields
        if not isinstance(field, StateField)
        and not field.is_relation
        and not field.primary_key
    ]
    return fields_


def get_all_fields_of_relation(model, parent):
    _fields = get_all_relation_fields(model)
    choices = [
        (f"{parent}__{field.name}", beautify_fields(f"{parent}_{field.name}"))
        for field in _fields
    ]
    return choices


def model_fields_choices(model, parent=None):
    choices = []
    for field in get_all_fields(model):
        if field.is_relation:
            if isinstance(field, ForeignKey):
                choices.append((field.name, beautify_fields(field.name)))
                choices.extend(
                    get_all_fields_of_relation(field.related_model, field.name)
                )
            elif "related_name" not in field.__dict__:
                choices.append((field.name, beautify_fields(field.name)))
            elif not field.related_name:
                choices.append((f"{field.name}", beautify_fields(f"{field.name}")))
            else:
                choices.append(
                    (field.related_name, beautify_fields(field.related_name))
                )
        else:
            choices.append((field.name, beautify_fields(field.name)))
    return choices
