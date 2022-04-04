from wq.db.patterns import serializers as patterns
from .models import Repeat, Item, Nested, Data


class ItemSerializer(patterns.AttachmentSerializer):
    class Meta(patterns.AttachmentSerializer.Meta):
        model = Item
        exclude = ("repeat",)
        object_field = "repeat"
        wq_config = {
            "initial": 3,
        }
        wq_field_config = {"count": {"control": {"appearance": "counter"}}}


class DataSerializer(patterns.AttachmentSerializer):
    class Meta(patterns.AttachmentSerializer.Meta):
        model = Data
        exclude = ("repeat",)
        object_field = "repeat"
        wq_config = {
            "initial": 3,
        }
        wq_field_config = {"value": {"control": {"appearance": "counter"}}}


class RepeatSerializer(patterns.AttachedModelSerializer):
    items = ItemSerializer(many=True)
    data = DataSerializer(many=True)

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
