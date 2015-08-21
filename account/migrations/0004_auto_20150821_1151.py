# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_member_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='share_street',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='share_email',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='street',
            field=models.CharField(max_length=60, null=True, blank=True),
        ),
    ]
