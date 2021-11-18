from django.db import models


class Repeat(models.Model):
    name = models.TextField(
        verbose_name="Name",
    )

    # Nested
    nested_name = models.TextField(
        verbose_name="Name",
    )
    count = models.IntegerField(
        verbose_name="Count",
    )

    class Meta:
        verbose_name = "repeat"
        verbose_name_plural = "repeats"


class Item(models.Model):
    repeat = models.ForeignKey(
        Repeat,
        on_delete=models.CASCADE,
        related_name="items",
    )
    name = models.TextField(
        verbose_name="Item Name",
    )
    count = models.IntegerField(
        verbose_name="Item Count",
    )

    class Meta:
        verbose_name = "item"
        verbose_name_plural = "items"
