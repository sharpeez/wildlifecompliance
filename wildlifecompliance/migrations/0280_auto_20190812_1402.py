# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-08-12 06:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0279_remove_callemail_inspection_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='InspectionDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('_file', models.FileField(max_length=255, upload_to=b'')),
                ('input_name', models.CharField(blank=True, max_length=255, null=True)),
                ('can_delete', models.BooleanField(default=True)),
                ('version_comment', models.CharField(blank=True, max_length=255, null=True)),
                ('inspection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='wildlifecompliance.Inspection')),
            ],
        ),
        migrations.AlterField(
            model_name='callemaildocument',
            name='_file',
            field=models.FileField(max_length=255, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='callemaillogdocument',
            name='_file',
            field=models.FileField(max_length=255, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='inspectioncommslogdocument',
            name='_file',
            field=models.FileField(max_length=255, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='inspectionreportdocument',
            name='_file',
            field=models.FileField(max_length=255, upload_to=b''),
        ),
    ]