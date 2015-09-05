# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='active',
            field=models.BooleanField(db_index=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='created',
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(db_index=True, max_length=30, choices=[(b'add friend', b'add friend')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='viewed',
            field=models.BooleanField(db_index=True),
        ),
    ]
