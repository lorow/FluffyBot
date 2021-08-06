import inspect
from collections import defaultdict

from Core.Events.event import BaseEvent


class EventHook(object):
    def __init__(self):
        self.events = defaultdict(list)

    @staticmethod
    def _get_event_name(event: str or BaseEvent):
        """ A helper function for determining events name"""
        if type(event) == str:
            return event
        return event.event_name

    def append_event(self, event: str or BaseEvent):
        event_name = self._get_event_name(event)
        if event_name not in self.events:
            self.events[self._get_event_name(event_name)] = []

    def append_listener(self, event: str or BaseEvent, listener):
        event_name = self._get_event_name(event)
        if listener not in self.events[event_name]:
            self.append_event(event_name)

        if event_name in self.events.keys() and listener not in self.events[event_name]:
            self.events[event_name].append(listener)

    def remove_event(self, event: str or BaseEvent):
        event_name = self._get_event_name(event)
        if event_name in self.events:
            self.events.pop(event_name)

    def remove_listener(self, event: str or BaseEvent, listener):
        event_name = self._get_event_name(event)
        if event_name in self.events:
            if listener in self.events[event_name]:
                self.events[event_name].remove(listener)

    async def notify(self, event: str or BaseEvent, *args, **kwargs):
        event_name = self._get_event_name(event)
        if not len(self.events[event_name]):
            pass

        if self.events[event_name]:
            for listener in self.events[event_name]:
                if inspect.iscoroutinefunction(listener):
                    await listener(*args, **kwargs)
                else:
                    listener(*args, **kwargs)


def setup():
    return EventHook()
