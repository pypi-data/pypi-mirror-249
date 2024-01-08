import re
from typing import Optional, Literal
from pydantic import BaseModel


FD_EXPR = re.compile(r"^(\w+)(:(\w+)(\[([^\]]+)\])?)?(!?)$")
SUBTYPED_TYPES = {"ListField", "DictField", "ReferenceField"}
FieldType = Literal[
    "StringField",
    "IntField",
    "FloatField",
    "BoolField",
    "ListField",
    "DictField",
    "ReferenceField",
    "SelfReferenceField",
    "ObjectIdField",
    "DatetimeField",
]


class FieldDescriptor(BaseModel):
    name: str
    field_type: FieldType
    field_subtype: Optional[str] = None
    required: bool = False

    def render(self) -> str:
        args = {}
        decl = self.name
        if self.field_subtype:
            decl += f": {self.field_type}[{self.field_subtype}]"
        decl += f" = {self.field_type}("

        if self.field_type == "ReferenceField":
            args["reference_model"] = self.field_subtype
        if self.required:
            args["required"] = "True"

        if args:
            decl += ", ".join([f"{k}={v}" for k, v in args.items()])

        decl += ")"
        return decl


def parse_field_descriptor(fd: str) -> FieldDescriptor:
    match = FD_EXPR.findall(fd)
    if not match:
        raise ValueError(f'invalid field descriptor "{fd}"')

    tokens = match[0]

    fname, _, ftype, _, fsubtype, excl = tokens
    match ftype.lower():
        case "":
            field_type = "StringField"
        case "str" | "string" | "stringfield":
            field_type = "StringField"
        case "int" | "integer" | "integerfield":
            field_type = "IntField"
        case "bool" | "boolean" | "boolfield":
            field_type = "BoolField"
        case "float" | "floatfield":
            field_type = "FloatField"
        case "objid" | "objectid" | "objectidfield":
            field_type = "ObjectIdField"
        case "list" | "listfield":
            field_type = "ListField"
        case "dict" | "dictfield":
            field_type = "DictField"
        case "date" | "datetime" | "timestamp" | "ts" | "dt":
            field_type = "DatetimeField"
        case "ref" | "reference" | "referencefield":
            field_type = "ReferenceField"
        case "self" | "selfreference" | "selfreferencefield":
            field_type = "SelfReferenceField"
        case _:
            raise ValueError(f'unknown field type "{ftype}"')

    if fsubtype and field_type not in SUBTYPED_TYPES:
        raise ValueError(f"type {field_type} can't have subtypes")
    if not fsubtype and field_type == "ReferenceField":
        raise ValueError(f"type ReferenceField must have a subtype")

    required = False
    if excl:
        required = True

    return FieldDescriptor(
        name=fname,
        field_type=field_type,
        field_subtype=fsubtype or None,
        required=required,
    )
