# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-01-18 06:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wildlifecompliance', '0116_merge_20190118_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='processing_status',
            field=models.CharField(
                choices=[
                    ('draft',
                     'Draft'),
                    ('with_officer',
                     'With Officer'),
                    ('with_assessor',
                     'With Assessor'),
                    ('with_assessor_conditions',
                     'With Assessor (Conditions)'),
                    ('with_approver',
                     'With Approver'),
                    ('renewal',
                     'Renewal'),
                    ('licence_amendment',
                     'Licence Amendment'),
                    ('awaiting_applicant_response',
                     'Awaiting Applicant Response'),
                    ('awaiting_assessor_response',
                     'Awaiting Assessor Response'),
                    ('awaiting_responses',
                     'Awaiting Responses'),
                    ('ready_for_conditions',
                     'Ready for Conditions'),
                    ('ready_to_issue',
                     'Ready to Issue'),
                    ('approved',
                     'Approved'),
                    ('declined',
                     'Declined'),
                    ('discarded',
                     'Discarded'),
                    ('under_review',
                     'Under Review')],
                default='draft',
                max_length=30,
                verbose_name='Processing Status'),
        ),
    ]
