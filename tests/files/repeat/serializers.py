from wq.db.patterns import serializers as patterns
from .models import Repeat, Item, Nested


class ItemSerializer(patterns.AttachmentSerializer):
    class Meta(patterns.AttachmentSerializer.Meta):
        model = Item
        exclude = ('repeat',)
        object_field = 'repeat'
        wq_config = {
            'initial': 3,
        }


class NestedSerializer(patterns.AttachmentSerializer):
    class Meta(patterns.AttachmentSerializer.Meta):
        model = Nested
        exclude = ('repeat',)
        object_field = 'repeat'


class RepeatSerializer(patterns.AttachedModelSerializer):
    items = ItemSerializer(many=True)
    nested = NestedSerializer(many=True)

    class Meta:
        model = Repeat
