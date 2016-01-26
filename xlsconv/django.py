from pyxform.xls2json import parse_file_to_json
from .renderer import render
from pkg_resources import resource_filename

default_template = resource_filename('xlsconv', 'templates/models.py')


GEO_TYPES = {'geopoint', 'geotrace', 'geoshape'}
FILE_TYPES = {'photo', 'video', 'audio', 'file'}

DJANGO_TYPES = {
    'integer': 'IntegerField',
    'text': 'TextField',
    'dateTime': 'DateTimeField',
    'date': 'DateField',
    'time': 'TimeField',

    'photo': 'ImageField',
    'video': 'FileField',
    'audio': 'FileField',
    'file': 'FileField',

    'geopoint': 'PointField',
    'geotrace': 'LineField',
    'geoshape': 'PolygonField',
}


def django_context(xform_json):
    context = {
        'form': xform_json,
        'fields': xform_json['children'],
    }

    # Additional variations on name/title for use in models.py
    class_name = context['form']['name']
    class_name = class_name.replace('_', ' ').title().replace(' ', '')
    plural = class_name.lower()
    if not plural.endswith('s'):
        plural += 's'
    context['form'].update(
        class_name=class_name,
        verbose_name=context['form']['title'].lower(),
        verbose_name_plural=plural,
        urlpath=plural,
    )

    # Django field types
    for field in context['fields']:
        field['field_name'] = field['name'].lower().replace('-', '_')
        field['type_is_%s' % field['type']] = True
        field['django_type'] = DJANGO_TYPES.get(
            field['type'], DJANGO_TYPES['text']
        )
        if field['type'] in FILE_TYPES:
            field['type_is_file'] = True
        if field['type'] in GEO_TYPES:
            context['form']['has_geo'] = True
            field['type_is_geo'] = True
    return context


def xls2django(filename, template_path=default_template):
    xform_json = parse_file_to_json(filename)
    context = django_context(xform_json)
    return render(context, template_path)


def main():
    import sys
    print(xls2django(*sys.argv[1:]))

if __name__ == '__main__':
    main()
