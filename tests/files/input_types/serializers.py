from wq.db.patterns import serializers as patterns
from .models import InputTypes


class InputTypesSerializer(patterns.AttachedModelSerializer):

    class Meta:
        model = InputTypes
        fields = "__all__"
