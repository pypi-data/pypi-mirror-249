from django.contrib import admin
from django.forms import BaseInlineFormSet

from .models.rules import (
    RestrictRuleCondition,
    ValidateRuleCondition,
)
from .models.transition import Transition
from .models.transitionstate import TransitionState
from .models.workflow import Workflow
from .forms import WorkFlowForm, RestrictRuleConditionAdminForm
class ChildModelInlineFormSet(BaseInlineFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs

class RestrictRuleConditionInlineAdmin(admin.TabularInline):
    model = RestrictRuleCondition
    extra = 0
    form = RestrictRuleConditionAdminForm
    formset = ChildModelInlineFormSet


class ValidationRuleAdmin(admin.TabularInline):
    model = ValidateRuleCondition
    extra = 0


class WorkflowAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    form = WorkFlowForm



class TransitionStateAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "description")
    list_filter = ("workflow",)


class TransitionAdmin(admin.ModelAdmin):
    list_display = ("workflow", "source_state", "destination_state")
    list_filter = ("workflow", "source_state", "destination_state")
    inlines = [RestrictRuleConditionInlineAdmin, ValidationRuleAdmin]
    def get_inline_instances(self, request, obj=None):
        """
        Show the inline only when editing an existing ParentModel object.
        """
        if obj:
            return super().get_inline_instances(request, obj)
        return []

class RestrictRuleConditionAdmin(admin.ModelAdmin):
    list_display = ("transition", "pk", "field", "operator", "value")
    list_display_links = ("pk",)
    list_filter = ("transition","transition__workflow",)
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

admin.site.register(Workflow, WorkflowAdmin)
admin.site.register(TransitionState, TransitionStateAdmin)
admin.site.register(Transition, TransitionAdmin)
admin.site.register(RestrictRuleCondition, RestrictRuleConditionAdmin)
