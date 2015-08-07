# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_group_private'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('complete', models.BooleanField(default=False)),
                ('member', models.ForeignKey(to='account.Member')),
            ],
        ),
        migrations.CreateModel(
            name='RequestComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('body', models.TextField()),
                ('complete', models.BooleanField(default=False)),
                ('member', models.ForeignKey(to='account.Member')),
                ('request', models.ForeignKey(to='requests.Request')),
            ],
        ),
    ]
