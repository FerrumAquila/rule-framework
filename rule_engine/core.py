__author__ = 'ironeagle'


class Engine(object):

    EVENT_PREFIX = '_event_'

    def __init__(self, config=None):
        self.config = config or dict()
        self.json_data = dict()

    def trigger_event(self, event_name, json_data):
        self.json_data = json_data
        trigger_name = self.EVENT_PREFIX + event_name
        events = self.get_events()
        for event in events:
            if event.name == trigger_name:
                event.trigger(self)
        self.json_data = dict()

    @classmethod
    def get_events(cls):
        from types import FunctionType
        from collections import namedtuple

        Event = namedtuple('Event', 'name trigger')
        return [Event(name, method) for name, method in cls.__dict__.items()
                if type(method) == FunctionType and name.startswith(cls.EVENT_PREFIX)]

    def _event_first_bill_pay(self):
        print 'triggered "first_bill_pay"'
        print 'Config:'
        print self.config

    def _event_5_under_5_trans(self):
        print 'triggered "5_under_5_trans"'
        print 'Config:'
        print self.config

    def _event_no_feedback(self):
        print 'triggered "no_feedback"'
        print 'Config:'
        print self.config