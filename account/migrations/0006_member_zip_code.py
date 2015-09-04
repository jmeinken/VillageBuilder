# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20150902_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='zip_code',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
