# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-08-26 06:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0506_auto_20200818_2103'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurposeSpecies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('header', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('purpose', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wildlifecompliance.LicencePurpose')),
            ],
            options={
                'ordering': ['order', 'header'],
                'verbose_name': 'Purpose Species',
                'verbose_name_plural': 'Purpose Species',
            },
        ),
    ]
