# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_member_last_emailed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='email_messages',
        ),
        migrations.AddField(
            model_name='member',
            name='email_pm',
            field=models.PositiveSmallIntegerField(default=2, choices=[(0, b'off'), (1, b'daily digest'), (2, b'immediately')]),
        ),
        migrations.AddField(
            model_name='member',
            name='email_request_comments',
            field=models.PositiveSmallIntegerField(default=1, choices=[(0, b'off'), (1, b'daily digest'), (2, b'immediately')]),
        ),
        migrations.AddField(
            model_name='member',
            name='email_requests',
            field=models.PositiveSmallIntegerField(default=2, choices=[(0, b'off'), (1, b'daily digest'), (2, b'immediately')]),
        ),
        migrations.AddField(
            model_name='member',
            name='email_shared_items',
            field=models.PositiveSmallIntegerField(default=1, choices=[(0, b'off'), (1, b'daily digest'), (2, b'immediately')]),
        ),
        migrations.AlterField(
            model_name='member',
            name='email_friend_requests',
            field=models.PositiveSmallIntegerField(default=2, choices=[(0, b'off'), (1, b'daily digest'), (2, b'immediately')]),
        ),
    ]
