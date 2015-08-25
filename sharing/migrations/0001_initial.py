# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20150821_1151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('parent', models.ForeignKey(blank=True, to='sharing.Category', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('share_type', models.CharField(max_length=6, choices=[(b'all_friends', b'all_friends'), (b'all_friends_groups', b'all_friends_groups'), (b'share_list', b'share_list'), (b'custom', b'custom')])),
                ('share_date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('category', models.ForeignKey(to='sharing.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ItemSharee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.ForeignKey(to='sharing.Item')),
                ('sharee', models.ForeignKey(to='account.Participant')),
            ],
        ),
        migrations.CreateModel(
            name='Sharelist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('owner', models.ForeignKey(to='account.Member')),
            ],
        ),
        migrations.CreateModel(
            name='SharelistSharee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sharee', models.ForeignKey(to='account.Participant')),
                ('sharelist', models.ForeignKey(to='sharing.Sharelist')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='sharelist',
            field=models.ForeignKey(blank=True, to='sharing.Sharelist', null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='sharer',
            field=models.ForeignKey(to='account.Member'),
        ),
    ]
