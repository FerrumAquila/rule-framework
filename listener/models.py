# App Imports
import json
import time

# Package Imports
from model_utils.models import TimeStampedModel
from aetos_serialiser.helpers import dict_reducer
from aetos_serialiser.serialisers import Serializer

# Django Imports
from django.db import models


class AetosModel(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    meta = models.TextField(default='{}')

    class Meta:
        abstract = True


class Event(AetosModel):
    user_id = models.BigIntegerField()
    source_time = models.DateTimeField()
    location = models.ForeignKey('Location', related_name='events', null=True, blank=True)
    noun = models.CharField(max_length=10)
    verb = models.CharField(max_length=10)
    time_spent = models.PositiveIntegerField()
    properties = models.TextField(default='{}')

    @classmethod
    def create_from_api(cls, json_data):
        class APIEventSerialiser(Serializer):
            BODY_MAP = {
                'user_id': ('userid', str),
                'source_time': ('ts', lambda x: "%s-%s-%s %s:%s:%s" % (x[:4], x[4:6], x[6:8], x[9:11], x[11:13], x[13:])),
                'location': ('__self___get_or_create_location', lambda x: x),
                'noun': ('noun', str),
                'verb': ('verb', str),
                'time_spent': ('timespent', int),
                'properties': ('properties', json.dumps),
                'meta': ('__self___get_meta', json.dumps)
            }
            REDUCER = dict_reducer

            @property
            def _get_or_create_location(self):
                lat_position, long_position = self.instance['latlong'].split(',')
                locations = Location.objects.filter(lat_position=lat_position, long_position=long_position)
                if locations:
                    location = locations.latest('id')
                else:
                    location = Location.create_from_api(self.instance)
                return location

            @property
            def _get_meta(self):
                return {'event_json': self.instance}

        instance = cls(**APIEventSerialiser(json_data).required_json)
        instance.save()
        return instance


class Location(AetosModel):
    name = models.CharField(max_length=64, blank=True, null=True)
    lat_position = models.DecimalField(max_digits=8, decimal_places=3)
    long_position = models.DecimalField(max_digits=8, decimal_places=3)

    @classmethod
    def create_from_api(cls, json_data):
        class APIEventLocationSerialiser(Serializer):
            BODY_MAP = {
                'name': ('__default__user_location_%s' % int(time.time()), str),
                'long_position': ('__self___get_long_position', float),
                'lat_position': ('__self___get_lat_position', float),
                'meta': ('__default__dict', str)
            }
            REDUCER = dict_reducer

            @property
            def _get_lat_position(self):
                return self.instance['latlong'].split(',')[0]

            @property
            def _get_long_position(self):
                return self.instance['latlong'].split(',')[1]

        instance = cls(**APIEventLocationSerialiser(json_data).required_json)
        instance.save()
        return instance
