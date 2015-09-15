# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20150910_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='last_emailed',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 14, 21, 13, 40, 676849, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
