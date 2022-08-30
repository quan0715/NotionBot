from enum import Enum

# class Number:
#     class Type(str, Enum):
#         number = "number"
#
#     class Filter(str, Enum):
#         # "number"
#         # Only return pages where the page property value matches the provided value exactly.
#         equals = "equals"
#         # Only return pages where the page property value does not match the provided value exactly.
#         does_not_equal = "does_not_equal"
#         # Only return pages where the page property value is greater than the provided value.
#         greater_than = "greater_than"
#         # Only return pages where the page property value is less than the provided value.
#         less_than = "less_than"
#         # Only return pages where the page property value is greater than or equal to the provided value.
#         greater_than_or_equal_to = "greater_than_or_equal_to"
#         # Only return pages where the page property value is less than or equal to the provided value.
#         less_than_or_equal_to = "less_than_or_equal_to"
#         # Only return pages where the page property value is empty.
#         is_empty = "is_empty"
#         # Only return pages where the page property value is present.
#         is_not_empty = "is_not_empty"
#
#     class Format(str, Enum):
#         number = "number"
#         number_with_commas = "number_with_commas"
#         percent = "percent"
#         dollar = "dollar"
#         canadian_dollar = "canadian_dollar"
#         euro = "euro"
#         pound = "pound"
#         yen = "yen"
#         ruble = "ruble"
#         rupee = "rupee"
#         won = "won"
#         yuan = "yuan"
#         real = "real"
#         lira = "lira"
#         rupiah = "rupiah"
#         franc = "franc"
#         hong_kong_dollar = "hong_kong_dollar"
#         new_zealand_dollar = "new_zealand_dollar"
#         krona = "krona"
#         norwegian_krone = "norwegian_krone"
#         mexican_peso = "mexican_peso"
#         rand = "rand"
#         new_taiwan_dollar = "new_taiwan_dollar"
#         danish_krone = "danish_krone"
#         zloty = "zloty"
#         baht = "baht"
#         forint = "forint"
#         koruna = "koruna"
#         shekel = "shekel"
#         chilean_peso = "chilean_peso"
#         philippine_peso = "philippine_peso"
#         dirham = "dirham"
#         colombian_peso = "colombian_peso"
#         riyal = "riyal"
#         ringgit = "ringgit"
#         leu = "leu"
#         argentine_peso = "argentine_peso"
#         uruguayan_peso = "uruguayan_peso"

# class Data:
#     class Type(str, Enum):
#         date = "date"
#         created_time = "created_time"
#         last_edited_time = "last_edited_time"
#
#     class Filter(str, Enum):
#         equals = "equals"
#         before = "before"
#         after = "after"
#         on_or_before = "on_or_before"
#         is_empty = "is_empty"
#         is_not_empty = "is_not_empty"
#         on_or_after = "on_or_after"
#         past_week = "past_week"
#         past_month = "past_month"
#         past_year = "past_year"
#         next_week = "next_week"
#         next_month = "next_month"
#         next_year = "next_year"


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


# class Option:
#     class Type(str, Enum):
#         select = "select"
#         multi_select = "multi_select"
#
#     class Filter(str, Enum):
#         equals = "equals"
#         does_not_equal = "does_not_equal"
#         is_empty = "is_empty"
#         is_not_empty = "is_not_empty"





# class Sort:
#     class Direction(str, Enum):
#         asc = "ascending"
#         dec = "descending"
#
#     class Timestamp(str, Enum):
#         created_time = "created_time"
#         last_edited_time = "last_edited_time"
#








