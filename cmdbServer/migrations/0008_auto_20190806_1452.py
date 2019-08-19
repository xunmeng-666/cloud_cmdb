# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-08-06 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdbServer', '0007_tasks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='tasks',
        ),
        migrations.AddField(
            model_name='tasks',
            name='script',
            field=models.FilePathField(blank=True, null=type, verbose_name='Playbook'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='result',
            field=models.FilePathField(blank=True, null=True, verbose_name='执行结果'),
        ),
    ]