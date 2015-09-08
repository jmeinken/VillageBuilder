# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent_on', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('body', models.TextField()),
                ('viewed', models.BooleanField(default=False, db_index=True)),
                ('recipient', models.ForeignKey(related_name='message_received_set', to='account.Participant')),
                ('sender', models.ForeignKey(related_name='message_sent_set', to='account.Participant')),
            ],
        ),
    ]
