from django.apps import apps
from django.db.models.signals import pre_save, post_save
from django.dispatch import Signal
from django.dispatch import receiver

from .models.workflow import Workflow


@receiver(pre_save, sender=Workflow)
def handle_workflow(sender, instance, **kwargs):
    from .handler import handle_state_change

    previous_instance = sender.objects.filter(pk=instance.pk).first()
    if not previous_instance:
        return
    PreviousModel = apps.get_model(
        previous_instance.workflow_model.app_label,
        previous_instance.workflow_model.model,
    )
    pre_save.disconnect(handle_state_change, sender=PreviousModel)


@receiver(post_save, sender=Workflow)
def handle_workflow(sender, instance, created, **kwargs):
    from .handler import handle_state_change
    Model = apps.get_model(
        instance.workflow_model.app_label, instance.workflow_model.model
    )
    pre_save.connect(handle_state_change, sender=Model,dispatch_uid="handle_state_change_"+Model.__name__.lower())


post_state_change = Signal()
