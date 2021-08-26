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


class NestedSerializer(patterns.AttachmentSerializer):
    class Meta(patterns.AttachmentSerializer.Meta):
        model = Nested
        exclude = ("nestedfk",)
        object_field = "nestedfk"


class NestedfkSerializer(patterns.AttachedModelSerializer):
    items = ItemSerializer(many=True)
    nested = NestedSerializer(many=True)

    class Meta:
        model = Nestedfk
        fields = "__all__"
