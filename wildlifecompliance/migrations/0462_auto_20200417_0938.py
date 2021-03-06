# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-04-17 01:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0461_applicationselectedactivity_additional_licence_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityinvoice',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activity_invoices', to='wildlifecompliance.ApplicationSelectedActivity'),
        ),
    ]
