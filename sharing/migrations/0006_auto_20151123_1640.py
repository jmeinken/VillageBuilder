# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0005_auto_20151119_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='code',
            field=models.CharField(db_index=True, max_length=30, null=True, blank=True),
        ),
    ]
