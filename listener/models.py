# Package Imports
from model_utils.models import TimeStampedModel

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
    location = models.ForeignKey('Location', related_name='events')
    noun = models.ForeignKey('Noun', related_name='events')
    verb = models.ForeignKey('Verb', related_name='events')
    time_spend = models.PositiveIntegerField()


class Location(AetosModel):
    name = models.CharField(max_length=64, blank=True, null=True)
    long_position = models.DecimalField(max_digits=8, decimal_places=3)
    lat_position = models.DecimalField(max_digits=8, decimal_places=3)


class Noun(AetosModel):
    text = models.CharField(max_length=10)


class Verb(AetosModel):
    text = models.CharField(max_length=10)