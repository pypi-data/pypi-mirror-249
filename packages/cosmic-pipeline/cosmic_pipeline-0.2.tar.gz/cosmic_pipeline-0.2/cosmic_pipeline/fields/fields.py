from django.db.models import ForeignKey, CASCADE, BLANK_CHOICE_DASH,SET_NULL

from ..models.transitionstate import TransitionState


class StateField(ForeignKey):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        self.field_name = None
        kwargs["null"] = True
        kwargs["blank"] = True
        kwargs["to"] = "%s.%s" % (
            TransitionState._meta.app_label,
            TransitionState._meta.object_name,
        )
        kwargs["on_delete"] = kwargs.get("on_delete",SET_NULL )
        kwargs["related_name"] = "+"
        super(StateField, self).__init__(*args, **kwargs)

    def formfield(self, *, using=None, **kwargs):
        kwargs["queryset"] = TransitionState.objects.select_related("workflow").filter(
            workflow__workflow_model__app_label=self.model._meta.app_label,
            workflow__workflow_model__model=self.model._meta.object_name.lower(),
        )
        form = super().formfield(**kwargs)
        return form

    def get_choices(
        self,
        include_blank=True,
        blank_choice=BLANK_CHOICE_DASH,
        limit_choices_to=None,
        ordering=(),
    ):
        transition_state = TransitionState.objects.select_related("workflow").filter(
            workflow__workflow_model__app_label=self.model._meta.app_label,
            workflow__workflow_model__model=self.model._meta.object_name.lower(),
        )
        if include_blank:
            return BLANK_CHOICE_DASH + [
                (transition_state.id, transition_state.name)
                for transition_state in transition_state
            ]
        return [
            (transition_state.id, transition_state.name)
            for transition_state in transition_state
        ]
