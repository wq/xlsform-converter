from wq.db.patterns import serializers as patterns
from .models import Select


class SelectSerializer(patterns.AttachedModelSerializer):

    class Meta:
        model = Select
