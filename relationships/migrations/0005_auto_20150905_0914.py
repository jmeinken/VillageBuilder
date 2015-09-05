# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0004_auto_20150905_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendship',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 5, 13, 13, 46, 13149, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 5, 13, 13, 50, 714635, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 5, 13, 13, 55, 832129, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guestfriendship',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 5, 13, 14, 0, 349999, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
