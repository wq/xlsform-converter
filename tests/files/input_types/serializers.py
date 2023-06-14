from wq.db import rest
from .models import InputTypes


class InputTypesSerializer(rest.ModelSerializer):
    class Meta:
        model = InputTypes
        fields = "__all__"
        wq_field_config = {}
