import os
from pyxform.xls2json import parse_file_to_json
from pyxform.question_type_dictionary import QUESTION_TYPE_DICT as QTYPES

GROUP_TYPES = ["group", "repeat"]

WQ_EXTENSIONS = ["ForeignKey", "length", "initial"]

IGNORE_FIELDS = ["meta", "__version__"]


def parse_xls(file_or_name):
    if isinstance(file_or_name, str):
        filename = file_or_name
        fileobj = None
    else:
        fileobj = file_or_name
        filename = fileobj.name
    xform_json = parse_file_to_json(
        filename,
        file_object=fileobj,
        default_name=os.path.splitext(os.path.basename(file_or_name))[0],
    )

    xform_json["children"] = [
        field
        for field in xform_json["children"]
        if field["name"] not in IGNORE_FIELDS
    ]

    def process_fields(root):
        for field in root["children"]:
            cons = field.get("bind", {}).get("constraint", "")
            if cons.startswith("wq:"):
                cons = cons[3:]
                for ext in WQ_EXTENSIONS:
                    if cons.startswith(ext + "(") and cons.endswith(")"):
                        field["wq:%s" % ext] = cons[len(ext) + 1 : -1]

            if field["type"] in GROUP_TYPES:
                process_fields(field)
                field["wq:nested"] = True
                if field["type"] == "repeat":
                    field["wq:many"] = True
                continue
            elif field["type"] in QTYPES:
                field["type_info"] = QTYPES[field["type"]]
            else:
                raise Exception("Unknown field type: %s" % field["type"])

    process_fields(xform_json)
    return xform_json


def generate_names(field_name, from_plural=False):
    class_name = field_name.replace("_", " ").title().replace(" ", "")
    plural_name = class_name.lower()
    if from_plural:
        if class_name.endswith("s"):
            class_name = class_name[:-1]
    else:
        if not plural_name.endswith("s"):
            plural_name += "s"

    return class_name, plural_name


def main():
    import sys
    import json

    print(
        json.dumps(
            parse_xls(*sys.argv[1:]),
            indent=4,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
