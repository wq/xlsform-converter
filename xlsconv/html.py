from .parser import parse_xls, generate_names
from .renderer import render
from pkg_resources import resource_filename

default_template = resource_filename('xlsconv', 'templates/form.html')

HTML5_INPUT_TYPES = {
    # Map XForm field types to <input type>
    'barcode': False,
    'binary': 'file',
    'date': 'date',
    'dateTime': 'datetime-local',
    'decimal': 'number',
    'geopoint': False,
    'geoshape': False,
    'geotrace': False,
    'int': 'number',
    'select': False,
    'select1': False,
    'string': 'text',
    'time': 'time',

    # String subtypes
    'email': 'email',
    'phone': 'tel',
    'text': False,
    'note': False,
}
STRING_SUBTYPES = ['email', 'phone', 'text', 'note']


def html_context(xform_json):
    context = {
        'form': xform_json,
        'fields': xform_json['children'],
    }
    urlpath = context['form']['name'].replace('_', '')
    if not urlpath.endswith('s'):
        urlpath += 's'
    context['form']['urlpath'] = urlpath

    # HTML5 field types
    def process_fields(fields, prefix=None):
        for field in fields:
            if 'wq:ForeignKey' in field:
                field['real_name'] = field['name']
                field['name'] = field['name'] + '_id'
            field['field_name'] = field['name']
            if prefix:
                field['field_formname'] = '%s[%s][%s]' % (
                    prefix, "{{@index}}", field['name'],
                )
                field['field_id'] = '%s-%s-%s' % (
                    prefix, "{{@index}}", field['name'],
                )
            else:
                field['field_formname'] = field['name']
                field['field_id'] = field['name']

            if field.get('wq:nested', False):
                class_name, plural_name = generate_names(
                    field['name'],
                    from_plural=True
                )
                field['plural_name'] = plural_name
                process_fields(field['children'], plural_name)
                continue
            if 'type_info' not in field:
                continue
            qtype = field['type_info']['bind']['type']
            if qtype == 'string':
                for qt in STRING_SUBTYPES:
                    if qt in field['type']:
                        qtype = qt
                        break
            field['type_is_%s' % qtype] = True
            field['html5_type'] = HTML5_INPUT_TYPES[qtype]
            field['subtype_is_%s' % field['type']] = True
            if qtype.startswith('geo'):
                field['type_is_geo'] = True
                context['form']['has_geo'] = True
            if qtype == 'dateTime' or 'wq:ForeignKey' in field:
                field['has_label'] = True
            if 'choices' in field:
                field['has_label'] = True
                for num in range(1, 21):
                    if len(field['choices']) > num:
                        field['more_than_%s_choices' % num] = True

    process_fields(context['fields'])
    return context


def xls2html(file_or_name, template_path=default_template):
    xform_json = parse_xls(file_or_name)
    context = html_context(xform_json)
    return render(context, template_path)


def main():
    import sys
    print(xls2html(*sys.argv[1:]))

if __name__ == '__main__':
    main()
