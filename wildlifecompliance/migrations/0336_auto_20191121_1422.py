# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-11-21 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0335_auto_20191121_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sanctionoutcome',
            name='status',
            field=models.CharField(choices=[(b'draft', b'Draft'), (b'awaiting_endorsement', b'Awaiting Endorsement'), (b'awaiting_payment', b'Awaiting Payment'), (b'awaiting_review', b'Awaiting Review'), (b'awaiting_remediation_actions', b'Awaiting Remediation Actions'), (b'declined', b'Declined'), (b'overdue', b'Overdue'), (b'withdrawn', b'Withdrawn'), (b'closed', b'Closed')], default=b'draft', max_length=40),
        ),
    ]
