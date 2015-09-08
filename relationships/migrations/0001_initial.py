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
                ('created', models.DateTimeField(auto_now_add=True)),
                ('friend', models.ForeignKey(related_name='reverse_friendship_set', to='account.Member')),
                ('member', models.ForeignKey(related_name='friendship_set', to='account.Member')),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('requested', models.BooleanField(default=False, db_index=True)),
                ('invited', models.BooleanField(default=False, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(to='account.Group')),
                ('member', models.ForeignKey(to='account.Member')),
            ],
        ),
        migrations.CreateModel(
            name='GuestFriendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('guest', models.ForeignKey(to='account.Guest')),
                ('member', models.ForeignKey(to='account.Member')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='guestfriendship',
            unique_together=set([('member', 'guest')]),
        ),
        migrations.AlterUniqueTogether(
            name='groupmembership',
            unique_together=set([('group', 'member')]),
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('member', 'friend')]),
        ),
    ]
