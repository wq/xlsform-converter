from wq.db import rest
from .models import Select


class SelectSerializer(rest.ModelSerializer):
    class Meta:
        model = Select
        fields = "__all__"
        wq_field_config = {}
