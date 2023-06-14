from wq.db import rest
from .models import Repeat, Item, Nested, Data


class ItemSerializer(rest.ModelSerializer):
    class Meta:
        model = Item
        exclude = ("repeat",)
        wq_field_config = {"count": {"control": {"appearance": "counter"}}}


class DataSerializer(rest.ModelSerializer):
    class Meta:
        model = Data
        exclude = ("repeat",)
        wq_field_config = {"value": {"control": {"appearance": "counter"}}}


class RepeatSerializer(rest.ModelSerializer):
    items = ItemSerializer(
        many=True,
        wq_config={
            "initial": 3,
        },
    )
    data = DataSerializer(
        many=True,
        wq_config={
            "initial": 3,
        },
    )

    class Meta:
        model = Repeat
        fields = "__all__"
        wq_field_config = {"count": {"control": {"appearance": "counter"}}}
        wq_fieldsets = {
            "": {"label": "General", "fields": ["name"]},
            "nested": {
                "label": "Nested",
                "control": {"appearance": "horizontal-view"},
                "fields": ["nested_name", "count"],
            },
        }
