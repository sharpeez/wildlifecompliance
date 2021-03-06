# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-15 06:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0535_auto_20210511_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionOptionCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('value', models.CharField(blank=True, default='', max_length=100)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_options', to='wildlifecompliance.QuestionOption')),
            ],
            options={
                'verbose_name': 'Schema Question Condition',
            },
        ),
        migrations.CreateModel(
            name='SectionQuestionCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Schema Section Question Condition',
            },
        ),
        migrations.AddField(
            model_name='sectionquestion',
            name='apply_special_conditions',
            field=models.BooleanField(default=False, help_text='If ticked, select the Save and Continue Editing button.'),
        ),
        migrations.AlterField(
            model_name='masterlistquestion',
            name='answer_type',
            field=models.CharField(choices=[('text', 'Text'), ('radiobuttons', 'Radio button'), ('checkbox', 'Checkbox'), ('number', 'Number'), ('email', 'Email'), ('text_area', 'Text area'), ('label', 'Label'), ('file', 'File'), ('date', 'Date'), ('group', 'Group'), ('group2', 'Group2'), ('expander_table', 'Expander Table'), ('species-all', 'Species List'), ('header', 'Expander Table Header'), ('expander', 'Expander Table Expander')], default='text', max_length=40, verbose_name='Answer Type'),
        ),
        migrations.AlterField(
            model_name='sectionquestion',
            name='parent_question',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='section', chained_model_field='question_sections__section', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children_questions', to='wildlifecompliance.MasterlistQuestion'),
        ),
        migrations.AlterField(
            model_name='sectionquestion',
            name='tag',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('isRepeatable', 'isRepeatable'), ('isLicenceField', 'isLicenceField')], max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='sectionquestioncondition',
            name='section_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='special_conditions', to='wildlifecompliance.SectionQuestion'),
        ),
    ]
