# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('email', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=60)),
                ('first_name', models.CharField(max_length=30, null=True, blank=True)),
                ('last_name', models.CharField(max_length=30, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('full_address', models.CharField(max_length=400)),
                ('address1', models.CharField(max_length=50, null=True, blank=True)),
                ('address2', models.CharField(max_length=50, null=True, blank=True)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('state', models.CharField(max_length=2, null=True, blank=True)),
                ('zip_code', models.CharField(max_length=10, null=True, blank=True)),
                ('latitude', models.DecimalField(max_digits=10, decimal_places=7)),
                ('longitude', models.DecimalField(max_digits=10, decimal_places=7)),
                ('street', models.CharField(max_length=50)),
                ('neighborhood', models.CharField(max_length=50, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=20, null=True, blank=True)),
                ('phone_type', models.CharField(blank=True, max_length=20, null=True, choices=[(b'mobile', b'mobile'), (b'home', b'home'), (b'work', b'work')])),
                ('share_email', models.BooleanField()),
                ('share_address', models.BooleanField()),
                ('share_phone', models.BooleanField()),
                ('user_pic_medium', models.CharField(max_length=100, null=True, blank=True)),
                ('user_pic_small', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('participant_type', models.CharField(max_length=6, choices=[(b'person', b'person'), (b'guest', b'guest'), (b'group', b'group')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('member', models.OneToOneField(to='account.Member')),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='participant',
            field=models.OneToOneField(to='account.Participant'),
        ),
        migrations.AddField(
            model_name='guest',
            name='participant',
            field=models.OneToOneField(to='account.Participant'),
        ),
        migrations.AddField(
            model_name='group',
            name='member',
            field=models.OneToOneField(to='account.Member'),
        ),
    ]
