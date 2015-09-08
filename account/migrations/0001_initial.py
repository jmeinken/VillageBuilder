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
                ('title', models.CharField(max_length=120, db_index=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('neighborhood', models.CharField(max_length=60, null=True, blank=True)),
                ('city', models.CharField(max_length=60, null=True, blank=True)),
                ('state', models.CharField(max_length=2, null=True, blank=True)),
                ('phone_number', models.CharField(max_length=20, null=True, blank=True)),
                ('phone_type', models.CharField(blank=True, max_length=20, null=True, choices=[(b'mobile', b'mobile'), (b'home', b'home'), (b'work', b'work')])),
                ('email', models.CharField(max_length=120, null=True, blank=True)),
                ('website', models.CharField(max_length=240, null=True, blank=True)),
                ('image', models.CharField(max_length=30, null=True, blank=True)),
                ('thumb', models.CharField(max_length=30, null=True, blank=True)),
                ('private', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('code', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('full_address', models.CharField(max_length=600)),
                ('street', models.CharField(max_length=60, null=True, blank=True)),
                ('neighborhood', models.CharField(max_length=60, null=True, blank=True)),
                ('city', models.CharField(max_length=60)),
                ('state', models.CharField(max_length=2, null=True, blank=True)),
                ('zip_code', models.CharField(max_length=10, null=True, blank=True)),
                ('latitude', models.DecimalField(max_digits=10, decimal_places=7)),
                ('longitude', models.DecimalField(max_digits=10, decimal_places=7)),
                ('phone_number', models.CharField(max_length=20, null=True, blank=True)),
                ('phone_type', models.CharField(blank=True, max_length=20, null=True, choices=[(b'mobile', b'mobile'), (b'home', b'home'), (b'work', b'work')])),
                ('share_email', models.BooleanField(default=True)),
                ('share_phone', models.BooleanField()),
                ('share_street', models.BooleanField(default=True)),
                ('image', models.CharField(max_length=30, null=True, blank=True)),
                ('thumb', models.CharField(max_length=30, null=True, blank=True)),
                ('code', models.CharField(max_length=60, null=True, blank=True)),
                ('is_admin', models.BooleanField(default=False, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(db_index=True, max_length=6, choices=[(b'member', b'member'), (b'guest', b'guest'), (b'group', b'group')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='participant',
            field=models.OneToOneField(to='account.Participant'),
        ),
        migrations.AddField(
            model_name='guest',
            name='created_by',
            field=models.ForeignKey(to='account.Member'),
        ),
        migrations.AddField(
            model_name='guest',
            name='participant',
            field=models.OneToOneField(to='account.Participant'),
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(to='account.Member'),
        ),
        migrations.AddField(
            model_name='group',
            name='participant',
            field=models.OneToOneField(to='account.Participant'),
        ),
    ]
