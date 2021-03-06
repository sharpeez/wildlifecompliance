# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-12-19 09:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0351_remove_artifact_custodian'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegalCaseRunningSheetArtifacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_artifacts', models.ManyToManyField(related_name='running_sheet_document_artifacts', to='wildlifecompliance.DocumentArtifact')),
                ('legal_case', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='running_sheet_artifacts', to='wildlifecompliance.LegalCase')),
                ('physical_artifacts', models.ManyToManyField(related_name='running_sheet_physical_artifacts', to='wildlifecompliance.PhysicalArtifact')),
            ],
        ),
    ]
