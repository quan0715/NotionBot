from enum import Enum
from PyNotion.database.Property import PropertyBase
from datetime import datetime


class Data:
    class Type(str, Enum):
        date = "date"
        created_time = "created_time"
        last_edited_time = "last_edited_time"

    class Filter(str, Enum):
        equals = "equals"
        before = "before"
        after = "after"
        on_or_before = "on_or_before"
        is_empty = "is_empty"
        is_not_empty = "is_not_empty"
        on_or_after = "on_or_after"
        past_week = "past_week"
        past_month = "past_month"
        past_year = "past_year"
        next_week = "next_week"
        next_month = "next_month"
        next_year = "next_year"

    def __init__(self, start=None, end=None, time_zone=None):
        # get current datetime
        # today = datetime.now()
        # Get current ISO 8601 datetime in string format
        # iso_date = today.isoformat()
        self.start = start
        self.end = end
        self.time_zone = time_zone

        self.template = dict(
            start=Data.iso_format(self.start),
            end=Data.iso_format(self.end),
            time_zone=self.time_zone,
        )

    @staticmethod
    def iso_format(time):
        if isinstance(time, datetime):
            return time.isoformat()
        return time

    def make(self):
        return self.template


class DataProperty(PropertyBase):
    def __init__(self):
        super().__init__("date")


class DataValue(DataProperty):
    def __init__(self, key, value):
        super().__init__()
        self.value = value
        self.template = {key: {self.type: self.value.make()}}
