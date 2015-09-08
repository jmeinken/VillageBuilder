# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_type', models.CharField(db_index=True, max_length=30, choices=[(b'add friend', b'add friend')])),
                ('viewed', models.BooleanField(db_index=True)),
                ('active', models.BooleanField(db_index=True)),
                ('created', models.DateField(auto_now_add=True, db_index=True)),
                ('event_data', models.TextField(null=True, blank=True)),
                ('affected_participant', models.ForeignKey(to='account.Participant')),
            ],
        ),
    ]
