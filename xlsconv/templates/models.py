{{#form.has_geo}}
from django.contrib.gis.db import models
{{/form.has_geo}}
{{^form.has_geo}}
from django.db import models
{{/form.has_geo}}


class {{form.class_name}}(models.Model):{{#fields}}{{^type_is_note}}
    {{field_name}} = models.{{django_type}}({{#type_is_file}}
        upload_to="{{form.urlpath}}",{{/type_is_file}}{{#type_is_geo}}
        srid=4326,{{/type_is_geo}}{{^bind.required}}
        null=True,
        blank=True,{{/bind.required}}{{#label}}
        verbose_name="{{label}}",{{/label}}{{#hint}}
        help_text="{{hint}}",{{/hint}}
    ){{/type_is_note}}{{/fields}}

    class Meta:
        verbose_name = "{{form.verbose_name}}"
        verbose_name_plural = "{{form.verbose_name_plural}}"
