import pprint

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models, OperationalError
from django.db.models import Q

from ..exceptions import CosmicPipelineValidationError
from .base import BaseModel

def is_model_made_by_simple_history(model):
    return hasattr(model, 'tracked_fields')

def get_workflow_choices():
    from .transitionstate import TransitionState

    filter = Q()
    all_models = apps.get_models()
    models_using_foreignkey = []
    for model in all_models:
        related_objects = model._meta.get_fields()
        for related_object in related_objects:
            if (
                related_object.is_relation
                and related_object.many_to_one
                and related_object.related_model == TransitionState
                and model._meta.app_label != "cosmic_pipeline"
            ):
                if getattr(settings, "COSMIC_PIPELINE_EXCLUDE_SIMPLE_HISTORY", False) and is_model_made_by_simple_history(model):
                    continue
                else:
                    models_using_foreignkey.append(
                        model._meta.app_label + "." + model._meta.object_name
                    )
                    filter |= Q(
                        app_label=model._meta.app_label,
                        model=model._meta.object_name.lower(),
                    )

    ContentTypes = apps.get_model("contenttypes", "ContentType")
    try:
        models_using_foreignkey = ContentTypes.objects.filter(filter)
        choices = [(None, "-----")] + [
            (model.id, model.name) for model in models_using_foreignkey
        ]
    except Exception:
        choices = [(None, "-----")]
    return tuple(choices)


def check_workflow_from_choices(workflow_model):
    """
    Checks if the workflow_model is in the choices
    """
    choices = get_workflow_choices()
    for choice in choices:
        if choice[0] == workflow_model.id:
            return True
    return False


class Workflow(BaseModel):
    workflow_model = models.OneToOneField(
        ContentType,
        verbose_name="Workflow Model",
        related_name="workflows",
        on_delete=models.PROTECT,
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "cosmic_pipeline"
        verbose_name = "Workflow"
        verbose_name_plural = "Workflows"

    def clean_fields(self, exclude=None):
        """
        Validates the workflow
        """
        if self.workflow_model:
            check_workflow = check_workflow_from_choices(self.workflow_model)
            if not check_workflow:
                raise CosmicPipelineValidationError(
                    "The workflow model is not in the choices"
                )
        return super().clean_fields(exclude=exclude)
