from django.db import models


class Select(models.Model):
    color = models.CharField(
        choices=(
            ("red", "Red"),
            ("green", "Green"),
            ("blue", "Blue"),
        ),
        max_length=5,
        null=True,
        blank=True,
        verbose_name="Pick a color",
    )
    tags = models.CharField(
        choices=(
            ("cool", "Cool"),
            ("active", "Active"),
            ("recent", "Recent"),
        ),
        max_length=6,
        null=True,
        blank=True,
        verbose_name="Pick some tags",
    )

    class Meta:
        verbose_name = "select"
        verbose_name_plural = "selects"
