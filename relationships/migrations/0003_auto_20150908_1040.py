# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0002_friendship_distance'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendship',
            name='distance_text',
            field=models.CharField(max_length=60, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='distance',
            field=models.IntegerField(),
        ),
    ]
