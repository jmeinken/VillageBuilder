# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_group_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='code',
            field=models.CharField(max_length=60, null=True, blank=True),
        ),
    ]
