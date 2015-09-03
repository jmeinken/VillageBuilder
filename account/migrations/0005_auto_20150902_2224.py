# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20150821_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='state',
            field=models.CharField(max_length=2, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='member',
            name='state',
            field=models.CharField(max_length=2, null=True, blank=True),
        ),
    ]
