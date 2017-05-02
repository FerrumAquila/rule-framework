__author__ = 'ironeagle'

# Package Imports
from redis import Redis


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


class DuplicateEntry(Exception):
    pass


class EmptyEntry(Exception):
    pass


class RedisEventHandler(object):

    def __init__(self, event):
        self.data = event.event_json
        from rule_framework.settings import redis_pool
        self.redis_conn = Redis(connection_pool=redis_pool)

    def get_key(self, key):
        return '%s_%s_%s' % (self._get_prefix('eventid', self.data['event_id']),
                             self._get_prefix('userid', self.data['userid']), key)

    def get_userid_key(self, key):
        return '%s_%s' % (self._get_prefix('userid', self.data['userid']), key)

    @staticmethod
    def _get_prefix(key, value):
        return '%s_%s' % (key, value)

    def get_db_value(self, key):
        return self.redis_conn.get(key)

    def entry_user_payment(self):
        total_amount = self.get_db_value(self.get_userid_key('total_amount'))
        if total_amount:
            total_amount = self.data['properties']['value'] + float(total_amount)
        else:
            total_amount = self.data['properties']['value']
        keys = (
            (self.get_key('amount'), self.data['properties']['value']),
            (self.get_key('ts'), self.data['ts']),
            (self.get_userid_key('total_amount'), total_amount),
        )
        for key in keys:
            self.redis_conn.set(key[0], key[1])
