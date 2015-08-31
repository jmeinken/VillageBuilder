# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0009_auto_20150828_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='to_borrow',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='item',
            name='to_keep',
            field=models.NullBooleanField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='sharelist',
            field=models.ForeignKey(blank=True, to='sharing.ShareList', null=True),
        ),
        migrations.AlterField(
            model_name='sharelistsharee',
            name='shareList',
            field=models.ForeignKey(to='sharing.ShareList'),
        ),
    ]
