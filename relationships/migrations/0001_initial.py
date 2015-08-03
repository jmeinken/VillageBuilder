# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('friend', models.ForeignKey(related_name='reverse_friendship_set', to='account.Member')),
                ('member', models.ForeignKey(related_name='friendship_set', to='account.Member')),
            ],
        ),
        migrations.CreateModel(
            name='GuestFriendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guest', models.ForeignKey(to='account.Guest')),
                ('member', models.ForeignKey(to='account.Member')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='guestfriendship',
            unique_together=set([('member', 'guest')]),
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('member', 'friend')]),
        ),
    ]
