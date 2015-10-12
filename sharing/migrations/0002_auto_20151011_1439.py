# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='facebook_date',
            field=models.DateTimeField(db_index=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='public',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
