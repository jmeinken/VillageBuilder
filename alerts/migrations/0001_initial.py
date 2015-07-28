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
                ('event_type', models.CharField(max_length=30, choices=[(b'add friend', b'add friend')])),
                ('viewed', models.BooleanField()),
                ('active', models.BooleanField()),
                ('created', models.DateField(auto_now_add=True)),
                ('event_data', models.TextField(null=True, blank=True)),
                ('affected_participant', models.ForeignKey(to='account.Participant')),
            ],
        ),
    ]
