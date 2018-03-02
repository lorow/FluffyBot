import inspect
from collections import defaultdict


class EmptyList(Exception):
    pass

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
        if(len(self.events[name_of_the_event]) == 0):
            raise EmptyList

        for listener in self.events[name_of_the_event]:
            if inspect.iscoroutinefunction(listener):
                await listener(*args, **keywargs)
            else:
                listener(*args, **keywargs)

    # decoratos for this sweet sweet sugar_syntax




class EventDispatcher(object):

    def __init__(self):
        self.event_handler = EventHook()
