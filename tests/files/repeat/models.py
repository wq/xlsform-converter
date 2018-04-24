from django.db import models


class Repeat(models.Model):
    name = models.TextField(
        verbose_name="Name",
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


class Nested(models.Model):
    repeat = models.OneToOneField(
        Repeat,
        on_delete=models.CASCADE,
    )
    name = models.TextField(
        verbose_name="Name",
    )

    class Meta:
        verbose_name = "nested"
        verbose_name_plural = "nesteds"
