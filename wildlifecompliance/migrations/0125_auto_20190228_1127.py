# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-02-28 03:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0124_auto_20190228_1035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='proposed_decline_status',
        ),
        migrations.RemoveField(
            model_name='application',
            name='proposed_issuance_licence',
        ),
    ]
