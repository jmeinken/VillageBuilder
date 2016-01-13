# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='unsubscribe_code',
            field=models.CharField(max_length=60, null=True, blank=True),
        ),
    ]
