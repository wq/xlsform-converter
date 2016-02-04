from pyxform.xls2json import parse_file_to_json
from pyxform.question_type_dictionary import QUESTION_TYPE_DICT as QTYPES

GROUP_TYPES = ['group', 'repeat']

WQ_EXTENSIONS = ["ForeignKey"]


def parse_xls(file_or_name):
    if isinstance(file_or_name, str):
        filename = file_or_name
        fileobj = None
    else:
        fileobj = file_or_name
        filename = fileobj.name
    xform_json = parse_file_to_json(filename, file_object=fileobj)
    for field in xform_json['children']:
        if field['type'] in GROUP_TYPES:
            continue
        if field['type'] not in QTYPES:
            raise Exception("Unknown field type: %s" % field['type'])
        else:
            field['type_info'] = QTYPES[field['type']]
            cons = field.get('bind', {}).get('constraint', '')
            if cons.startswith('wq:'):
                cons = cons[3:]
                for ext in WQ_EXTENSIONS:
                    if cons.startswith(ext + "(") and cons.endswith(")"):
                        field['wq:%s' % ext] = cons[len(ext) + 1:-1]
    return xform_json
