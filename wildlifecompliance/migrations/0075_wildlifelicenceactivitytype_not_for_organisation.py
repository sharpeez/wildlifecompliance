# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-08-17 02:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0074_auto_20180816_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='wildlifelicenceactivitytype',
            name='not_for_organisation',
            field=models.BooleanField(
                default=False,
                help_text='If ticked, this licenced activity will not be available for applications on behalf of an organisation.'),
        ),
    ]
