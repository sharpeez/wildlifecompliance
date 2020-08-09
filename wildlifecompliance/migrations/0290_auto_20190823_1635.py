# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-08-23 08:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0289_weaklinks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callemail',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('open', 'Open'), ('open_followup', 'Open (follow-up)'), ('open_inspection', 'Open (Inspection)'), ('open_case', 'Open (Case)'), ('closed', 'Closed')], default='draft', max_length=40),
        ),
        migrations.AlterField(
            model_name='inspection',
            name='organisation_inspected',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organisation_inspected', to='accounts.Organisation'),
        ),
    ]