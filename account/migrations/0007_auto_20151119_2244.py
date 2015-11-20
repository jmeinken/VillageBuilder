# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20151014_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='email_friend_requests',
            field=models.PositiveSmallIntegerField(default=2, choices=[(0, b'no email'), (1, b'daily digest'), (2, b'immediate')]),
        ),
        migrations.AlterField(
            model_name='member',
            name='email_pm',
            field=models.PositiveSmallIntegerField(default=2, choices=[(0, b'no email'), (1, b'daily digest'), (2, b'immediate')]),
        ),
        migrations.AlterField(
            model_name='member',
            name='email_request_comments',
            field=models.PositiveSmallIntegerField(default=1, choices=[(0, b'no email'), (1, b'daily digest'), (2, b'immediate')]),
        ),
        migrations.AlterField(
            model_name='member',
            name='email_requests',
            field=models.PositiveSmallIntegerField(default=2, choices=[(0, b'no email'), (1, b'daily digest'), (2, b'immediate')]),
        ),
        migrations.AlterField(
            model_name='member',
            name='email_shared_items',
            field=models.PositiveSmallIntegerField(default=1, choices=[(0, b'no email'), (1, b'daily digest'), (2, b'immediate')]),
        ),
    ]
