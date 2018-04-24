from django.db import models
import pystache


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
    number = models.CharField(
        choices=(
            ("1", "One"),
            ("2", "Two"),
            ("3", "Three"),
            ("4", "Four"),
            ("5", "Five"),
            ("6", "Six"),
            ("7", "Seven"),
            ("8", "Eight"),
            ("9", "Nine"),
            ("10", "Ten"),
            ("11", "Eleven"),
        ),
        max_length=2,
        null=True,
        blank=True,
        verbose_name="Pick a number",
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
    site = models.ForeignKey(
        "other_app.Site",
        on_delete=models.CASCADE,
        verbose_name="Pick a Site ID",
    )

    wq_label_template = "{{color}} - {{number}}"

    def __str__(self):
        return pystache.render(self.wq_label_template, self)

    class Meta:
        verbose_name = "select"
        verbose_name_plural = "selects"
