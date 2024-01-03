from django.db import models

from .base import BaseModel


class Transition(BaseModel):
    workflow = models.ForeignKey(
        "Workflow",
        verbose_name="Workflow",
        related_name="transitions",
        on_delete=models.PROTECT,
    )
    source_state = models.ForeignKey(
        "TransitionState",
        verbose_name="Source TransitionState",
        related_name="transitions_source",
        on_delete=models.PROTECT,
    )
    destination_state = models.ForeignKey(
        "TransitionState",
        verbose_name="Destination TransitionState",
        related_name="transitions_destination",
        on_delete=models.PROTECT,
    )
    display_name = models.CharField(
        verbose_name="Display Name",
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.workflow} | {self.source_state.name} ---> {self.destination_state.name}"
    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.display_name = f"{self.source_state.name} ---> {self.destination_state.name}"
        super().save(force_insert, force_update, using, update_fields)
    class Meta:
        app_label = "cosmic_pipeline"
        verbose_name = "Transition"
        verbose_name_plural = "Transitions"
        unique_together = (
            ("workflow", "source_state", "destination_state"),
        )