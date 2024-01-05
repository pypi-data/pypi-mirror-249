from .choices import get_all_fields, get_all_relation_fields
from .constants import OperandChoices


def filter_field_by_name(model, field_name):
    fields = get_all_fields(model) + get_all_relation_fields(model)
    if "__" in field_name:
        field_name = field_name.split("__")[-1]
    for field in fields:
        if field.is_relation:
            if "related_name" not in field.__dict__:
                if field.name == field_name:
                    return field
            elif not field.related_name:
                if f"{field.name}" == field_name:
                    return field
            else:
                if field.related_name == field_name:
                    return field
        else:
            if field.name == field_name:
                return field


def check_operations(model, field, operator, annotate):
    """
    Checks if the field is a relation and if it is a many to many relation
    """
    _field = filter_field_by_name(model, field)
    if _field.is_relation:
        if "related_name" not in _field.__dict__:
            if annotate:
                return operator in [
                    OperandChoices.GT,
                    OperandChoices.GTE,
                    OperandChoices.LT,
                    OperandChoices.LTE,
                    OperandChoices.NONE,
                ]
            return operator in [
                OperandChoices.IN,
                OperandChoices.ISNULL,
                OperandChoices.NONE,
            ]
        elif not _field.related_name or _field.related_name:
            if annotate:
                return operator in [
                    OperandChoices.GT,
                    OperandChoices.GTE,
                    OperandChoices.LT,
                    OperandChoices.LTE,
                    OperandChoices.NONE,
                ]
            return operator in [
                OperandChoices.IN,
            ]
        else:
            # TODO: Check if the related name is a many to many field
            return False
    else:
        return operator in [
            OperandChoices.IN,
            OperandChoices.EXACT,
            OperandChoices.IEXACT,
            OperandChoices.GT,
            OperandChoices.GTE,
            OperandChoices.LT,
            OperandChoices.LTE,
            OperandChoices.NONE,
            OperandChoices.ISNULL,
        ]
