# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20151119_2244'),
        ('sharing', '0006_auto_20151123_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shared', models.BooleanField(default=True, db_index=True)),
                ('group', models.ForeignKey(to='account.Group')),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='share_type',
            field=models.CharField(db_index=True, max_length=30, choices=[(b'all_friends', b'all_friends'), (b'share_list', b'share_list'), (b'custom', b'custom')]),
        ),
        migrations.AlterField(
            model_name='itemsharee',
            name='sharee',
            field=models.ForeignKey(to='account.Member'),
        ),
        migrations.AlterField(
            model_name='sharelistsharee',
            name='sharee',
            field=models.ForeignKey(to='account.Member'),
        ),
        migrations.AddField(
            model_name='itemgroup',
            name='item',
            field=models.ForeignKey(to='sharing.Item'),
        ),
    ]
