from functools import partial

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

from .exceptions import CosmicPipelineValidationError
from .fields.fields import StateField
from .models.transition import Transition
from .models.workflow import Workflow
from .signals import post_state_change
from .utils.check_restriction_rules import check_restriction_rules


def post_state_change_handler(
    sender, instance, created, previous_state, current_state, **kwargs
):
    post_state_change.send(
        sender=instance.__class__,
        instance=instance,
        created=created,
        transition=Transition.objects.get(
            workflow=instance.state.workflow,
            source_state=previous_state,
            destination_state=current_state,
        ),
        previous_state=previous_state,
        current_state=current_state,
    )
    post_save.disconnect(
        sender=sender,
        dispatch_uid=f"post_state_change_{previous_state.name}_{current_state.name}",
    )


def handle_state_change(sender, instance, **kwargs):
    fields = sender._meta.fields
    char_fields = [field for field in fields if isinstance(field, StateField)]
    if char_fields:
        field_name = char_fields[0].name
        current_state = getattr(instance, field_name)
        previous_instance = sender.objects.filter(pk=instance.pk).first()
        if current_state and previous_instance:
            previous_state = getattr(previous_instance, field_name)
            if previous_state is None and current_state and current_state.initial:
                # Info
                # Added Condition to allow initial state to be set
                # without any previous state
                # Not triggering any post_state_change signal
                # Further validation can be added here
                pass
            elif previous_state != current_state:
                content_type = ContentType.objects.get(
                    app_label=instance._meta.app_label,
                    model=instance._meta.object_name.lower(),
                )
                workflow = Workflow.objects.get(workflow_model=content_type)

                transition = Transition.objects.filter(
                    workflow=workflow,
                    source_state=previous_state,
                    destination_state=current_state,
                )
                if not transition:
                    raise CosmicPipelineValidationError(
                        {
                            field_name: CosmicPipelineValidationError(
                                "Invalid state transition", code="validation_error"
                            )
                        }
                    )
                elif transition.count() > 1:
                    raise CosmicPipelineValidationError("Invalid state transition")
                transition = transition.first()
                passed, errors = check_restriction_rules(transition, instance)
                if not passed:
                    state_error = []
                    if len(errors) > 1:
                        _err = "Rules Failed :"
                    else:
                        _err = "Rule Failed :"
                    state_error.append(_err)
                    for role_id, error in errors.items():
                        state_error.append(f"{role_id} : {error}")
                    raise CosmicPipelineValidationError(
                        {field_name: CosmicPipelineValidationError(state_error)}
                    )
                post_save.connect(
                    partial(
                        post_state_change_handler,
                        previous_state=previous_state,
                        current_state=current_state,
                    ),
                    sender=sender,
                    dispatch_uid=f"post_state_change_{previous_state.name}_{current_state.name}",
                )
    else:
        return
