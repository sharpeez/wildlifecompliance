# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-08-26 06:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0507_purposespecies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purposespecies',
            name='header',
            field=models.CharField(max_length=255),
        ),
    ]
