# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='subject',
        ),
        migrations.AlterField(
            model_name='message',
            name='recipient',
            field=models.ForeignKey(related_name='message_received_set', to='account.Participant'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.ForeignKey(related_name='message_sent_set', to='account.Participant'),
        ),
        migrations.AlterField(
            model_name='message',
            name='sent_on',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='viewed',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
