from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

from .base import BaseModel
from .workflow import Workflow


class TransitionState(BaseModel):
    workflow = models.ForeignKey(
        Workflow,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="states",
        related_query_name="state",
    )
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    initial= models.BooleanField(default=False)

    def save(
        self, *args,**kwargs
    ):
        if self.initial:
            self.__class__.objects.filter(workflow=self.workflow).update(initial=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.workflow} | {self.name}"

    class Meta:
        app_label = "cosmic_pipeline"
        verbose_name = "TransitionState"
        verbose_name_plural = "States"
        unique_together = ("workflow", "slug")

    def next_possible_states(self):
        return self.__class__.objects.filter(id__in=self.transitions_source.all().values_list(
            "destination_state__id", flat=True)
        )

def on_pre_save(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


pre_save.connect(on_pre_save, TransitionState)
