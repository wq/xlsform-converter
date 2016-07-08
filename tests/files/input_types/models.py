from django.contrib.gis.db import models


class InputTypes(models.Model):
    int_field = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Integer field",
        help_text="Enter an integer number.",
    )
    dec_field = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Decimal field",
        help_text="Enter a decimal number.",
    )
    text_field = models.TextField(
        null=True,
        blank=True,
        verbose_name="Text field",
        help_text="Enter some text.",
    )
    char_field = models.CharField(
        max_length=5,
        null=True,
        blank=True,
        verbose_name="Char field",
        help_text="Enter some text.",
    )
    point_field = models.PointField(
        srid=4326,
        verbose_name="Point field",
        help_text="Enter a point.",
    )
    linestring_field = models.LineStringField(
        srid=4326,
        null=True,
        blank=True,
        verbose_name="Line string field",
        help_text="Enter a line.",
    )
    polygon_field = models.PolygonField(
        srid=4326,
        null=True,
        blank=True,
        verbose_name="Polygon field",
        help_text="Enter a polygon.",
    )
    date_field = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date field",
        help_text="Enter a date.",
    )
    time_field = models.TimeField(
        null=True,
        blank=True,
        verbose_name="Time field",
        help_text="Enter a time.",
    )
    datetime_field = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date+time field",
        help_text="Enter a date and a time.",
    )
    image_field = models.ImageField(
        upload_to="inputtypes",
        verbose_name="Image field",
        help_text="Add an image.",
    )
    audio_field = models.FileField(
        upload_to="inputtypes",
        null=True,
        blank=True,
        verbose_name="Audio field",
        help_text="Add an audio file.",
    )
    video_field = models.FileField(
        upload_to="inputtypes",
        null=True,
        blank=True,
        verbose_name="Video field",
        help_text="Add a video.",
    )

    class Meta:
        verbose_name = "input_types"
        verbose_name_plural = "inputtypes"
