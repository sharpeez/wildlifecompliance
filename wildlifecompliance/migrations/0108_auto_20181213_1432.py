# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-12-13 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0107_merge_20181211_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisationrequest',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]
