# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_member_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=120, db_index=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_admin',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='participant',
            name='type',
            field=models.CharField(db_index=True, max_length=6, choices=[(b'member', b'member'), (b'guest', b'guest'), (b'group', b'group')]),
        ),
    ]
