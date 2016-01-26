{{#form.has_geo}}
from django.contrib.gis.db import models
{{/form.has_geo}}
{{^form.has_geo}}
from django.db import models
{{/form.has_geo}}


class {{form.class_name}}(models.Model):{{#fields}}{{#django_type}}
    {{field_name}} = models.{{django_type}}({{#type_is_binary}}
        upload_to="{{form.urlpath}}",{{/type_is_binary}}{{#type_is_image}}
        upload_to="{{form.urlpath}}",{{/type_is_image}}{{#type_is_geo}}
        srid=4326,{{/type_is_geo}}{{^bind.required}}
        null=True,
        blank=True,{{/bind.required}}{{#label}}
        verbose_name="{{label}}",{{/label}}{{#hint}}
        help_text="{{hint}}",{{/hint}}
    ){{/django_type}}{{/fields}}

    class Meta:
        verbose_name = "{{form.verbose_name}}"
        verbose_name_plural = "{{form.verbose_name_plural}}"
