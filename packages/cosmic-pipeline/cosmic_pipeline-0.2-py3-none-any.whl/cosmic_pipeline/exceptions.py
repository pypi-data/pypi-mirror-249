from django.core.exceptions import ValidationError

class CosmicPipelineValidationError(ValidationError):
    pass