from .parser import parse_xls, generate_names
from .renderer import render
from .ast import (
    ast_module,
    ast_import,
    ast_assign,
    ast_expr,
    ast_call,
    ast_name,
    ast_args,
    ast_keywords,
    ast_class,
    ast_def,
    ast_return,
    ast_trailing_comma,
    ast_newline,
    ast_comment,
    ast_dict,
    ast_list,
    ast_tuple,
    unparse,
)
import black


TEMPLATES = {
    "admin": lambda node: node.as_admin(),
    "models": lambda node: node.as_models(),
    "rest": lambda node: node.as_rest(),
    "wizard": lambda node: node.as_wizard(),
    "serializers": lambda node: node.as_serializers(),
}
TEMPLATE_NAMES = list(TEMPLATES.keys())
DEFAULT_TEMPLATE = "models"

DJANGO_TYPES = {
    # Map XForm field types to Django field types
    "barcode": False,
    "binary": "FileField",
    "date": "DateField",
    "dateTime": "DateTimeField",
    "decimal": "FloatField",
    "geopoint": "PointField",
    "geoshape": "PolygonField",
    "geotrace": "LineStringField",
    "int": "IntegerField",
    "select": "CharField",
    "select1": "CharField",
    "string": "TextField",
    "time": "TimeField",
    # Binary subtypes
    "image": "ImageField",
}
IMAGE_SUBTYPES = ("image", "photo", "picture")


class Node:
    def __init__(self, name, parent=None, children=None, **kwargs):
        if parent and parent.parent and not parent.config.get('wq:many'):
            if name in parent.parent.reserved:
                name = f'{parent.name}_{name}'
                if name in parent.parent.reserved:
                    raise Exception(f"{name} is not unique")
                parent.parent.reserved.add(name)

        self.name = name
        self.class_name = kwargs.get("class_name", None)
        self.label = kwargs.get("label", None)
        self.appearance = kwargs.get("control", {}).get("appearance", None)
        self.config = kwargs
        self.parent = parent
        self.reserved = set(
            child['name'] for child in children or []
            if not child.get('children')
        )
        if children:
            self.children = [Node(parent=self, **child) for child in children]
        else:
            self.children = None

    @property
    def root(self):
        node = self
        while node.parent:
            node = node.parent
        return node

    @property
    def models(self):
        models = [self.class_name]
        for field in self.children:
            if field.children:
                models += field.models
        return models

    def as_admin(self):
        module = "django.contrib"
        register_args = [ast_name(self.class_name)]
        if self.config.get("has_geo"):
            module = "django.contrib.gis"
            register_args.append(ast_name("admin.GeoModelAdmin"))

        return ast_module(
            ast_import(module, "admin"),
            ast_import(".models", self.class_name),
            ast_newline(),
            ast_newline(),
            ast_expr(ast_call("admin.site.register", *register_args)),
        )

    def as_models(self):
        module = "django.db"
        label_template = self.config.get("label_template")
        if self.config.get("has_geo"):
            module = "django.contrib.gis.db"

        return ast_module(
            ast_import(module, "models"),
            ast_import("pystache") if label_template else None,
            *self.as_model(label_template),
        )

    def as_model(self, label_template=None):
        fields = []
        if self.parent:
            assert self.config.get("wq:many")
            conf = {
                "name": self.parent.name,
                "bind": {"required": True},
                "wq:ForeignKey": ast_name(self.parent.class_name),
                "django_type": "ForeignKey",
                "related_name": self.config.get("verbose_name_plural"),
            }
            fields.append(Node(**conf).as_field())

        for child in self.children:
            if child.children and not child.config.get('wq:many'):
                fields += child.as_fields()
            else:
                fields.append(child.as_field())

        if label_template:
            str_def = [
                ast_newline(),
                ast_assign("wq_label_template", label_template),
                ast_def(
                    "__str__",
                    ["self"],
                    ast_return(
                        ast_call(
                            "pystache.render",
                            ast_name("self.wq_label_template"),
                            ast_name("self"),
                        )
                    ),
                ),
            ]
        else:
            str_def = []

        nested_models = []
        for field in self.children:
            if field.children and field.config.get('wq:many'):
                nested_models.append(field.as_model())

        return [
            ast_class(
                self.class_name,
                ["models.Model"],
                *fields,
                *str_def,
                ast_class(
                    "Meta",
                    [],
                    ast_assign("verbose_name", self.config["verbose_name"]),
                    ast_assign(
                        "verbose_name_plural",
                        self.config["verbose_name_plural"],
                    ),
                ),
            ),
            *nested_models,
        ]

    def as_field(self):
        django_type = self.config.get("django_type")
        if not django_type:
            return None
        args = []
        kwargs = {}

        if self.config.get("wq:ForeignKey"):
            fkname = self.config["wq:ForeignKey"]
            if isinstance(fkname, str):
                fkname = fkname.strip("\"'")
            args.append(fkname)
            kwargs.update(
                on_delete=ast_name("models.CASCADE"),
            )
            if self.config.get("related_name"):
                kwargs.update(related_name=self.config["related_name"])

        if self.config.get("has_choices"):
            kwargs.update(
                choices=ast_tuple(
                    (choice["name"], choice["label"])
                    for choice in self.config["choices"]
                )
            )

        if self.config.get("type_is_geo"):
            kwargs.update(srid=4326)

        if self.config.get("type_is_binary"):
            kwargs.update(upload_to=self.root.config.get("urlpath"))

        max_length = self.config.get("max_len", self.config.get("wq:length"))
        if max_length:
            kwargs.update(
                max_length=int(max_length),
            )

        if not self.config.get("bind", {}).get("required"):
            kwargs.update(
                null=True,
                blank=True,
            )

        if self.config.get("label"):
            kwargs.update(
                verbose_name=self.config["label"],
            )
        if self.config.get("hint"):
            kwargs.update(
                help_text=self.config["hint"],
            )
        return ast_assign(
            self.name,
            ast_call(f"models.{django_type}", comma=True, *args, **kwargs),
        )

    def as_fields(self):
        assert self.children and not self.config.get('wq:many')
        return [
            ast_newline(),
            ast_newline(),
            ast_comment(self.config.get('label') or self.name),
        ] + [
            child.as_field() for child in self.children
        ] + [
            ast_newline(),
        ]

    def as_rest(self):
        kwargs = {}

        if self.config.get("has_nested"):
            serializer = f"{self.class_name}Serializer"
            kwargs.update(serializer=ast_name(serializer))
        else:
            serializer = None

        kwargs.update(
            fields="__all__",
            cache="first_page",
            background_sync=True,
        )

        if self.config.get("has_geo"):
            kwargs.update(
                map=ast_list(
                    [
                        ast_dict(
                            {
                                "mode": "list",
                                "autoLayers": True,
                                "layers": [],
                            }
                        ),
                        ast_dict(
                            {
                                "mode": "detail",
                                "autoLayers": True,
                                "layers": [],
                            }
                        ),
                        ast_dict(
                            {
                                "mode": "edit",
                                "autoLayers": True,
                                "layers": [],
                            }
                        ),
                    ]
                )
            )

        return ast_module(
            ast_import("wq.db", "rest"),
            ast_import(".models", self.class_name),
            ast_import(".serializers", serializer) if serializer else None,
            ast_newline(),
            ast_newline(),
            ast_expr(
                ast_call(
                    "rest.router.register_model",
                    ast_name(self.class_name),
                    **kwargs,
                )
            ),
        )

    def as_wizard(self):
        if self.config.get("has_nested"):
            serializer = f"{self.class_name}Serializer"
            args = [self.name, ast_name(serializer)]
        else:
            serializer = None
            args = [ast_name(self.class_name)]

        return ast_module(
            ast_import("data_wizard"),
            ast_import(".models", self.class_name),
            ast_import(".serializers", serializer) if serializer else None,
            ast_newline(),
            ast_newline(),
            ast_expr(
                ast_call("data_wizard.register", *args)
            ),
        )

    def as_serializers(self):
        serializers = self.as_serializer()
        return ast_module(
            ast_import("wq.db.patterns", "serializers", "patterns"),
            ast_import(".models", self.models),
            *serializers,
        )

    def as_serializer(self):
        nested_serializers = []
        nested_fields = []
        wq_field_config = {}
        wq_fieldsets = {}
        root_fields = []
        for field in self.children:
            if field.children:
                if field.config.get('wq:many'):
                    nested_serializers += field.as_serializer()
                    nested_fields.append(
                        ast_assign(
                            field.name,
                            ast_call(
                                f"{field.class_name}Serializer",
                                many=True,
                            ),
                        )
                    )
                else:
                    fieldset = {
                        'label': field.config.get('label'),
                    }
                    if field.appearance:
                        fieldset['control'] = {'appearance': field.appearance}
                    fieldset['fields'] = [
                        child.name for child in field.children
                    ]
                    for child in field.children:
                        if child.appearance:
                            wq_field_config[
                                child.name
                            ] = child.as_wq_field_config()
                    wq_fieldsets[field.name] = fieldset
            else:
                root_fields.append(field.name)
                if field.appearance:
                    wq_field_config[
                        field.name
                    ] = field.as_wq_field_config()

        if wq_fieldsets:
            wq_fieldsets = {
                '': {
                    'label': 'General',
                    'fields': root_fields,
                },
                **wq_fieldsets
            }
        else:
            wq_fieldsets = None

        return [
            *nested_serializers,
            ast_class(
                f"{self.class_name}Serializer",
                [
                    "patterns.AttachmentSerializer"
                    if self.parent
                    else "patterns.AttachedModelSerializer"
                ],
                *nested_fields,
                ast_class(
                    "Meta",
                    ["patterns.AttachmentSerializer.Meta"],
                    ast_assign("model", ast_name(self.class_name)),
                    ast_assign("exclude", (self.parent.name,)),
                    ast_assign("object_field", self.parent.name),
                    ast_assign("wq_config", ast_dict(initial=3))
                    if self.config.get("wq:many")
                    else None,
                    ast_assign("wq_field_config", wq_field_config),
                    ast_assign("wq_fieldsets", wq_fieldsets),
                )
                if self.parent
                else ast_class(
                    "Meta",
                    [],
                    ast_assign("model", ast_name(self.class_name)),
                    ast_assign("fields", "__all__"),
                    ast_assign("wq_field_config", wq_field_config),
                    ast_assign("wq_fieldsets", wq_fieldsets),
                ),
            ),
        ]

    def as_wq_field_config(self):
        return {
            'control': {
                'appearance': self.appearance,
            }
        }


def django_context(xform_json):
    context = {
        "form": xform_json,
        "fields": xform_json["children"],
    }

    # Additional variations on name/title for use in models.py
    class_name, plural_name = generate_names(context["form"]["name"])
    context["form"].update(
        class_name=class_name,
        field_name=class_name.lower(),
        verbose_name=context["form"]["title"].lower(),
        verbose_name_plural=plural_name,
        urlpath=plural_name,
    )

    instance_name = context["form"].get("instance_name", "").strip()
    if instance_name.startswith("concat(") and instance_name.endswith(")"):
        label_template = ""
        for part in instance_name[7:-1].split(","):
            part = part.strip()
            if part.startswith("${") and part.endswith("}"):
                part = part.replace("${", "{{").replace("}", "}}")
            elif part[0] in ('"', "'") and part[-1] in ('"', "'"):
                part = part[1:-1]
            label_template += part
        context["form"]["label_template"] = label_template

    def process_fields(fields):
        # Django field types
        for field in fields:
            if field.get("wq:nested", False):
                process_fields(field["children"])
                class_name, plural_name = generate_names(
                    field["name"], from_plural=True
                )
                field.update(
                    class_name=class_name,
                    verbose_name=class_name.lower(),
                    verbose_name_plural=plural_name,
                )
                context["form"]["has_nested"] = True
                continue
            if "type_info" not in field or "note" in field["type"]:
                continue

            if "choices" in field:
                field["has_choices"] = True
                max_len = 0
                for choice in field["choices"]:
                    if len(choice["name"]) > max_len:
                        max_len = len(choice["name"])
                field["max_len"] = max_len

            if field["type"] in ("select1", "select one"):
                qtype = "select1"
            elif field["type"].startswith("select"):
                qtype = "select"
            else:
                qtype = field["type_info"]["bind"]["type"]

            field["type_is_%s" % qtype] = True
            field["subtype_is_%s" % field["type"]] = True
            field["field_name"] = field["name"].lower().replace("-", "_")

            if "wq:ForeignKey" in field:
                field["django_type"] = "ForeignKey"
            elif "wq:length" in field and qtype == "string":
                field["django_type"] = "CharField"
            elif qtype == "binary":
                field["django_type"] = DJANGO_TYPES["binary"]
                for qt in IMAGE_SUBTYPES:
                    if qt in field["type"]:
                        field["django_type"] = DJANGO_TYPES["image"]
            else:
                field["django_type"] = DJANGO_TYPES[qtype]

            if qtype.startswith("geo"):
                context["form"]["has_geo"] = True
                field["type_is_geo"] = True

    process_fields(context["fields"])
    return context


def xls2django(file_or_name, template_name=DEFAULT_TEMPLATE):
    xform_json = parse_xls(file_or_name)
    context = django_context(xform_json)
    transform = TEMPLATES.get(template_name)

    if transform:
        tree = transform(Node(**context["form"]))
        code = unparse(tree)
    else:
        code = render(context, template_name)

    return black.format_str(code, mode=black.FileMode())


def main():
    import sys

    print(xls2django(*sys.argv[1:]))


if __name__ == "__main__":
    main()
