from datetime import datetime
from dateutil.parser import parse
from abc import ABCMeta, abstractmethod, ABC
from collections.abc import Iterable

class DeadlinedMetaReminder(Iterable, metaclass=ABCMeta):

    @abstractmethod
    def is_due(self):
        pass

class DeadlinedReminder(ABC, Iterable):

    @abstractmethod
    def is_due(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is not DeadlinedReminder:
            return NotImplemented

        def attr_in_hierarchy(attr):
            return any (attr in SuperClass.__dict__ for SuperClass in subclass.__mro__)

        if not all(attr_in_hierarchy(attr) for attr in ('__iter__', 'is_due')):
            return NotImplemented

        return True

class DateReminder(DeadlinedReminder):

    def __init__(self, text, date):
        self.date = parse(date, dayfirst=True)
        self.text = text

    # override the abstractmethod from DeadlinedReminder class
    def is_due(self):
        return True if self.date <= datetime.now() else False

    def __iter__(self):
        return iter([self.text, self.date.isoformat()])
