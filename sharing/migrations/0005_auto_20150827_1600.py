# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0004_auto_20150825_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharelistsharee',
            name='sharelist',
        ),
        migrations.AddField(
            model_name='sharelistsharee',
            name='shareList',
            field=models.ForeignKey(default=1, to='sharing.ShareList'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='sharelist',
            field=models.ForeignKey(blank=True, to='sharing.ShareList', null=True),
        ),
    ]
