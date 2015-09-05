# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0003_auto_20150804_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmembership',
            name='invited',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='groupmembership',
            name='requested',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
