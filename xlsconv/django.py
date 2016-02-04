from .parser import parse_xls
from .renderer import render
from pkg_resources import resource_filename

default_template = resource_filename('xlsconv', 'templates/models.py-tpl')

DJANGO_TYPES = {
    # Map XForm field types to Django field types
    'barcode': False,
    'binary': 'FileField',
    'date': 'DateField',
    'dateTime': 'DateTimeField',
    'decimal': 'FloatField',
    'geopoint': 'PointField',
    'geoshape': 'PolygonField',
    'geotrace': 'LineStringField',
    'int': 'IntegerField',
    'select': 'CharField',
    'select1': 'CharField',
    'string': 'TextField',
    'time': 'TimeField',

    # Binary subtypes
    'image': 'ImageField',
}
IMAGE_SUBTYPES = ('image', 'photo', 'picture')


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
        if 'type_info' not in field or 'note' in field['type']:
            continue
        qtype = field['type_info']['bind']['type']
        if qtype == 'binary':
            for qt in IMAGE_SUBTYPES:
                if qt in field['type']:
                    qtype = 'image'
                    break

        if 'choices' in field:
            field['has_choices'] = True
            max_len = 0
            for choice in field['choices']:
                if len(choice['name']) > max_len:
                    max_len = len(choice['name'])
            field['max_len'] = max_len

        field['type_is_%s' % qtype] = True
        field['subtype_is_%s' % field['type']] = True
        field['field_name'] = field['name'].lower().replace('-', '_')
        if 'wq:ForeignKey' in field:
            field['django_type'] = "ForeignKey"
        elif 'wq:length' in field and qtype == "string":
            field['django_type'] = "CharField"
        else:
            field['django_type'] = DJANGO_TYPES[qtype]
        if qtype.startswith('geo'):
            context['form']['has_geo'] = True
            field['type_is_geo'] = True
    return context


def xls2django(file_or_name, template_path=default_template):
    xform_json = parse_xls(file_or_name)
    context = django_context(xform_json)
    return render(context, template_path)


def main():
    import sys
    print(xls2django(*sys.argv[1:]))

if __name__ == '__main__':
    main()
