# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-10-22 23:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0093_auto_20181023_0729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='returntype',
            name='condition',
        ),
    ]
