# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0003_auto_20150825_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.CharField(default='all_friends', max_length=30, choices=[(b'stuff', b'stuff'), (b'space', b'space'), (b'labor', b'labor')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='share_type',
            field=models.CharField(max_length=30, choices=[(b'all_friends', b'all_friends'), (b'all_friends_groups', b'all_friends_groups'), (b'share_list', b'share_list'), (b'custom', b'custom')]),
        ),
    ]
