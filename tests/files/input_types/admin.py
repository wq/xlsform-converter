from django.contrib.gis import admin
from .models import InputTypes


admin.site.register(InputTypes, admin.GeoModelAdmin)
