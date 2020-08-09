# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-12-11 02:49
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wildlifecompliance', '0341_sanctionoutcomeduedate_due_date_term_currently_applied'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artifact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'CM_Artifact',
                'verbose_name_plural': 'CM_Artifacts',
            },
        ),
        migrations.CreateModel(
            name='DocumentArtifactType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artifact_type', models.CharField(max_length=50)),
                ('version', models.SmallIntegerField(default=1)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('replaced_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wildlifecompliance.DocumentArtifactType')),
            ],
            options={
                'verbose_name': 'CM_DocumentArtifactType',
                'verbose_name_plural': 'CM_DocumentArtifactTypes',
            },
        ),
        migrations.CreateModel(
            name='PhysicalArtifactDisposalMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disposal_method', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'CM_PhysicalArtifactDisposalMethod',
                'verbose_name_plural': 'CM_PhysicalArtifactDisposalMethods',
            },
        ),
        migrations.CreateModel(
            name='PhysicalArtifactType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artifact_type', models.CharField(max_length=50)),
                ('details_schema', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('storage_schema', django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                ('version', models.SmallIntegerField(default=1)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('replaced_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wildlifecompliance.PhysicalArtifactType')),
            ],
            options={
                'verbose_name': 'CM_PhysicalArtifactType',
                'verbose_name_plural': 'CM_PhysicalArtifactTypes',
            },
        ),
        migrations.CreateModel(
            name='DocumentArtifact',
            fields=[
                ('artifact_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wildlifecompliance.Artifact')),
                ('_file', models.FileField(max_length=255, upload_to=b'')),
                ('identifier', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('document_created_date', models.DateField(null=True)),
                ('document_created_time', models.TimeField(blank=True, null=True)),
                ('custodian', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_artifact_custodian', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'CM_DocumentArtifact',
                'verbose_name_plural': 'CM_DocumentArtifacts',
            },
            bases=('wildlifecompliance.artifact',),
        ),
        migrations.CreateModel(
            name='PhysicalArtifact',
            fields=[
                ('artifact_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wildlifecompliance.Artifact')),
                ('identifier', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('used_within_case', models.BooleanField(default=False)),
                ('sensitive_non_disclosable', models.BooleanField(default=False)),
                ('artifact_created_date', models.DateField(null=True)),
                ('artifact_created_time', models.TimeField(blank=True, null=True)),
                ('_file', models.FileField(max_length=255, upload_to=b'')),
                ('disposal_date', models.DateField(null=True)),
                ('disposal_details', models.TextField(blank=True, null=True)),
                ('custodian', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='physical_artifact_custodian', to=settings.AUTH_USER_MODEL)),
                ('disposal_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wildlifecompliance.PhysicalArtifactDisposalMethod')),
                ('officer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='physical_artifact_officer', to=settings.AUTH_USER_MODEL)),
                ('physical_artifact_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wildlifecompliance.DocumentArtifactType')),
                ('statement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='physical_artifact_statement', to='wildlifecompliance.DocumentArtifact')),
            ],
            options={
                'verbose_name': 'CM_DocumentArtifact',
                'verbose_name_plural': 'CM_DocumentArtifacts',
            },
            bases=('wildlifecompliance.artifact',),
        ),
        migrations.AlterUniqueTogether(
            name='physicalartifacttype',
            unique_together=set([('artifact_type', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='documentartifacttype',
            unique_together=set([('artifact_type', 'version')]),
        ),
        migrations.AddField(
            model_name='documentartifact',
            name='document_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wildlifecompliance.DocumentArtifactType'),
        ),
        migrations.AddField(
            model_name='documentartifact',
            name='interviewer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_artifact_interviewer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documentartifact',
            name='offence',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_artifact_offence', to='wildlifecompliance.Offence'),
        ),
        migrations.AddField(
            model_name='documentartifact',
            name='people_attending',
            field=models.ManyToManyField(related_name='document_artifact_people_attending', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documentartifact',
            name='person_providing_statement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='document_artifact_person_providing_statement', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documentartifact',
            name='statement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='document_artifact_statement', to='wildlifecompliance.DocumentArtifact'),
        ),
    ]