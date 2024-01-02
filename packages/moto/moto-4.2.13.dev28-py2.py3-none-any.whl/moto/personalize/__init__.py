"""personalize module initialization; sets value for base decorator."""
from ..core.models import base_decorator
from .models import personalize_backends

mock_personalize = base_decorator(personalize_backends)
