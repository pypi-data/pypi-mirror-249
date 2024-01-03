from django.db import models
from django.db.models import (
    Count,
    Sum,
    Avg,
    Min,
    Max,
)
from django.db.models.signals import pre_save

from .base import BaseModel
from ..constants import AnnotateChoices, OperandChoices

ANNOTATE_METHODS = {
    "count": Count,
    "sum": Sum,
    "avg": Avg,
    "min": Min,
    "max": Max,
}


class RestrictRuleCondition(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    transition = models.ForeignKey(
        "Transition",
        verbose_name="Transition",
        related_name="restrict_rule_condition",
        on_delete=models.CASCADE,
    )
    field = models.CharField(max_length=255, blank=False, null=False)
    annotate = models.CharField(
        max_length=255, blank=True, null=True, choices=AnnotateChoices.choices
    )
    operator = models.CharField(
        max_length=255, choices=OperandChoices.choices, blank=False, null=False
    )
    value = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        app_label = "cosmic_pipeline"
        verbose_name = "Restrict Rule Condition"
        verbose_name_plural = "Restrict Rule Conditions"

    def make_condition(self, instance):
        transition = self.transition
        model = transition.workflow.workflow_model.model_class()
        if self.annotate and self.annotate.strip() != "":
            annotate_method = ANNOTATE_METHODS.get(self.annotate)
            if annotate_method is None:
                raise False
            annotate = {annotate_method(self.field)}
            if self.operator == OperandChoices.NONE:
                filters = {f"{self.field}": self.value}
            else:
                filters = {f"{self.field}__{self.operator}": self.value}
            return model.objects.annotate(*annotate).filter(id=instance.id, **filters)
        if self.operator == OperandChoices.NONE:
            filters = {f"{self.field}_id": self.value}
        else:
            value = self.value
            if self.operator == OperandChoices.ISNULL:
                value = True if value and value.lower() == "true" else False
            filters = {f"{self.field}__{self.operator}": value}
        return model.objects.filter(id=instance.id, **filters)


class ValidateRuleCondition(BaseModel):
    transition = models.ForeignKey(
        "Transition",
        verbose_name="Workflow",
        related_name="validate_rule_condition",
        on_delete=models.CASCADE,
    )
    permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="Permissions",
        related_name="validate_rule_condition",
        blank=True,
    )

    class Meta:
        app_label = "cosmic_pipeline"
        verbose_name = "Validate Rule Condition"
        verbose_name_plural = "Validate Rule Conditions"


def restrict_rule_condition_cleanup(sender, instance, **kwargs):
    if instance.annotate and instance.annotate.strip() == "":
        instance.annotate = None


pre_save.connect(restrict_rule_condition_cleanup, sender=RestrictRuleCondition)
