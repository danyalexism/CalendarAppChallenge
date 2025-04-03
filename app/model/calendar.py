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


class Calendar:
    def __init__(self):
        self.days: dict[date, Day] = {}
        self.events: dict[str, Event] = {}

    def add_event(self, title: str, description: str, date_: date, start_at: time, end_at: time) -> str:
        if date_ < datetime.now().date():
            date_lower_than_today_error()

        if date_ not in self.days:
            self.days[date_] = Day(date_)

        event = Event(title, description, date_, start_at, end_at)
        self.days[date_].add_event(event)
        self.events[event.id] = event

        return event.id

    def add_reminder(self, event_id: str, date_time: datetime, type_: str):
        if event_id not in self.events:
            event_not_found_error()

        self.events[event_id].add_reminder(date_time, type_)