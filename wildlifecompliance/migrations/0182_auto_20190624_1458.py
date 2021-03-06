# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-06-24 06:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0181_auto_20190619_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='returntype',
            name='fee_amount',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=8),
        ),
        migrations.AddField(
            model_name='returntype',
            name='fee_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='returntype',
            name='fee_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='returntype',
            name='data_format',
            field=models.CharField(choices=[('sheet', 'Sheet'), ('question', 'Question'), ('data', 'Data')], default='data', max_length=30, verbose_name='Data format'),
        ),
    ]
