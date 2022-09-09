from enum import Enum


class People:
    class Type(str, Enum):
        people = "people"
        created_by = "created_by"
        last_edited_by = "last_edited_by"

    class Filter(str, Enum):
        contains = "contains"
        does_not_contain = "does_not_contain"
        is_empty = "is_empty"
        is_not_empty = "is_not_empty"


class PropertyType(str, Enum):
    number = "number"
    title = "title"
    rich_text = "rich_text"
    select = "select"
    multi_select = "multi_select"
    date = "date"
    people = "people"
    files = "files"
    checkbox = "checkbox"
    url = "url"
    email = "email"
    phone_number = "phone_number"
    formula = "formula"
    relation = "relation"
    rollup = "rollup"
    created_time = "created_time"
    created_by = "created_by"
    last_edited_time = "last_edited_time"
    last_edited_by = "last_edited_by"








