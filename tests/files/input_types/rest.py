from wq.db import rest
from .models import InputTypes


rest.router.register_model(
    InputTypes,
    map={
        'list': {
            'autoLayers': True,
            'layers': [],
        },
        'detail': {
            'autoLayers': True,
            'layers': [],
        },
        'edit': {
            'layers': [{
                'type': 'geojson',
                'name': 'point_field',
                'url': 'inputtypes/{{id}}/edit.geojson',
                'draw': {
                    'circle': False,
                    'marker': {},
                    'polyline': False,
                    'polygon': False,
                    'rectangle': False,
                },
                'geometryField': 'point_field',
                'flatten': True,
            }],
            'layers': [{
                'type': 'geojson',
                'name': 'linestring_field',
                'url': 'inputtypes/{{id}}/edit.geojson',
                'draw': {
                    'circle': False,
                    'marker': False,
                    'polyline': {},
                    'polygon': False,
                    'rectangle': False,
                },
                'geometryField': 'linestring_field',
                'flatten': True,
            }],
            'layers': [{
                'type': 'geojson',
                'name': 'polygon_field',
                'url': 'inputtypes/{{id}}/edit.geojson',
                'draw': {
                    'circle': False,
                    'marker': False,
                    'polyline': False,
                    'polygon': {},
                    'rectangle': {},
                },
                'geometryField': 'polygon_field',
                'flatten': True,
            }],
        },
    },
)
