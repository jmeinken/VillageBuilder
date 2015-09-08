# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('body', models.TextField()),
                ('complete', models.BooleanField(default=False, db_index=True)),
                ('member', models.ForeignKey(to='account.Member')),
            ],
        ),
        migrations.CreateModel(
            name='RequestComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('body', models.TextField()),
                ('member', models.ForeignKey(to='account.Member')),
                ('request', models.ForeignKey(to='requests.Request')),
            ],
        ),
    ]
