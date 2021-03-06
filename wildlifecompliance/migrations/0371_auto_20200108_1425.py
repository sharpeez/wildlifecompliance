# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-01-08 06:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0370_auto_20200108_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artifact',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('waiting_for_disposal', 'Waiting For Disposal'), ('closed', 'Closed')], default='active', max_length=100),
        ),
        migrations.AlterField(
            model_name='artifactuseraction',
            name='who',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
