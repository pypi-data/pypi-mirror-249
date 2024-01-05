from django import forms

from .choices import model_fields_choices
from .check import check_operations
from .exceptions import CosmicPipelineValidationError
from .models.rules import RestrictRuleCondition
from .models.workflow import Workflow, get_workflow_choices


class WorkFlowForm(forms.ModelForm):
    class Meta:
        model = Workflow
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["workflow_model"].choices = get_workflow_choices()


class RestrictRuleConditionAdminForm(forms.ModelForm):
    class Meta:
        model = RestrictRuleCondition
        fields = "__all__"

    def __init__(self, *args, parent_object, **kwargs):
        self.parent_object = parent_object
        super().__init__(*args, **kwargs)
        widget = forms.Select(
            choices=model_fields_choices(
                self.parent_object.workflow.workflow_model.model_class()
            )
        )
        self.fields["field"].widget = widget

    def clean_operator(self):
        operator = self.cleaned_data["operator"]
        annotate = self.cleaned_data["annotate"]
        transition = self.parent_object.workflow.workflow_model.model_class()
        field = self.cleaned_data["field"]
        is_valid = check_operations(transition, field, operator,annotate)
        if not is_valid:
            raise CosmicPipelineValidationError(
                f"Invalid operator for {field}", code="invalid_operator"
            )
        return self.cleaned_data["operator"]
