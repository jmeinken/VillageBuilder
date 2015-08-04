# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('relationships', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('request_sent_to_group', models.BooleanField(default=False)),
                ('request_received_from_group', models.BooleanField(default=False)),
                ('group', models.ForeignKey(to='account.Group')),
                ('member', models.ForeignKey(to='account.Member')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='groupmembership',
            unique_together=set([('group', 'member')]),
        ),
    ]
