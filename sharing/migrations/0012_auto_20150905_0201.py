# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0011_auto_20150831_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='share_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='share_type',
            field=models.CharField(db_index=True, max_length=30, choices=[(b'all_friends', b'all_friends'), (b'all_friends_groups', b'all_friends_groups'), (b'share_list', b'share_list'), (b'custom', b'custom')]),
        ),
        migrations.AlterField(
            model_name='item',
            name='sharelist',
            field=models.ForeignKey(blank=True, to='sharing.ShareList', null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(max_length=120, db_index=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='to_borrow',
            field=models.BooleanField(default=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='to_keep',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(db_index=True, max_length=30, choices=[(b'stuff', b'Stuff'), (b'space', b'Space'), (b'labor', b'Labor/Skills')]),
        ),
        migrations.AlterField(
            model_name='itemkeyword',
            name='keyword',
            field=models.CharField(max_length=60, db_index=True),
        ),
        migrations.AlterField(
            model_name='sharelistsharee',
            name='shareList',
            field=models.ForeignKey(to='sharing.ShareList'),
        ),
    ]
