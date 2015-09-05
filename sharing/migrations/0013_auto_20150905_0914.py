# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0012_auto_20150905_0201'),
    ]

    operations = [
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
