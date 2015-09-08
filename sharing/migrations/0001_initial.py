# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('share_type', models.CharField(db_index=True, max_length=30, choices=[(b'all_friends', b'all_friends'), (b'all_friends_groups', b'all_friends_groups'), (b'share_list', b'share_list'), (b'custom', b'custom')])),
                ('share_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('type', models.CharField(db_index=True, max_length=30, choices=[(b'stuff', b'Stuff'), (b'space', b'Space'), (b'labor', b'Labor/Skills')])),
                ('title', models.CharField(max_length=120, db_index=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.CharField(max_length=30, null=True, blank=True)),
                ('thumb', models.CharField(max_length=30, null=True, blank=True)),
                ('to_borrow', models.BooleanField(default=True, db_index=True)),
                ('to_keep', models.BooleanField(default=False, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=60, db_index=True)),
                ('item', models.ForeignKey(to='sharing.Item')),
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
            name='ShareList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('owner', models.ForeignKey(to='account.Member')),
            ],
        ),
        migrations.CreateModel(
            name='ShareListSharee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shareList', models.ForeignKey(to='sharing.ShareList')),
                ('sharee', models.ForeignKey(to='account.Participant')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='sharelist',
            field=models.ForeignKey(blank=True, to='sharing.ShareList', null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='sharer',
            field=models.ForeignKey(to='account.Member'),
        ),
    ]
