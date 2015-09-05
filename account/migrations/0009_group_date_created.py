# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20150905_0159'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 5, 13, 11, 29, 963097, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
