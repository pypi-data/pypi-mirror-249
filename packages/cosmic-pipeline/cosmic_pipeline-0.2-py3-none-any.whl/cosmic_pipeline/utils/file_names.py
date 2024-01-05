from ..constants import OperandChoices


def create_filters(rule_instance):
    value = rule_instance.value
    field_name = rule_instance.field
    if rule_instance.annotate:
        field_name = f"{field_name}__{rule_instance.annotate}"
    if rule_instance.operator == OperandChoices.NONE:
        filter_names = {f"{field_name}": value}
    else:
        filter_names = {f"{field_name}__{rule_instance.operator}": value}
    return filter_names
