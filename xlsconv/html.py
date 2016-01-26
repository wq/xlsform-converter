from pyxform.xls2json import parse_file_to_json
from .renderer import render
from pkg_resources import resource_filename

default_template = resource_filename('xlsconv', 'templates/form.html')


HTML5_TYPES = {
    'date': 'date',
    'time': 'time',
    'datetime': 'datetime',
    'phonenumber': 'tel',
    'integer': 'number',
    'decimal': 'number',

    'photo': 'file',
    'audio': 'file',
    'video': 'file',
}
OTHER_TYPES = ['text', 'note']


def html_context(xform_json):
    context = {
        'form': xform_json,
        'fields': xform_json['children'],
    }

    # HTML5 field types
    for field in context['fields']:
        field['type_is_%s' % field['type']] = True
        if field['type'] in HTML5_TYPES:
            field['html5_type'] = HTML5_TYPES[field['type']]
        elif field['type'] not in OTHER_TYPES:
            field['type_is_unknown'] = True
    return context


def xls2html(filename, template_path=default_template):
    xform_json = parse_file_to_json(filename)
    context = html_context(xform_json)
    return render(context, template_path)


def main():
    import sys
    print(xls2html(*sys.argv[1:]))

if __name__ == '__main__':
    main()
