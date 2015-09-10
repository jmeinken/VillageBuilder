# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='member',
            name='phone_type',
        ),
        migrations.RemoveField(
            model_name='member',
            name='share_phone',
        ),
    ]
