# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestcomment',
            name='complete',
        ),
        migrations.AlterField(
            model_name='request',
            name='complete',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='date',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='requestcomment',
            name='date',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
