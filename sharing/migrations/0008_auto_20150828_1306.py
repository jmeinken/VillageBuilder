# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sharing', '0007_auto_20150828_1034'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=60)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='sharelist',
            field=models.ForeignKey(blank=True, to='sharing.ShareList', null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.CharField(max_length=30, choices=[(b'stuff', b'Stuff'), (b'space', b'Space'), (b'skills', b'Skills')]),
        ),
        migrations.AlterField(
            model_name='sharelistsharee',
            name='shareList',
            field=models.ForeignKey(to='sharing.ShareList'),
        ),
        migrations.AddField(
            model_name='itemkeyword',
            name='item',
            field=models.ForeignKey(to='sharing.Item'),
        ),
    ]
