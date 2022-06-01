from enum import Enum

class select_filter_condition(Enum):
    equals = "equals"
    does_not_equal = "does_not_equal"
    is_empty = "is_empty"
    is_not_empty = "is_not_empty"


class checkbox_filter_condition(Enum):
    # checkbox
    equals = "equals"
    does_not_equal = "does_not_equal"


class text_filter_condition(Enum):
    # "title", "rich_text", "url", "email", and "phone_number"
    # Only return pages where the page property value matches the provided value exactly.
    equals = "equals"
    # Only return pages where the page property value does not match the provided value exactly.
    does_not_equal = "does_not_equal"
    # Only return pages where the page property value contains the provided value.
    contains = "contains"
    # Only return pages where the page property value does not contain the provided value.
    does_not_contain = "does_not_contain"
    # Only return pages where the page property value starts with the provided value.
    starts_with = "starts_with"
    # Only return pages where the page property value ends with the provided value.
    ends_with = "ends_with"
    # Only return pages where the page property value is empty.
    is_empty = "is_empty"
    # Only return pages where the page property value is present.
    is_not_empty = "is_not_empty"


class operator(Enum):
    AND = "and"
    OR = "or"


class TextColor(Enum):
    default = "default"
    gray = "gray"
    brown = "brown"
    orange = "orange"
    yellow = "yellow"
    green = "green"
    blue = "blue"
    purple = "purple"
    pink = "pink"
    red = "red"


class BackgroundColor(Enum):
    gray = "gray_background"
    brown = "brown_background"
    orange = "orange_background"
    yellow = "yellow_background"
    green = "green_background"
    blue = "blue_background"
    purple = "purple_background"
    pink = "pink_background"
    red = "red_background"
