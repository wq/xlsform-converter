from pyxform.xls2json import parse_file_to_json
from pyxform.question_type_dictionary import QUESTION_TYPE_DICT as QTYPES

GROUP_TYPES = ['group', 'repeat']


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
    return xform_json
