# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-01-21 08:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0117_auto_20190118_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referral',
            name='application',
        ),
        migrations.RemoveField(
            model_name='referral',
            name='referral',
        ),
        migrations.RemoveField(
            model_name='referral',
            name='sent_by',
        ),
        migrations.DeleteModel(
            name='Referral',
        ),
    ]
