from wq.db import rest
from .models import Nestedfk, Item, Nested


class ItemSerializer(rest.ModelSerializer):
    class Meta:
        model = Item
        exclude = ("nestedfk",)
        wq_field_config = {}


class NestedfkSerializer(rest.ModelSerializer):
    items = ItemSerializer(
        many=True,
        wq_config={
            "initial": 3,
        },
    )

    class Meta:
        model = Nestedfk
        fields = "__all__"
        wq_field_config = {}
        wq_fieldsets = {
            "": {"label": "General", "fields": ["name"]},
            "nested": {"label": "Nested", "fields": ["group"]},
        }
