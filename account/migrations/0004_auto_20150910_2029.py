# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20150910_0813'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='email_friend_requests',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='member',
            name='email_messages',
            field=models.BooleanField(default=True),
        ),
    ]
