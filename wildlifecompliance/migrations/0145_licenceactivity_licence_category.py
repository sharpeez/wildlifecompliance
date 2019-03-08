# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-03-08 05:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0144_merge_20190307_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='licenceactivity',
            name='licence_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wildlifecompliance.LicenceCategory'),
        ),
        migrations.RunSQL("""
            UPDATE wildlifecompliance_licenceactivity AS activity
                SET licence_category_id = da.licence_category_id
            FROM
                wildlifecompliance_defaultactivity AS da
            WHERE
                activity.ID = da.activity_id;
        """, reverse_sql=""),
    ]
