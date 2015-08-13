# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_member_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent_on', models.DateTimeField(auto_now_add=True)),
                ('subject', models.CharField(max_length=60)),
                ('body', models.TextField()),
                ('viewed', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(related_name='received_set', to='account.Participant')),
                ('sender', models.ForeignKey(related_name='sent_set', to='account.Participant')),
            ],
        ),
    ]
