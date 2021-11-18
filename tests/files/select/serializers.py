from wq.db.patterns import serializers as patterns
from .models import Select


class SelectSerializer(patterns.AttachedModelSerializer):
    class Meta:
        model = Select
        fields = "__all__"
        wq_field_config = {}
