# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0002_auto_20150912_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='more_data',
            field=models.TextField(null=True, blank=True),
        ),
    ]
