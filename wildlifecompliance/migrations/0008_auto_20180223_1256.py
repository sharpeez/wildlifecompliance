# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-23 04:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0007_organisationcontactaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisationcontact',
            name='user_status',
            field=models.CharField(
                choices=[
                    ('draft',
                     'Draft'),
                    ('pending',
                     'Pending'),
                    ('active',
                     'Active'),
                    ('decline',
                     'Decline'),
                    ('unlinked',
                     'Unlinked'),
                    ('suspended',
                     'Suspended')],
                default='draft',
                max_length=40,
                verbose_name='Status'),
        ),
    ]
