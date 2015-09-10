# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20150909_2239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='group',
            name='phone_type',
        ),
    ]
