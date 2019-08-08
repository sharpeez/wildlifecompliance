# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-21 01:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20160913_0931'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailUserReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occurence', models.IntegerField()),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('dob', models.DateField(null=True, verbose_name='date of birth')),
            ],
            options={
                'db_table': 'accounts_emailuser_report_v',
                'managed': False,
            },
        ),
    ]
