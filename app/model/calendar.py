from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import ClassVar

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_not_available_error
@dataclass
class Reminder:
    EMAIL: ClassVar[str] = "email"
    SYSTEM: ClassVar[str] = "system"
    date_time: datetime
    type: str = field(default=EMAIL)

    def _str_(self):
        return f"Reminder on {self.date_time} of type {self.type}"



# TODO: Implement Event class here
@dataclass
class Event:
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    reminders: list = field(default_factory=list)
    id: str = field(default_factory=generate_unique_id)

    def add_reminder(self, date_time, type_=None):
        if type_ is None:
            type_ = Reminder.EMAIL
        self.reminders.append(Reminder(date_time=date_time, type=type_))

    def delete_reminder(self, reminder_index):
        if 0 <= reminder_index < len(self.reminders):
            self.reminders.pop(reminder_index)
        else:
            reminder_not_found_error()

    def _str_(self):
        return f"ID: {self.id}\nEvent title: {self.title}\nDescription: {self.description}\nTime: {self.start_at} - {self.end_at}"


# TODO: Implement Day class here
@dataclass()
class Day:
    def _init(self, date):
        self.date_ = date_
        self.slots = {}
        self._init_slots()

    def _init_slots(self):
        for hour in range(24):
            for minute in range(0, 60, 15):
                slot = time(hour, minute)
                self.slots[slot] = None

