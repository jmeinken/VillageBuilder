# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationships', '0002_auto_20150804_1045'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupmembership',
            old_name='request_received_from_group',
            new_name='invited',
        ),
        migrations.RenameField(
            model_name='groupmembership',
            old_name='request_sent_to_group',
            new_name='requested',
        ),
    ]
