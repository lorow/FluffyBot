import inspect
from collections import defaultdict
import cogs.core.utils.ErrorCodes as errorCodes


class EventHook(object):

    def __init__(self):
        self.events = defaultdict(list)

    def append_event(self, event: str):
        if event not in self.events:
            self.events[event] = []
            return self

    def append_listener(self, event: str, listener):
        if listener not in self.events[event]:
            self.append_event(event)

        if event in self.events.keys() and listener not in self.events[event]:
            self.events[event].append(listener)

        return self

    async def notify(self, name_of_the_event, *args, **keywargs):
        if len(self.events[name_of_the_event]) == 0:
            pass

        if self.events[name_of_the_event]:
            for listener in self.events[name_of_the_event]:
                if inspect.iscoroutinefunction(listener):
                    await listener(*args, **keywargs)
                else:
                    listener(*args, **keywargs)


def setup():
    return EventHook()
