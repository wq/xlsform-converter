from django.db import models


class Nestedfk(models.Model):
    name = models.TextField(
        verbose_name="Name",
    )

    class Meta:
        verbose_name = "nestedfk"
        verbose_name_plural = "nestedfks"


class Item(models.Model):
    nestedfk = models.ForeignKey(
        Nestedfk,
        on_delete=models.CASCADE,
        related_name="items",
    )
    type = models.ForeignKey(
        "otherapp.Type",
        on_delete=models.CASCADE,
        verbose_name="Item Type",
    )
    name = models.TextField(
        verbose_name="Item Name",
    )
    photo = models.ImageField(
        upload_to="nestedfks",
        verbose_name="Photo",
    )

    class Meta:
        verbose_name = "item"
        verbose_name_plural = "items"


class Nested(models.Model):
    nestedfk = models.OneToOneField(
        Nestedfk,
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        "otherapp.Group",
        on_delete=models.CASCADE,
        verbose_name="Group",
    )

    class Meta:
        verbose_name = "nested"
        verbose_name_plural = "nesteds"
