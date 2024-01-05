from ..models.rules import RestrictRuleCondition


def make_rule_from_rule_id(id,instance):
    rule = RestrictRuleCondition.objects.get(id=id)
    return rule.make_condition(instance).exists()


def check_restriction_rules(transition,instance):
    passed = True
    errors = {}
    rules = transition.restrict_rule_condition.all()
    for rule in rules:
        rule_info = make_rule_from_rule_id(rule.id,instance)
        if not rule_info:
            passed = False
            errors[rule.name] = "Failed"
    if errors:
        passed = False
    return passed, errors
