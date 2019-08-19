# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-08-15 14:03
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdbServer', '0016_auto_20190814_1400'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='command',
        ),
        migrations.AlterField(
            model_name='tasks',
            name='result',
            field=django.contrib.postgres.fields.jsonb.JSONField(verbose_name='执行结果'),
        ),
    ]
