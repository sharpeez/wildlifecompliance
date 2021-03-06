# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-12-19 02:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0108_auto_20181217_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='wildlifelicence',
            name='licence_class',
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to='wildlifecompliance.WildlifeLicenceClass'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wildlifelicenceactivity',
            name='code',
            field=models.CharField(
                default='',
                max_length=4),
        ),
        migrations.AlterUniqueTogether(
            name='wildlifelicence',
            unique_together=set(
                [
                    ('licence_number',
                     'licence_sequence',
                     'licence_class')]),
        ),
    ]
