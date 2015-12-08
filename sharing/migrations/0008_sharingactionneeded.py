# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20151119_2244'),
        ('sharing', '0007_auto_20151206_2224'),
    ]

    operations = [
        migrations.CreateModel(
            name='SharingActionNeeded',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=20, db_index=True)),
                ('alertee', models.ForeignKey(to='account.Member')),
                ('subject', models.ForeignKey(to='account.Participant')),
            ],
        ),
    ]
