# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-28 11:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listener', '0002_auto_20170428_0637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='listener.Location'),
        ),
    ]