from wq.db.patterns import serializers as patterns
from .models import Nestedfk, Item, Nested


class ItemSerializer(patterns.AttachmentSerializer):
    class Meta(patterns.AttachmentSerializer.Meta):
        model = Item
        exclude = ("nestedfk",)
        object_field = "nestedfk"
        wq_config = {
            "initial": 3,
        }
        wq_field_config = {}


class NestedfkSerializer(patterns.AttachedModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Nestedfk
        fields = "__all__"
        wq_field_config = {}
        wq_fieldsets = {
            "": {"label": "General", "fields": ["name"]},
            "nested": {"label": "Nested", "fields": ["group"]},
        }
